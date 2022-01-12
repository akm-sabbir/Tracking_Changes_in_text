from negspacy.termsets import termset
from negspacy.negation import Negex
from negspacy import negation
import spacy
nlp = spacy.load("en_core_sci_sm")
ts = termset("en_clinical_sensitive")
ts.add_patterns({"preceding_negations": ["quit"]})
ruler = nlp.add_pipe("entity_ruler")
patterns = [{"label": "GPE", "pattern": "Smoke"},
            {"label": "GPE", "pattern": "Smoker"},
            {"label": "GPE", "pattern": [{"LOWER": "smoke"}]},
            {"label": "GPE", "pattern": [{"LOWER": "smoking"}]},
            {"label": "GPE", "pattern": [{"LOWER": "smokes"}]},
            {"label": "GPE", "pattern": "Smokes"},
            {"label": "GPE", "pattern": [{"LOWER": "tobacco"}]},
            {"label": "GPE", "pattern": "Tobacco"}

            ]
ruler.add_patterns(patterns)
nlp.add_pipe("negex", config={"chunk_prefix": ["never", "no", "stopped", "stops", "stop"]
    }
    )

doc = nlp("""patient stopped taking tobacco. patient stopped smoking. patient never smoke. patient quit smoking. 
patient does not smoke. no smoking.""")

for word in doc.doc.ents:
    print(word, word._.negex)
