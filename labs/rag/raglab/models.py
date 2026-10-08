"""Local, pinned model snapshots; no automatic downloads during serving."""
import json
from functools import lru_cache
import numpy as np
from .config import model_dir, DIMENSION

@lru_cache(maxsize=1)
def encoder():
    from sentence_transformers import SentenceTransformer
    path=model_dir()/'encoder'
    if not (path/'config.json').exists():
        raise RuntimeError('Run python -m raglab.prepare_models first')
    return SentenceTransformer(str(path), device='cpu', local_files_only=True, trust_remote_code=False)

@lru_cache(maxsize=1)
def cross_encoder():
    import torch
    from sentence_transformers import CrossEncoder
    path=model_dir()/'reranker'
    if not (path/'config.json').exists():
        raise RuntimeError('Run python -m raglab.prepare_models first')
    model = CrossEncoder(str(path), device='cpu', local_files_only=True, trust_remote_code=False)
    # On the validated macOS/torch 2.14.1 stack, a linear layer produced NaNs
    # with the loaded parameter storage but finite results with identical cloned
    # values. Materialize independent contiguous storage; see VALIDATION.md.
    with torch.no_grad():
        for parameter in model.model.parameters():
            parameter.data = parameter.detach().clone(memory_format=torch.contiguous_format)
    return model

def embed(texts):
    if not isinstance(texts,list) or any(not isinstance(t,str) or not t.strip() for t in texts):
        raise ValueError('texts must be a list of nonempty strings')
    if not texts:
        return np.empty((0,DIMENSION),dtype=np.float32)
    vectors=encoder().encode(texts,normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
    if vectors.shape!=(len(texts),DIMENSION) or not np.isfinite(vectors).all():
        raise ValueError('invalid model output')
    return vectors

def rerank(query, candidates, k=5):
    if not isinstance(query,str) or not query.strip() or type(k) is not int or not 1<=k<=20:
        raise ValueError('nonempty query and k in 1..20 required')
    if len(candidates)>100:
        raise ValueError('at most 100 candidates')
    if not candidates:
        return []
    scores=np.asarray(cross_encoder().predict([(query,c['text']) for c in candidates],show_progress_bar=False)).reshape(-1)
    if scores.size!=len(candidates) or not np.isfinite(scores).all():
        raise ValueError('invalid reranker output')
    rows=[dict(c,rerank_score=float(score)) for c,score in zip(candidates,scores)]
    return sorted(rows,key=lambda r:(-r['rerank_score'],r['chunk_id']))[:k]
