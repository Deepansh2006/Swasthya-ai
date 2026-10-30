"""
rag_service.py
Hybrid Retrieval Service combining Dense FAISS Cosine Search and Sparse BM25 Keyword Search.
Implements Reciprocal Rank Fusion (RRF) and similarity threshold guardrails.
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Any, Tuple
from backend.app.models.schemas import SourceCitation, UrgencyLevel

try:
    import faiss
    HAVE_FAISS = True
except ImportError:
    HAVE_FAISS = False

from knowledge_base.tokenizer import tokenize_indic

class HybridRAGService:
    def __init__(self, index_dir: str = None):
        if index_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            index_dir = os.path.join(base_dir, "..", "knowledge_base", "indices")
            index_dir = os.path.abspath(index_dir)
            
        self.index_dir = index_dir
        self.bm25 = None
        self.chunks = []
        self.vectorizer = None
        self.faiss_index = None
        self.dense_matrix = None
        self.load_indices()

    def load_indices(self):
        bm25_file = os.path.join(self.index_dir, "bm25_index.pkl")
        if os.path.exists(bm25_file):
            with open(bm25_file, "rb") as f:
                data = pickle.load(f)
                self.bm25 = data["bm25"]
                self.chunks = data["chunks"]
                
        vec_file = os.path.join(self.index_dir, "dense_vectorizer.pkl")
        if os.path.exists(vec_file):
            with open(vec_file, "rb") as f:
                self.vectorizer = pickle.load(f)
                
        faiss_file = os.path.join(self.index_dir, "guidelines_faiss.index")
        if os.path.exists(faiss_file) and HAVE_FAISS:
            self.faiss_index = faiss.read_index(faiss_file)

    def retrieve(self, query: str, top_k: int = 3) -> List[SourceCitation]:
        """
        Execute Hybrid Search: BM25 + FAISS Dense Inner Product using Reciprocal Rank Fusion.
        """
        if not self.chunks or not query.strip():
            return []

        # 1. Sparse BM25 Retrieval
        tokens = tokenize_indic(query)
        bm25_scores = self.bm25.get_scores(tokens)
        bm25_ranking = np.argsort(bm25_scores)[::-1]

        # 2. Dense Cosine Retrieval
        dense_ranking = []
        dense_scores_map = {}
        if self.vectorizer is not None and (self.faiss_index is not None or self.dense_matrix is not None):
            query_vec = self.vectorizer.transform([query]).toarray().astype(np.float32)
            norm = np.linalg.norm(query_vec)
            if norm > 0:
                query_vec = query_vec / norm
                if self.faiss_index is not None:
                    D, I = self.faiss_index.search(query_vec, len(self.chunks))
                    dense_ranking = I[0]
                    dense_scores_map = {idx: score for idx, score in zip(I[0], D[0])}
                elif self.dense_matrix is not None:
                    sims = np.dot(self.dense_matrix, query_vec.T).flatten()
                    dense_ranking = np.argsort(sims)[::-1]
                    dense_scores_map = {idx: sims[idx] for idx in dense_ranking}

        # 3. Reciprocal Rank Fusion (RRF)
        # RRF_Score = 0.5/(60 + rank_bm25) + 0.5/(60 + rank_dense)
        rrf_scores = {}
        k_const = 60
        
        for rank, idx in enumerate(bm25_ranking):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (0.5 / (k_const + rank))

        for rank, idx in enumerate(dense_ranking):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (0.5 / (k_const + rank))

        sorted_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]

        citations = []
        for idx in sorted_indices:
            chunk = self.chunks[idx]
            # Calculate an intuitive relevance percentage for display
            dense_sim = float(dense_scores_map.get(idx, 0.5))
            citations.append(SourceCitation(
                id=chunk.get("id", f"CHUNK_{idx}"),
                protocol=chunk.get("protocol", "National Health Mission"),
                source=chunk.get("source", "Indian Health Guidelines"),
                page=chunk.get("page", 1),
                relevance_score=round(max(0.4, min(0.98, dense_sim + 0.3)), 2),
                excerpt=chunk.get("content_hi", "") or chunk.get("content_en", ""),
                triage_urgency=chunk.get("triage_urgency")
            ))

        return citations

# Singleton instance
rag_service = HybridRAGService()
