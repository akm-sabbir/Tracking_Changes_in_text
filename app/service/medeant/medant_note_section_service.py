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
    hpi_section_regex = r"(?<=HPI:).*?(?=ROS:)"
    exam_section_regex = r"(?<=exam:).*?((?=medication[^\w]*review[^\w]completed))|(?<=exam:).*?(?=\n{2})"

    medical_problems_regex = r"(medical[^\w]problems:).*?(?=\(accidents[^\w]*injuries\))"
    problems_list_regex = r"(problem[^\w]list:).*?(?=\(health[^\w]*maintenance\))"
    personal_habit_regex = r"(personal[^\w]habits:).*?(?=reviewed[^\w]*and[^\w]*updated)"

    session_notes_regex = r"(?<=session[^\w]notes:).*?(?=progress[^\w]notes)|(?<=session[^\w]notes:).*?(?=\n{2})"
    progress_notes_regex = r"(?<=progress[^\w]notes:).*?(?=progress[^\w]notes:\n|time[^\w]out:)|" \
                           r"(?<=progress[^\w]notes:).*?(?=\n{2})"
    __family_history_section_regex = r"(?<=fh:\n).*?(?=sh:|objective)|(?<=fh:\n).*?(?=\n{2})"

    CONSTANT_ENDINGS_PATTERN = [r'assessment', r'plan[^\w]other', r'lab[^\w]orders', r'correspond\'s',
                                r'follow[^\w]up', r'treatment[^\w]plan', r'resident[^\w]informed', r'referral']
    ending_pattern_for_med_new_section = CONSTANT_ENDINGS_PATTERN + [r'med[^\w]current']
    ending_pattern_for_med_current_section = CONSTANT_ENDINGS_PATTERN + [r'med[^\w]new']
    ending_pattern_for_med_discontinued_section = CONSTANT_ENDINGS_PATTERN
    ending_pattern_for_current_meds_prior_to_visit_section = [r'allergies', r'medication[^\w]reviewed']

    current_meds_prior_to_visit_section_regex = r"(?<=current[^\w]meds[^\w]prior[^\w]to[^\w]visit).*?(?=" + \
                                                r"|".join(ending_pattern_for_current_meds_prior_to_visit_section) + r")"
    med_new_section_regex = r"(?<=med[^\w]new[^\w]).*?(?=" + \
                            r"|".join(ending_pattern_for_med_new_section) + r")"
    med_current_section_regex = r"(?<=med[^\w]current[^\w]).*?(?=" + \
                                r"|".join(ending_pattern_for_med_current_section) + r")"

    def get_subjective_sections(self, note: str) -> List[Match]:

        matches = []

        medical_problems_patten = re.compile(self.medical_problems_regex, flags=re.DOTALL | re.IGNORECASE)
        problems_list_patten = re.compile(self.problems_list_regex, flags=re.DOTALL | re.IGNORECASE)
        personal_habit_patten = re.compile(self.personal_habit_regex, flags=re.DOTALL | re.IGNORECASE)
        hpi_section_patten = re.compile(self.hpi_section_regex, flags=re.DOTALL | re.IGNORECASE)

        hpi_section_sections = [section for section in hpi_section_patten.finditer(note)]
        medical_problems_sections = [section for section in medical_problems_patten.finditer(note)]
        problems_list_sections = [section for section in problems_list_patten.finditer(note)]
        personal_habit_sections = [section for section in personal_habit_patten.finditer(note)]

        matches.extend(medical_problems_sections+problems_list_sections+personal_habit_sections+hpi_section_sections)

        return matches

    def get_family_history_sections(self, note: str) -> List[FamilyHistorySection]:
        family_history_section_pattern = re.compile(self.__family_history_section_regex,
                                                    flags=re.DOTALL | re.IGNORECASE)

        return [FamilyHistorySection(section.start(), section.end()) for section in
                family_history_section_pattern.finditer(note)]

    def get_medication_sections(self, note: str) -> List[Match]:
        current_meds_prior_to_visit_section_pattern = re.compile(self.current_meds_prior_to_visit_section_regex,
                                                                 flags=re.DOTALL | re.IGNORECASE)
        med_new_section_patten = re.compile(self.med_new_section_regex, flags=re.DOTALL | re.IGNORECASE)
        med_current_section_pattern = re.compile(self.med_current_section_regex, flags=re.DOTALL | re.IGNORECASE)

        current_meds_prior_to_visit_sections = [section for section in
                                                current_meds_prior_to_visit_section_pattern.finditer(note)]
        med_new_sections = [section for section in med_new_section_patten.finditer(note)]
        med_current_sections = [section for section in med_current_section_pattern.finditer(note)]

        return current_meds_prior_to_visit_sections + med_new_sections + med_current_sections
