from negspacy.termsets import termset
from negspacy import negation
from negspacy.negation import Negex
import spacy


class SmokerUtility:
    nlp = spacy.load("en_core_sci_sm")
    ts = termset("en_clinical_sensitive")
    ts.add_patterns({"preceding_negations": ["quit", "former"]})
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [{"label": "GPE", "pattern": "Smoke"},
                {"label": "GPE", "pattern": "Smoker"},
                {"label": "GPE", "pattern": [{"LOWER": "smoke"}]},
                {"label": "GPE", "pattern": [{"LOWER": "smoking"}]},
                {"label": "GPE", "pattern": [{"LOWER": "smokes"}]},
                {"label": "GPE", "pattern": [{"LOWER": "smoker"}]},
                {"label": "GPE", "pattern": [{"LOWER": "smokers"}]},
                {"label": "GPE", "pattern": [{"LOWER": "smoked"}]},
                {"label": "GPE", "pattern": "Smokes"},
                {"label": "GPE", "pattern": [{"LOWER": "tobacco"}]},
                {"label": "GPE", "pattern": "Tobacco"}]

    ruler.add_patterns(patterns)
    nlp.add_pipe("negex", config={"chunk_prefix": ["never", "no", "stopped", "stops", "stop", "former"],
                                  "neg_termset": ts.get_patterns()})

    @staticmethod
    def get_nlp_obs() -> spacy.Language:
        return SmokerUtility.nlp

