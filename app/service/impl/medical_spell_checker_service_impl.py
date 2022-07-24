import os
from typing import List

import spacy
from medcat.cdb import CDB
from medcat.config import Config
from medcat.utils.normalizers import BasicSpellChecker
from medcat.vocab import Vocab

from zipfile import ZipFile

from app import app_base_path
from app.service.downloader.s3_downloader import S3DownloaderService
from app.service.spell_checker_service import SpellCheckerService
from app.util.config_manager import ConfigManager


class MedicalSpellCheckerServiceImpl(SpellCheckerService):
    def __init__(self, cdb_vocab: CDB, config: Config, data_vocab: Vocab):
        self.__model_name = ConfigManager.get_specific_config("scispacy_umls_model_name", "umls_model_name")

        self._medical_spell_checker = BasicSpellChecker(cdb_vocab.vocab, config, data_vocab.vocab)

        self.nlp = spacy.load(self.__model_name)

    def get_corrected_text(self, sentence: str) -> List[tuple]:

        spacy_doc = self.nlp(sentence)

        return [(token.text, self._medical_spell_checker.fix(token.lower_)) for token in spacy_doc]


if __name__ == '__main__':
    s3_downloader = S3DownloaderService()

    ConfigManager.initiate_config()

    DATA_DIR = os.path.join(os.path.dirname(app_base_path), "medcat_model")

    local_file_name = DATA_DIR + "/snomed_umls_modelpack.zip"

    local_file_folder = DATA_DIR + "/snomed_umls_modelpack"

    print(DATA_DIR)
    print(local_file_name)
    print(local_file_folder)

    if not os.path.exists(local_file_folder):
        print("Downloading")
        s3_downloader.download_from_s3(bucket="avicenna-medcat-assets",
                                       key="snomed_umls_modelpack.zip",
                                       local_file_name=local_file_name)
        print("Download ended.")

        with ZipFile(local_file_name, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(DATA_DIR)

    cdb = CDB.load(DATA_DIR + "/snomed_umls_modelpack/cdb.dat")
    vocab = Vocab.load(DATA_DIR + "/snomed_umls_modelpack/vocab.dat")
    config = Config.load(DATA_DIR + "/snomed_umls_modelpack/meta_Status/config.json")

    medical_spell_checker = MedicalSpellCheckerServiceImpl(cdb, config, vocab)

    sentence = "123 hert attack dibetes schzophrenia exacebation dpression hyprglycema sicle alchol disoder neplasm endocine geitourinary periatal recurent"


    result = medical_spell_checker.get_corrected_text(sentence)


    for res in result:
        print(res)
