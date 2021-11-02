from app.dto.core.trie_structure import Trie


class EnglishDictionary(object):

    def insert_in(self, word, trie, value=None, index=0):
        if index == len(word) - 1:
            if trie.current_elem.get(word[index]) is not None:
                trie.current_elem[word[index]].is_word = True
                trie.current_elem[word[index]].word = word[index]
                if len(trie.current_elem[word[index]].current_elem) == 0:
                    trie.current_elem[word[index]].is_leaf = True
            else:
                trie.current_elem[word[index]] = Trie()
                trie.current_elem[word[index]].is_word = True
                trie.current_elem[word[index]].is_leaf = True
                trie.current_elem[word[index]].word = word[index]
            trie.current_elem[word[index]].unicode_point = ord(word[index])
            return index
        else:
            if trie.current_elem.get(word[index]) is None:
                trie.current_elem[word[index]] = Trie()
                trie.current_elem[word[index]].is_word = False
                trie.current_elem[word[index]].is_leaf = False
                trie.current_elem[word[index]].word = word[index]
                trie.current_elem[word[index]].unicode_point = ord(word[index])
        index = self.insert_in(word, trie.current_elem[word[index]], value=value, index=index + 1)
        return index

    def is_valid_word(self, word, trie, index):
        if index == len(word):
            if trie.is_word is True:
                return True
            else:
                return False
        if trie.current_elem.get(word[index]) is None:
            return False
        return self.is_valid_word(word, trie.current_elem[word[index]], index + 1)
