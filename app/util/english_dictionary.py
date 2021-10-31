from app.util.trie_structure import Trie


class EnglishDictionary():

    def insert_in(self, word, trie, value=None, index=0):
        if index == len(word) - 1:
            if trie.current_elem.get(word[index]) is not None:
                trie.current_elem[word[index]].isWord = True
                trie.current_elem[word[index]].word = word[index]
                if len(trie.current_elem[word[index]].current_elem) == 0:
                    trie.current_elem[word[index]].isLeaf = True
            else:
                trie.current_elem[word[index]] = Trie()
                trie.current_elem[word[index]].isWord = True
                trie.current_elem[word[index]].isLeaf = True
                trie.current_elem[word[index]].word = word[index]
            trie.current_elem[word[index]].unicodePoint = ord(word[index])
            return
        else:
            if trie.current_elem.get(word[index]) is None:
                trie.current_elem[word[index]] = Trie()
                trie.current_elem[word[index]].isWord = False
                trie.current_elem[word[index]].isLeaf = False
                trie.current_elem[word[index]].word = word[index]
                trie.current_elem[word[index]].unicodePoint = ord(word[index])
        self.insert_in(word, trie.current_elem[word[index]], value=value, index=index + 1)
        return

    def is_valid_word(self, word, trie, index):
        if index == len(word):
            if trie.isWord is True:
                return True
            else:
                return False
        if trie.current_elem[word[index]] is None:
            return False
        return self.is_valid_word(word, trie.current_elem[word[index]], index + 1)
