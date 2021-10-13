from collections import Counter

def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

def anagram_indices(word, s):
    result = []
    for i in range(len(s) - len(word) + 1):
        window = s[i:i + len(word)]
        if is_anagram(window, word):
            result.append(i)
    return result
anagram_indices() 
