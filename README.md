<h1>Autocomplete Lab</h1>
<h2>Description</h2>
In this lab, I develop a PrefixTree and implement different functions to find possible words in the tree. <br/> 
 

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>


<p align="left">
PREFIX tree:<br/>
The 'PrefixTree' class has methods to add a key with the given value to the prefix tree or reassign the associated value if it is already present, return the value for a specified prefix, delete the given key from the prefix tree if it exists, returns a boolean value if a key is in the prefix tree, and generates (key, value) pairs for all keys/values in this prefix tree and its children (this is a generator). <br/>


        class PrefixTree:
            def __init__(self):
                self.value = None
                self.children = {}
        
            def __setitem__(self, key, value):
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
                if not isinstance(key, str):
                    raise TypeError("key not a string")
        
                if len(key) == 0:
                    if self.value is None:
                        raise KeyError("key not in the prefix tree")
                    return self.value
                else:
                    return self.children[key[0]].__getitem__(key[1:])

            def __delitem__(self, key):
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
                if not isinstance(key, str):
                    raise TypeError("key not a string")
                try:
                    self[key]  # getitem
                    return True
                except:
                    return False
        
            def __iter__(self):
                if self.value is not None:
                    yield ("", self.value)  # until finds value
        
                for letter, prefxtree in self.children.items():  # letter is key
                    for key, value in prefxtree.__iter__():
                        yield (letter + key, value)
<br/>
<p align="left">
AUTOCOMPLETE engine:<br/>
In this section, I implement the autocomplete engine. To this end, I have built up a particular kind of prefix tree based on a piece of text: a frequency prefix tree, whose keys are words and values are the numbers of times that those words occur in the given text.<br/>

The 'word_frequencies' function takes in a string containing a body of text and returns a PrefixTree instance mapping words in the text to the frequency with which they occur in the given piece of text. A method has been provided called tokenize_sentences which will try to intelligently split a piece of text into individual sentences. It takes in a single string and returns a list of sentence strings. Each sentence string has had its punctuation removed, leaving only the words. Words within the sentence strings are sequences of characters separated by spaces.<br/>

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
<br/>
<br/>
<br/>
The 'autocomplete' function returns the list of the most-frequently-occurring elements that start with the given prefix.  It includes only the top max_count elements if max_count is specified, otherwise returns all. In the case of a tie, it outputs any of the most-frequently-occurring keys. If there are fewer than max_count valid keys available starting with prefix, it returns only as many as there are. The returned list can be in any order.<br/>

For example: autocomplete(t, "ba", 1) → [“bat”] because it occurs most, autocomplete(t, "ba", 2) → [“bat”,”bark”] or [“bat”,”bar”] because bat occurs most, then bark & bar tied in 2nd.<br/>

The code as follows:<br/>

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

<br/>
HELPER FUNCTION:<br/>
-subtree: given a tree, return subtree with the given prefix.<br/>
        
            if not prefix:
                return tree
            else:
                if prefix[0] not in tree.children:
                    return None
                return subtree(tree.children[prefix[0]], prefix[1:])

<br/>
<p align="left">
AUTOCORRECT:<br/>
For some words, the autocomplete implementation generates very few or no suggestions. In cases such as these, we may want to guess that the user mistyped something in the original word. Here, I have implemented a more sophisticated tool: autocorrect. This function returns a list of up to max_count words. It invokes autocomplete but, if fewer than max_count completions are made, it suggests additional words by applying one valid edit to the prefix. An edit for a word can be any one of the following:<br/>
        
-A single-character insertion (adds any one character in the range "a" to "z" at any place in the word).<br/>

            #alphabet = "abcdefghijklmnopqrstuvwxyz"
            valid_words = set()
        
            for letter in alphabet:
                for i in range(len(prefix) + 1):
                    new_word = prefix[:i] + letter + prefix[i:]
                    if new_word in tree:
                        valid_words.add((new_word, tree[new_word]))
        
            return valid_words
<br/>
-A single-character deletion (removes any one character from the word).<br/>

            #alphabet = "abcdefghijklmnopqrstuvwxyz"
            valid_words = set()
        
            for i in range(len(prefix)):
                new_word = prefix[:i] + prefix[i + 1 :]
                if new_word in tree:
                    valid_words.add((new_word, tree[new_word]))
        
            return valid_words

<br/>
-A single-character replacement (replaces any one character in the word with a character in the range a-z).<br/>

            #alphabet = "abcdefghijklmnopqrstuvwxyz"
            valid_words = set()
        
            for letter in alphabet:
                for i in range(len(prefix)):
                    new_word = prefix[:i] + letter + prefix[i + 1 :]
                    if new_word in tree:
                        valid_words.add((new_word, tree[new_word]))
        
            return valid_words
<br/>
-A two-character transpose (switches the positions of any two adjacent characters in the word).<br/>

            #alphabet = "abcdefghijklmnopqrstuvwxyz"
            valid_words = set()
        
            for i in range(len(prefix) - 1):
                new_word = prefix[:i] + prefix[i + 1] + prefix[i] + prefix[i + 2 :]
                if new_word in tree:
                    valid_words.add((new_word, tree[new_word]))
        
            return valid_words
<br/>

A valid edit is an edit that results in a word in the prefix tree without considering any suffix characters. In other words, we don't try to autocomplete valid edits, we just check whether the edit exists in the prefix tree. For example, editing "te" to "the" is valid, but editing "te" to "tze" is not, as "tze" isn't a word. Likewise, editing "phe" to "the" is valid, but "phe" to "pho" is not because "pho" is not a word in the corpus, although many words beginning with "pho" are. <br/>

In summary, given a prefix that produces C completions, where C<max_count, generate up to max_count−C additional words by considering all valid single edits of that prefix (i.e., corpus words that can be generated by 1 edit of the original prefix) and selecting the most-frequently-occurring edited words. It returns a list of suggestions produced by including all C of the completions and up to max_count−C of the most-frequently-occuring valid edits of the prefix; the list may be in any order. Importantly, it does not repeat suggested words. If max_count is None (or is unspecified), autocorrect returns all autocompletions as well as all valid edits. For example:<br/>

autocorrect(t, "bar", 3) returns ['bar', 'bark', 'bat'] since "bar" and "bark" are found by autocomplete and "bat" is valid edit involving a single-character replacement, i.e., "t" is replacing the "r" in "bar". <br/>

The code is as follows: <br/> 

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
<br/>
<p align="left">
FILTERING words:<br/>
It's sometimes useful to select only the words from a corpus that match a pattern. That's the purpose of the word_filter method. This function returns a list of (word, freq) tuples for those words whose characters match those of the given pattern. The characters in pattern are matched one-at-a-time with the characters in each word stored in the prefix tree. If all the characters in a particular word are matched, the (word, freq) pair is included in the list to be returned. The list can be in any order. The characters in pattern are interpreted as follows:<br/>
-'?' matches the next unmatched character in word no matter what it is.<br/>
-'*' matches a sequence of zero or more of the next unmatched characters in word.<br/>
-Otherwise the character in the pattern must exactly match the next unmatched character in the word.<br/>

Note that the characters replaced by * and ? can be arbitrary characters, not just letters. Pattern examples:<br/>
-"year" only matches "year".<br/>
-"year?" matches "years" and "yearn" (but not longer words).<br/>
-"???" matches all 3-letter words.<br/>
-"?ing" matches all 4-letter words ending in "ing.".<br/>
-"*ing" matches all words ending in "ing.".<br/>
-"?*ing" matches all words with 4 or more letters that end in "ing.".<br/>
-"*a*t" matches all words that contain an "a" and end in "t." e.g. "at", "art", "saint", and "what.".<br/>
-"year*" would match "year," "years," and "yearn," among others (as well as longer words like "yearning").<br/>

Filter examples:<br/>
-word_filter(t, "bat") returns [('bat', 2)].<br/>
-word_filter(t, "ba?") returns [('bat', 2), ('bar', 1)], i.e., listing all the 3-letter words in the prefix tree that begin with "ba".<br/>
-word_filter(t, "???") returns [('bat', 2), ('bar', 1)], i.e., listing all the 3-letter words in the prefix tree.<br/>
-word_filter(t, "*") returns [('bat', 2), ('bar', 1), ('bark', 1)], i.e., listing all the words in the prefix tree.<br/>
-word_filter(t, "*r*") returns [('bar', 1), ('bark', 1)], i.e., listing every word containing an "r" in any position.<br/>

The matching operation can be implemented as a recursive search function that attempts to match the next character in the pattern with some number of characters at the beginning of the word, then recursively matches the remaining characters in the pattern with remaining unmatched characters in the word. <br/>

The word_filter code is as follows: <br/>

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

<br/>
HELPER FUNCTION:<br/>
-word_filter_help: given a letter and list of tuples (word, freq), it adds the letter at start of each word.

            all_children = []
            for word, freq in words:
                all_children.append((start_letter + word, freq))
            return all_children
