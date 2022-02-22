import json
import re
import os


class ICDExclusions:
    def __init__(self, exclusions_json_dict=None):
        self.exclusion_dictionary = exclusions_json_dict
        self.icd10_regex = "[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}"
        self.regex = re.compile(self.icd10_regex)
        self.regex_words = re.compile("^[a-zA-Z]*$")

    # get the common substring between two codes
    # E001, E002 = E00

    def load_from_json(self):
        with open(self.exclusions_json) as json_file:
            self.exclusion_dictionary = json.load(json_file)

    def return_codes(self, code_or_word):
        code_or_words = code_or_word.split(' ')
        for each_data in code_or_words:
            each_data = each_data.replace('(', "")
            each_data = each_data.replace(')', "")
            each_data = each_data.replace(",", "")
            if len(re.findall(self.regex_words, each_data)) == 0:
                if 1 <= len(re.findall(self.regex, each_data)) <= 2:
                    yield each_data
        return

    def extract_codes(self):

        for key, value in self.exclusion_dictionary.items():
            list_of_codes = []
            for each_item in value:
                for each_code in self.return_codes(each_item):
                    list_of_codes.append(each_code)
            if(len(list_of_codes) != 0):
                print(each_item + ", extracted codes" + str(list_of_codes))
            self.exclusion_dictionary[key] = list_of_codes
        with open("exclusions_updated.json", "w") as outfile:
            json.dump(self.exclusion_dictionary, outfile)

    def get_common_substring(self, string1, string2):
        common = os.path.commonprefix([string1, string2])
        return common

    # If E00 is common, get 2 from E002
    def get_trailing_number(self, code, prefix):
        return int(code.replace(prefix, ''))

    # if range is E001-E007, then E002 is excluded but E009101 is not
    def is_in_range(self, range_code, target):
        if range_code[0] <= target and range_code[1] >= target:
            return True
        return False

    def is_exlusion_in_range(self, both, target):
        left = both[0]
        right = both[1]
        common_prefix = self.get_common_substring(left, right)

        if not target.startswith(common_prefix):
            return False

        start_integer = self.get_trailing_number(left, common_prefix)
        end_integer = self.get_trailing_number(right, common_prefix)
        target_integer = self.get_trailing_number(target, common_prefix)
        if target_integer >= start_integer and target_integer <= end_integer:
            return True
        else:
            return False

    # case of whether E0052 is excluded by E005
    def is_exlusion_after_range(self, left, target):
        if target.startswith(left) or left.startswith(target):
            return True
        else:
            return False

    # check against three kinds of exclusion representation
    def is_excluded(self, exclusions, target):

        # iterate over the list
        # find three classes
        # and check with target
        for item in exclusions:
            stubs = item.split('-')
            if (len(stubs) <= 1):
                return (stubs == target)
            elif not stubs[1]:
                return self.is_exlusion_after_range(stubs[0], target)
            else:
                return self.is_exlusion_in_range(stubs, target)

    # given a code, and a list of codes; return those that are mutually exclusive

    def is_excluded_updated(self, item, target):
        if item.find('-') == -1:
            return item == target
        if item[-1] == '-':
            range_ = item[:-1].split('-')
            if len(range_) == 1:
                return os.path.commonprefix([range_[0], target]) == range_[0]
            if range_[0] <= target <= range_[1]:
                return True
            return os.path.commonprefix([range_[1], target]) == range_[1]
        range_ = item.split('-')
        return range_[0] <= target <= range_[1]

    def preprocess_code(self, source_code: str):
        source_code = source_code.replace(".", "")

        return source_code

    def get_exclusion_decision(self, source_code: str, target_code_to_check: str) -> bool:
        exclusion_list = self.exclusion_dictionary.get(target_code_to_check)
        return

    def get_excluded_list(self, source_code, codes_to_check_against):

        # trim source code to first three characters

        excluded = []
        source_code = source_code.replace(".", "")
        if len(codes_to_check_against) == 0:
            return excluded
        exclusions = self.exclusion_dictionary.get(source_code)
        for code in codes_to_check_against:
            for each_exclusion_code in exclusions:
                if self.is_excluded_updated(each_exclusion_code, code.replace(".", "")) is True:
                    excluded.append(code)
                    break
        return excluded