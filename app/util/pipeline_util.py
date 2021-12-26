from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation


class PipelineUtil:
    @staticmethod
    def track_changed_words(original_word, changed_word, start, end, annotation_results):
        annotation = ChangedWordAnnotation(changed_word, original_word, start, end)
        if changed_word in annotation_results["changed_words"]:
            annotation_results["changed_words"][changed_word].append(annotation)
        else:
            annotation_results["changed_words"][changed_word] = [annotation]
