import re
from re import Match
from typing import List

from app.dto.pipeline.excluded_sections.family_history_excluded_section import FamilyHistorySection


class MedantNoteSectionService:

    """ These regex finds text between two sections, or up to the next two newlines
    e.g. subjective_section_regex - finds text between Subjective and Current Meds Prior to Visit
    If Current Meds Prior to Visit is absent, match text up to the next two newlines
    """

    subjective_section_regex = r"(?<=subjective\n).*?(?=current[^\w]*meds[^\w]*prior[^\w]*to[^\w]*visit)|" \
                               r"(?<=subjective\n).*?(?=\n{2})"
    exam_section_regex = r"(?<=exam:).*?((?=medication[^\w]*review[^\w]completed))|(?<=exam:).*?(?=\n{2})"
    session_notes_regex = r"(?<=session[^\w]notes:).*?(?=progress[^\w]notes)|(?<=session[^\w]notes:).*?(?=\n{2})"
    progress_notes_regex = r"(?<=progress[^\w]notes:).*?(?=progress[^\w]notes:\n|time[^\w]out:)|" \
                           r"(?<=progress[^\w]notes:).*?(?=\n{2})"
    __family_history_section_regex = r"(?<=fh:\n).*?(?=sh:|objective)|(?<=fh:\n).*?(?=\n{2})"

    def get_subjective_sections(self, note: str) -> List[Match]:
        subjective_section_patten = re.compile(self.subjective_section_regex, flags=re.DOTALL | re.IGNORECASE)
        exam_section_pattern = re.compile(self.exam_section_regex, flags=re.DOTALL | re.IGNORECASE)

        subjective_sections = [section for section in subjective_section_patten.finditer(note)]
        if subjective_sections:
            exam_sections = [section for section in exam_section_pattern.finditer(note)]
            return subjective_sections + exam_sections

        session_notes_section_patten = re.compile(self.session_notes_regex, flags=re.DOTALL | re.IGNORECASE)
        progress_notes_section_pattern = re.compile(self.progress_notes_regex, flags=re.DOTALL | re.IGNORECASE)

        session_notes_sections = [section for section in session_notes_section_patten.finditer(note)]

        if session_notes_sections:
            progress_notes_sections = [section for section in progress_notes_section_pattern.finditer(note)]
            return session_notes_sections + progress_notes_sections

        return []

    def get_family_history_sections(self, note: str) -> List[FamilyHistorySection]:
        family_history_section_pattern = re.compile(self.__family_history_section_regex, flags=re.DOTALL | re.IGNORECASE)

        return [FamilyHistorySection(section.start(), section.end()) for section in
                family_history_section_pattern.finditer(note)]
