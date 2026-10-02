"""Product regressions: real PDF/SQL/Qdrant-local pipeline, mocked external model HTTP."""
import io
import json
from uuid import uuid4

import fitz
import httpx
import openai
import pytest
import pytest_asyncio
from qdrant_client import QdrantClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import delete

from app.core.config import settings
from app.core.deps import DEFAULT_OWNER_ID
from app.db import Base, get_db
from app.main import create_app
from app.models import User
from app.rag.vector_store import QdrantVectorStore

ADMIN = "test-only-administrator-key-000000000000"
HEADERS = {"Authorization": f"Bearer {ADMIN}"}


@pytest_asyncio.fixture
async def system(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "embedding_provider", "openai")
    monkeypatch.setattr(settings, "admin_api_key", ADMIN)
    monkeypatch.setattr(settings, "knowledge_owner_id", DEFAULT_OWNER_ID)
    monkeypatch.setattr(settings, "upload_dir", str(tmp_path / "uploads"))
    monkeypatch.setattr(settings, "embedding_dimension", 3)
    monkeypatch.setattr(settings, "embedding_api_key", "test-embedding")
    monkeypatch.setattr(settings, "embedding_base_url", "https://embedding.test/v1")
    monkeypatch.setattr(settings, "openai_api_key", "test-chat")
    monkeypatch.setattr(settings, "openai_base_url", "https://llm.test/v1")
    monkeypatch.setattr(settings, "openai_model", "test-model")
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with sessions() as db:
        db.add(User(id=DEFAULT_OWNER_ID, username="owner", email="owner@test.invalid", password_hash="!"))
        await db.commit()
    async def database():
        async with sessions() as db:
            yield db
    app = create_app()
    app.dependency_overrides[get_db] = database
    vector_client = QdrantClient(":memory:")
    monkeypatch.setattr(QdrantVectorStore, "_build_client", lambda self: vector_client)
    calls = []
    async def provider(request):
        body = json.loads(request.content)
        calls.append((str(request.url), body))
        if request.url.path.endswith("/embeddings"):
            assert request.headers["authorization"] == "Bearer test-embedding"
            return httpx.Response(200, json={"data": [{"embedding": [1.0, 0.1, 0.2], "index": 0}], "model": "test", "object": "list"})
        assert request.url.host == "llm.test"
        assert request.headers["authorization"] == "Bearer test-chat"
        assert "40 percent" in body["messages"][1]["content"]
        return httpx.Response(200, json={"id":"test", "object":"chat.completion", "created":0, "model":"test-model", "choices":[{"index":0,"message":{"role":"assistant","content":"The exam is 40 percent. [1]"},"finish_reason":"stop"}]})
    real_client = openai.AsyncOpenAI
    monkeypatch.setattr(openai, "AsyncOpenAI", lambda **kwargs: real_client(**kwargs, http_client=httpx.AsyncClient(transport=httpx.MockTransport(provider))))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        yield client, vector_client, calls, sessions
    vector_client.close()
    await engine.dispose()


def pdf_bytes():
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Course assessment: the exam is 40 percent. Coursework is 60 percent.")
    data = doc.tobytes()
    doc.close()
    return data


@pytest.mark.asyncio
async def test_admin_boundary_and_removed_routes(system, monkeypatch):
    client, _, _, _ = system
    doc_id = uuid4()
    routes = [("GET", "/api/documents"), ("POST", "/api/documents/upload"),
              ("DELETE", f"/api/documents/{doc_id}"), ("POST", f"/api/documents/{doc_id}/reindex"),
              ("GET", f"/api/documents/{doc_id}/status"), ("GET", "/api/documents/chunks/search?q=test"),
              ("GET", "/api/llm/status")]
    for method, path in routes:
        assert (await client.request(method, path)).status_code == 401
        assert (await client.request(method, path, headers={"Authorization":"Bearer wrong"})).status_code == 401
    for path in ["auth/register", "auth/login", "tasks", "review", "plan/generate"]:
        assert (await client.post(f"/api/{path}", json={})).status_code == 404
    assert (await client.get("/api/documents", headers=HEADERS)).status_code == 200
    monkeypatch.setattr(settings, "admin_api_key", "")
    assert (await client.get("/api/documents", headers=HEADERS)).status_code == 503


@pytest.mark.asyncio
async def test_upload_vector_retrieve_answer_citation_reindex_delete(system, monkeypatch):
    client, vector, calls, sessions = system
    uploaded = await client.post("/api/documents/upload", headers=HEADERS, files={"file":("course.pdf", pdf_bytes(), "application/pdf")})
    assert uploaded.status_code == 201, uploaded.text
    doc_id = uploaded.json()["task_id"]
    status = (await client.get(f"/api/documents/{doc_id}/status", headers=HEADERS)).json()
    assert status["status"] == "processed" and status["total_chunks"] > 0
    assert status["error_message"] is None
    count = vector.count(settings.qdrant_collection_name).count
    assert count == status["total_chunks"]
    response = await client.post("/api/rag/ask", json={"question":"What is the exam assessment?"})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["answer"] == "The exam is 40 percent. [1]"
    assert result["is_placeholder"] is False
    assert result["sources"][0]["filename"] == "course.pdf"
    assert result["sources"][0]["page_start"] == 1
    # Old /chat endpoint now always uses knowledge, including planning-like wording.
    stream = await client.post("/api/chat", json={"message":"plan exam assessment"})
    assert 'event: citations' in stream.text and 'event: done' in stream.text
    assert 'created_tasks' not in stream.text
    reindexed = await client.post(f"/api/documents/{doc_id}/reindex", headers=HEADERS)
    assert reindexed.status_code == 200 and reindexed.json()["error_message"] is None
    assert vector.count(settings.qdrant_collection_name).count == count
    assert any("embedding.test" in url for url, _ in calls)
    assert any("llm.test" in url for url, _ in calls)
    # Selecting another owner cannot reveal or mutate this owner's data.
    other = uuid4()
    async with sessions() as db:
        db.add(User(id=other,username="other",email="other@test.invalid",password_hash="!"))
        await db.commit()
    monkeypatch.setattr(settings, "knowledge_owner_id", other)
    isolated = (await client.post("/api/rag/ask", json={"question":"exam", "document_id":doc_id})).json()
    assert isolated["sources"] == []
    assert (await client.delete(f"/api/documents/{doc_id}", headers=HEADERS)).status_code == 404
    monkeypatch.setattr(settings, "knowledge_owner_id", DEFAULT_OWNER_ID)
    assert (await client.delete(f"/api/documents/{doc_id}", headers=HEADERS)).status_code == 200
    assert vector.count(settings.qdrant_collection_name).count == 0
    assert (await client.get("/api/documents", headers=HEADERS)).json() == []
    assert (await client.post("/api/rag/ask", json={"question":"exam"})).json()["sources"] == []


@pytest.mark.asyncio
async def test_embedding_failure_visible_and_repairable(system, monkeypatch):
    from app.rag.embedding import EmbeddingService, EmbeddingError
    client, _, _, _ = system
    original = EmbeddingService._request_embedding
    async def fail(self, text):
        raise EmbeddingError("test outage")
    monkeypatch.setattr(EmbeddingService, "_request_embedding", fail)
    uploaded = await client.post("/api/documents/upload", headers=HEADERS, files={"file":("course.pdf",pdf_bytes(),"application/pdf")})
    assert uploaded.status_code == 201
    doc_id=uploaded.json()["task_id"]
    status=(await client.get(f"/api/documents/{doc_id}/status",headers=HEADERS)).json()
    assert status["status"] == "processed" and status["error_message"]
    monkeypatch.setattr(EmbeddingService, "_request_embedding", original)
    repaired = await client.post(f"/api/documents/{doc_id}/reindex",headers=HEADERS)
    assert repaired.json()["error_message"] is None


@pytest.mark.asyncio
async def test_invalid_input_empty_knowledge_and_missing_owner(system, monkeypatch):
    client, _, calls, _ = system
    assert (await client.post("/api/rag/ask", json={"question":""})).status_code == 422
    assert (await client.post("/api/rag/ask", json={"question":"x"*1001})).status_code == 422
    assert (await client.post("/api/documents/upload",headers=HEADERS,files={"file":("bad.txt",b"test","text/plain")})).status_code == 400
    answer=(await client.post("/api/rag/ask",json={"question":"anything"})).json()
    assert not answer["sources"] and "只能依据知识库" in answer["answer"]
    assert not any("llm.test" in url for url,_ in calls)
    monkeypatch.setattr(settings,"knowledge_owner_id",uuid4())
    assert (await client.post("/api/rag/ask",json={"question":"exam"})).status_code == 503


@pytest.mark.asyncio
async def test_new_install_creates_disabled_shared_owner(system):
    client, _, _, sessions = system
    async with sessions() as db:
        await db.execute(delete(User))
        await db.commit()
    response=await client.get("/api/documents",headers=HEADERS)
    assert response.status_code == 200
    async with sessions() as db:
        owner=await db.get(User,DEFAULT_OWNER_ID)
        assert owner.password_hash == "!disabled"
    assert (await client.post("/api/rag/ask",json={"question":"anything"})).status_code == 200
