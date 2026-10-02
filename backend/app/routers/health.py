from fastapi import APIRouter, Depends
from app.core.deps import require_admin

from app.core.config import settings
from app.services.llm_service import LlmService

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@router.get("/llm/status", dependencies=[Depends(require_admin)])
async def llm_status() -> dict[str, object]:
    status = LlmService.config_status()
    return {
        "configured": status.configured,
        "provider": status.provider,
        "model": status.model,
        "base_url_host": status.base_url_host,
        "missing": status.missing,
        "mode": "live" if status.configured else "placeholder",
    }
