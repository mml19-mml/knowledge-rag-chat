"""Run before the first PDF upload: python scripts/prepare_local_model.py"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.config import settings
from app.rag.embedding import EmbeddingService

async def main():
    if settings.embedding_provider != "local":
        raise SystemExit("Set EMBEDDING_PROVIDER=local first")
    result = await EmbeddingService().embed_text("本地知识库模型准备完成。")
    print(f"Local model ready: {result.model}; dimension={len(result.vector)}; no API key used")

if __name__ == "__main__":
    asyncio.run(main())
