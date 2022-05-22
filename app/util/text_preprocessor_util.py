class TextPreProcessorUtil:
    @staticmethod
    def get_preprocessed_text(text: str) -> str:
        if text[-1].isalnum():
            return text + ","

        return text
