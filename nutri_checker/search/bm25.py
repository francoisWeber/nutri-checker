# mypy: ignore-errors
from typing import Any, List
import pandas as pd

import bm25s
from numpy.typing import NDArray
import re
from Stemmer import Stemmer  # pylint: disable=E0611



class BM25Index:
    def __init__(self, stemmer: Stemmer | None = None, n_grams: int = 0) -> None:
        self.bm25 = bm25s.BM25()
        self.stemmer = stemmer if stemmer else Stemmer("french")
        self.token_pattern = r'(?=({}))'.format("."*n_grams) if n_grams else None

    def index(self, documents: List[str] | NDArray) -> None:
        tokenized_docs = bm25s.tokenize(documents, stemmer=self.stemmer, lower=True, token_pattern=self.token_pattern)
        self.bm25.index(tokenized_docs)

    def retrieve(self, queries: List[str] | NDArray, corpus: List[Any] | None = None, k=100):
        tokenized_queries = bm25s.tokenize(queries, stemmer=self.stemmer, lower=True, token_pattern=self.token_pattern)
        documents, scores = self.bm25.retrieve(tokenized_queries, corpus=corpus, k=k)
        return documents, scores
    

class NutriIndex:
    def __init__(self, nutridataset: pd.DataFrame, n_grams=2):
        self.nutridataset = nutridataset
        self.bm25 = BM25Index(n_grams=n_grams)
        self.bm25.index(self.nutridataset["name_fr"].values)
        
    def retrieve(self, query: str | List[str], k=1):
        if isinstance(query, str):
            query = [query]
        docs, _ = self.bm25.retrieve(query, k=k)
        return self.nutridataset.loc[docs.ravel()]