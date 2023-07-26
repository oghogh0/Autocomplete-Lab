"""
6.1010 Spring '23 Lab 9: Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("key not a string")

        if len(key) == 0:
            self.value = value
        elif key[0] not in self.children:
            self.children[key[0]] = PrefixTree()
            self.children[key[0]].__setitem__(key[1:], value)
        elif key[0] in self.children:
            self.children[key[0]].__setitem__(key[1:], value)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("key not a string")

        if len(key) == 0:
            if self.value is None:
                raise KeyError("key not in the prefix tree")
            return self.value
        else:
            return self.children[key[0]].__getitem__(key[1:])

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("key not a string")
        if key:  # if key not empty string
            del self.children[key[0]][key[1:]]  # raises error e.g. if 'f' not in dict
        else:
            if self.value is None:  # word doesn't exist in tree
                raise KeyError("key not in the prefix tree")  # e.g. 'ba'
            else:  # if value in node
                self.value = None

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError("key not a string")
        try:
            self[key]  # getitem
            return True
        except:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        if self.value is not None:
            yield ("", self.value)  # until finds value

        for letter, prefxtree in self.children.items():  # letter is key
            for key, value in prefxtree.__iter__():
                yield (letter + key, value)


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    sentences = tokenize_sentences(text)  # splits into sentences

    freq_dict = {}

    for sentence in sentences:
        for word in sentence.split():
            if word not in freq_dict:  # nodes included in setitem
                freq_dict[word] = 0
            freq_dict[word] += 1

    tree = PrefixTree()
    for word in freq_dict:
        tree[word] = freq_dict[word]
    return tree


def subtree(tree, prefix):
    """
    Given tree, return subtree with prefix
    """
    if not prefix:
        return tree
    else:
        if prefix[0] not in tree.children:
            return None
        return subtree(tree.children[prefix[0]], prefix[1:])


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if not isinstance(prefix, str):
        raise TypeError("key not a string")

    most_freq_elem = []
    if subtree(tree, prefix) is None:  # prefix doesn't exist
        return []

    tree_list = list(subtree(tree, prefix))
    tree_list.sort(
        key=lambda x: x[1], reverse=True
    )  # mutates object, returns none, sorts tree based on min value have to rev

    if max_count is not None and max_count < len(
        tree_list
    ):  # max_count is less than list len
        tree_list = tree_list[:max_count]

    count = 0
    for word, freq in tree_list:  # (word,freq)
        most_freq_elem.append(prefix + word)  # add prefix back to word
        count += 1
        if max_count == None:
            continue
        elif count == max_count:
            return most_freq_elem

    return most_freq_elem


# edits
alphabet = "abcdefghijklmnopqrstuvwxyz"


def insertion(tree, prefix):
    """
    Given a prefix, return a list of all valid words
    after inserting a letter from alphabet
    """
    valid_words = set()

    for letter in alphabet:
        for i in range(len(prefix) + 1):
            new_word = prefix[:i] + letter + prefix[i:]
            if new_word in tree:
                valid_words.add((new_word, tree[new_word]))

    return valid_words


def deletion(tree, prefix):
    """
    Given a prefix, return a list of all valid words
    after deleting a letter from prefix
    """
    valid_words = set()

    for i in range(len(prefix)):
        new_word = prefix[:i] + prefix[i + 1 :]
        if new_word in tree:
            valid_words.add((new_word, tree[new_word]))

    return valid_words


def replacement(tree, prefix):
    """
    Given a prefix, return a list of all valid words
    after replacing a letter from prefix with letter in alphabet
    """
    valid_words = set()

    for letter in alphabet:
        for i in range(len(prefix)):
            new_word = prefix[:i] + letter + prefix[i + 1 :]
            if new_word in tree:
                valid_words.add((new_word, tree[new_word]))

    return valid_words


def transpose(tree, prefix):
    """
    Given a prefix, return a list of all valid words
    after transposing adjacent letters in prefix
    """

    valid_words = set()

    for i in range(len(prefix) - 1):
        new_word = prefix[:i] + prefix[i + 1] + prefix[i] + prefix[i + 2 :]
        if new_word in tree:
            valid_words.add((new_word, tree[new_word]))

    return valid_words


def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    output = autocomplete(tree, prefix, max_count)

    if len(output) != max_count:
        all_words = list(
            insertion(tree, prefix)
            | deletion(tree, prefix)
            | replacement(tree, prefix)
            | transpose(tree, prefix)
        )

        all_words.sort(key=lambda x: x[1], reverse=True)
        for word, freq in all_words:
            if len(output) != max_count and word not in output:  # account for dups
                output.append(word)
    return output


def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    # base case - empty string
    if pattern == "":
        if tree.value is not None:
            return [(pattern, tree.value)]
        else:
            return []  # if doesn't exist -> empty list


    # ? case
    if pattern[0] == "?":
        all_children = []
        for child in tree.children:  # loop over children
            add_on = word_filter(
                tree.children[child], pattern[1:]
            )  # call recursion on each child
            all_children.extend(word_filter_help(child, add_on))
        return all_children
    # * case
    if pattern[0] == "*":
        cases = set()

        case1 = word_filter(tree, pattern[1:])
        if case1 is not None:
            for word, freq in case1:
                cases.add((word, freq))

        for child in tree.children:  # loop over children
            case3 = word_filter(tree.children[child], pattern)
            cases.update(set(word_filter_help(child, case3)))

        return list(cases)
    # letter case
    if pattern[0] in alphabet:
        if pattern[0] in tree.children:
            all_words = set()
            suffix_list = word_filter(tree.children[pattern[0]], pattern[1:])

            if suffix_list is not None:
                for word, value in suffix_list:
                    all_words.add((pattern[0] + word, value))
            return list(all_words)


def word_filter_help(start_letter, words):
    """
    Given a letter and list of tuples,
    add letter at start of words[0]
    """
    all_children = []
    for word, freq in words:
        all_children.append((start_letter + word, freq))
    return all_children


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    doctest.testmod()
    tree = PrefixTree()
    tree["bar"] = 1
    tree["bat"] = 2
    tree["bark"] = 1

    # print(word_filter(tree,"*ing"))

    # t = word_frequencies("man mat mattress map me met a man a a a map man met")
    # print(t)
