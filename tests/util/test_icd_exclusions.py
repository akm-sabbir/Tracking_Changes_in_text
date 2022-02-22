import unittest
import collections
from app.util.icd_exclusions import ICDExclusions


class TestICDExclusions(unittest.TestCase):

    def setUp(self):
        self.icd_exclusions = ICDExclusions()

    def test_get_common_substring(self):
        self.assertEqual(self.icd_exclusions.get_common_substring('E00', 'E05'),'E0', 'Should be E0')

    def test_get_trailing_number(self):
        self.assertEqual(self.icd_exclusions.get_trailing_number('E00', 'E0'), 0, 'Should be 0')
        self.assertEqual(self.icd_exclusions.get_trailing_number('E01', 'E0'), 1, 'Should be 1')
        self.assertEqual(self.icd_exclusions.get_trailing_number('E052', 'E05'), 2, 'Should be 2')

    def test_is_exlusion_in_range(self):
        both = []
        both.append('E001')
        both.append('E005')
        self.assertTrue(self.icd_exclusions.is_exlusion_in_range(both, 'E004'), 'Should be in target')
        self.assertFalse(self.icd_exclusions.is_exlusion_in_range(both, 'E006'), 'Should not be in target')
        self.assertFalse(self.icd_exclusions.is_exlusion_in_range(both, 'F99'), 'Should not be in target')

    def test_is_exlusion_after_range(self):
        left = 'E005'
        target1 = 'E0056'
        target2 = 'E006'
        self.assertTrue(self.icd_exclusions.is_exlusion_after_range(left, target1), 'Should be True')
        self.assertFalse(self.icd_exclusions.is_exlusion_after_range(left, target2), 'Should be False')

    def test_is_excluded(self):
        exclusions = []
        exclusions.append('E00-E02-')
        exclusions.append('E00')
        exclusions.append('E30-')
        self.assertTrue(self.icd_exclusions.is_excluded_updated(exclusions[2], 'E301'), 'Should be excluded')

    def test_get_excluded_list(self):
        code = 'A05'
        codes = ['E00', 'E01', 'F89', 'A041', 'A0475', 'A3201', 'A3202']
        actual_excluded_codes = ['A041', 'A0475', 'A3201', 'A3202']
        self.icd_exclusions.exclusion_dictionary = {"A05":["A02-", "T61-T62", "A040-A044", "A047-", "A32-"]}
        extracted_excluded_codes = self.icd_exclusions.get_excluded_list(code, codes)
        self.assertTrue(collections.Counter(actual_excluded_codes) == collections.Counter(extracted_excluded_codes),
                        'Should be equal')


if __name__ == '__main__':
    unittest.main()