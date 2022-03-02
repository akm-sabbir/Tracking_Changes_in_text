from scispacy.candidate_generation import DEFAULT_PATHS, DEFAULT_KNOWLEDGE_BASES
from scispacy.candidate_generation import (
    LinkerPaths
)
from scispacy.linking_utils import KnowledgeBase
from scispacy.linking import *

CustomLinkerPaths_2021AB = LinkerPaths(
    ann_index="learning_outputs2/nmslib_index.bin",
    tfidf_vectorizer="learning_outputs2/tfidf_vectorizer.joblib",
    tfidf_vectors="learning_outputs2/tfidf_vectors_sparse.npz",
    concept_aliases_list="learning_outputs2/concept_aliases.json",
)


class UMLS2021KnowledgeBase(KnowledgeBase):
    def __init__(
            self,
            file_path: str = "umls2021AB.jsonl",
    ):
        super().__init__(file_path)


# Admittedly this is a bit of a hack, because we are mutating a global object.
# However, it's just a kind of registry, so maybe it's ok.
DEFAULT_PATHS["umls2021"] = CustomLinkerPaths_2021AB
DEFAULT_KNOWLEDGE_BASES["umls2021"] = UMLS2021KnowledgeBase
