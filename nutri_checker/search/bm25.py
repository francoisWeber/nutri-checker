# mypy: ignore-errors
from typing import Any, List
import pandas as pd

import bm25s
from numpy.typing import NDArray
from Stemmer import Stemmer  # pylint: disable=E0611



class BM25Index:
    def __init__(self, stemmer: Stemmer | None = None) -> None:
        self.bm25 = bm25s.BM25()
        self.stemmer = stemmer if stemmer else Stemmer("french")

    def index(self, documents: List[str] | NDArray) -> None:
        tokenized_docs = bm25s.tokenize(documents, stemmer=self.stemmer)
        self.bm25.index(tokenized_docs)

    def retrieve(self, queries: List[str] | NDArray, corpus: List[Any] | None = None, k=100):
        tokenized_queries = bm25s.tokenize(queries, stemmer=self.stemmer)
        documents, scores = self.bm25.retrieve(tokenized_queries, corpus=corpus, k=k)
        return documents, scores
    

class NutriIndex:
    def __init__(self, nutridataset: pd.DataFrame):
        self.nutridataset = nutridataset
        self.bm25 = BM25Index()
        self.bm25.index(self.nutridataset["name_fr"].values)
        
    def retrieve(self, query: str | List[str], k=1):
        if isinstance(query, str):
            query = [query]
        docs, scores = self.bm25.retrieve(query, k=k)
        return self.nutridataset.loc[docs.ravel()]