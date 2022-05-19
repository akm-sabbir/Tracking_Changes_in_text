import pkg_resources
from symspellpy import SymSpell


class MedicalSpellCheckerServiceImpl:
    def __init__(self, edit_distance_max: int = 0, prefix_length: int = 7):
        self.dictionary_path = pkg_resources.resource_filename("symspellpy"
                                                               , "frequency_dictionary_en_82_765.txt")
        self.bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )

        self.sym_spell = SymSpell(edit_distance_max, prefix_length)
        self.sym_spell.load_dictionary(self.dictionary_path, 0, 1)
        self.sym_spell.load_bigram_dictionary(self.bigram_path, term_index=0, count_index=2)

    def get_corrected_text(self, sentence: str, max_edit_distance: int, transfer_casing: bool, ignore_non_words: bool,
                           split_by_space: bool, ignore_term_with_digits: bool) -> str:
        correct_text_suggested_results = self.sym_spell.lookup_compound(sentence,
                                                                        max_edit_distance=max_edit_distance,
                                                                        transfer_casing=transfer_casing,
                                                                        ignore_non_words=ignore_non_words,
                                                                        split_by_space=split_by_space,
                                                                        ignore_term_with_digits=ignore_term_with_digits)

        return sentence if not correct_text_suggested_results else correct_text_suggested_results[0].term
