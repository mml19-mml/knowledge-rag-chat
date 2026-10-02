from typing import Annotated
from uuid import UUID
import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db import get_db
from app.models.user import User

DbSession = Annotated[AsyncSession, Depends(get_db)]
bearer = HTTPBearer(auto_error=False)
DEFAULT_OWNER_ID = UUID("00000000-0000-4000-8000-000000000001")

async def require_admin(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> None:
    expected = settings.admin_api_key.strip()
    if len(expected) < 32 or expected in {"change-me", "sk-change-me"}:
        raise HTTPException(503, "管理员访问尚未配置，请设置至少 32 位随机 ADMIN_API_KEY。")
    if credentials is None or not secrets.compare_digest(credentials.credentials.encode(), expected.encode()):
        raise HTTPException(401, "管理员凭证无效", headers={"WWW-Authenticate": "Bearer"})

async def get_knowledge_owner(db: DbSession) -> User:
    # Keep the existing SQL and Qdrant owner filters; never accept an owner from a request.
    owner = await db.get(User, settings.knowledge_owner_id)
    if owner is not None:
        return owner
    if settings.knowledge_owner_id != DEFAULT_OWNER_ID:
        raise HTTPException(503, "配置的知识库所有者不存在，请检查 KNOWLEDGE_OWNER_ID。")
    # Conflict-safe for simultaneous first visits and multiple backend workers.
    await db.execute(insert(User).values(
        id=DEFAULT_OWNER_ID, username="__public_knowledge__",
        email="public-knowledge@localhost.invalid", password_hash="!disabled",
    ).on_conflict_do_nothing(index_elements=[User.id]))
    await db.commit()
    return await db.get(User, DEFAULT_OWNER_ID)

async def get_admin_owner(db: DbSession, _: Annotated[None, Depends(require_admin)]) -> User:
    return await get_knowledge_owner(db)

KnowledgeOwner = Annotated[User, Depends(get_knowledge_owner)]
AdminOwner = Annotated[User, Depends(get_admin_owner)]
