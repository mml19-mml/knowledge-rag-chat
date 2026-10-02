"""CPU-only, cached multilingual embeddings. No paid API or remote code execution."""
from functools import lru_cache
from threading import Lock
from pathlib import Path
import os

_lock = Lock()


@lru_cache(maxsize=1)
def _load_model(name: str, cache_dir: str, offline: bool):
    os.environ.setdefault("HF_HOME", str(Path(cache_dir).resolve() / "huggingface"))
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name, device="cpu", cache_folder=cache_dir,
                               local_files_only=offline, trust_remote_code=False)


def encode_local(name: str, cache_dir: str, offline: bool,
                 texts: list[str], dimension: int) -> list[list[float]]:
    import numpy as np
    # Serialize initialization/inference; the async caller moves this CPU work off the event loop.
    with _lock:
        model = _load_model(name, cache_dir, offline)
        if model.get_sentence_embedding_dimension() != dimension:
            raise ValueError("EMBEDDING_DIMENSION differs from local model output")
        tokenizer = model.tokenizer
        window_size = max(1, model.max_seq_length - tokenizer.num_special_tokens_to_add())
        output = []
        for text in texts:
            # Original PDF chunks may exceed the model context. Pool every token window,
            # instead of silently discarding the remainder of a paragraph.
            ids = tokenizer.encode(text, add_special_tokens=False, truncation=False)
            windows = [ids[i:i + window_size] for i in range(0, len(ids), window_size)]
            if not windows:
                raise ValueError("Text has no tokens")
            pieces = [tokenizer.decode(w, skip_special_tokens=True) for w in windows]
            vectors = model.encode(pieces, batch_size=16, convert_to_numpy=True,
                                   normalize_embeddings=True, show_progress_bar=False)
            vector = np.average(vectors, axis=0, weights=[len(w) for w in windows])
            norm = np.linalg.norm(vector)
            if not np.isfinite(vector).all() or not np.isfinite(norm) or norm == 0:
                raise ValueError("Invalid local embedding")
            output.append((vector / norm).astype(float).tolist())
        return output
