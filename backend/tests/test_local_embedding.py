import asyncio
from types import SimpleNamespace
import numpy as np
import pytest
from app.core.config import settings
from app.rag import local_embedding
from app.rag.embedding import EmbeddingService, EmbeddingError


class Tokenizer:
    def num_special_tokens_to_add(self): return 2
    def encode(self, text, **kwargs): return list(range(len(text.split())))
    def decode(self, tokens, **kwargs): return " ".join(map(str, tokens))


class Model:
    tokenizer = Tokenizer()
    max_seq_length = 6
    def get_sentence_embedding_dimension(self): return 3
    def encode(self, texts, **kwargs):
        self.pieces = texts
        return np.array([[1., 0., 0.] if i == 0 else [0., 1., 0.] for i, _ in enumerate(texts)])


def test_long_text_pools_tail_and_rejects_wrong_dimension(monkeypatch):
    model = Model()
    monkeypatch.setattr(local_embedding, "_load_model", lambda *args: model)
    vector = local_embedding.encode_local('test', 'cache', True, ['a b c d e f'], 3)[0]
    assert model.pieces == ['0 1 2 3', '4 5']
    assert vector[1] > 0 and np.linalg.norm(vector) == pytest.approx(1)
    with pytest.raises(ValueError, match="DIMENSION"):
        local_embedding.encode_local('test', 'cache', True, ['a'], 384)


@pytest.mark.asyncio
async def test_local_no_api_key_no_remote_client_and_batch(monkeypatch):
    monkeypatch.setattr(settings, 'embedding_provider', 'local')
    monkeypatch.setattr(settings, 'openai_api_key', '')
    monkeypatch.setattr(settings, 'embedding_api_key', '')
    monkeypatch.setattr(settings, 'embedding_dimension', 3)
    monkeypatch.setattr(local_embedding, '_load_model', lambda *args: Model())
    def forbidden(*args): raise AssertionError('Remote API used')
    monkeypatch.setattr(EmbeddingService, '_build_client', forbidden)
    service = EmbeddingService()
    result = await service.embed_texts(['中文 问题', 'English question'])
    assert len(result) == 2 and len(result[0].vector) == 3
    assert len((await service.embed_text('知识库')).vector) == 3
    assert await service.embed_texts([]) == []
    with pytest.raises(EmbeddingError, match='empty'):
        await service.embed_texts(['  '])


@pytest.mark.asyncio
async def test_download_failure_is_explicit_without_remote_fallback(monkeypatch):
    monkeypatch.setattr(settings, 'embedding_provider', 'local')
    def unavailable(*args): raise OSError('offline')
    monkeypatch.setattr(local_embedding, '_load_model', unavailable)
    with pytest.raises(EmbeddingError, match='Local embedding failed'):
        await EmbeddingService().embed_text('test')
