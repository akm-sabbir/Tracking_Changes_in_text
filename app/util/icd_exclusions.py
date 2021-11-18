import os
import re


class ICDExclusions:
    def __init__(self, exclusions_json=None):
        #if exclusions_json is None:
        #    raise ValueError("exclusion list is None")
        self.exclusion_dictionary = exclusions_json

    # get the common substring between two codes
    # E001, E002 = E00
    def set_exclusion_dictionary(self, dic_: dict) -> None:
        if dic_ is None:
            raise ValueError("exclusion list is None")
        self.exclusion_dictionary = dic_

    def get_common_substring(self, string1, string2):
        common = os.path.commonprefix([string1, string2])
        return common

    # If E00 is common, get 2 from E002
    def get_trailing_number(self, code, prefix):
        if len(re.findall("[A-Za-z]+", code.replace(prefix, ''))) !=0:
            return 999999
        # invalid literals "1, 3"
        return int(code.replace(prefix, ''))

    # if range is E001-E007, then E002 is excluded but E009 is not
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
        
        #iterate over the list
        #find three classes
        # and check with target

        for item in exclusions:
            stubs = item.split('-')
            if (len(stubs) <= 1):
                return (stubs == target)
            elif not stubs[1]:
                return self.is_exlusion_after_range(stubs[0], target)
            else:
                return self.is_exlusion_in_range(stubs, target)

        return False
    # given a code, and a list of codes; return those that are mutually exclusive
    # 
    def get_excluded_list(self, source_code, codes_to_check_against):

        #trim source code to first three characters
        source_code = source_code[0:3]
        
        excluded = []
        if len(codes_to_check_against) == 0:
            return excluded
        # get lists
        exclusions = self.exclusion_dictionary.get(source_code)
        if exclusions is None:
            return excluded
        for code in codes_to_check_against:
            if self.is_excluded(exclusions, code):
                excluded.append(code)
        return excluded


