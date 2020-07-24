from __future__ import absolute_import
from __future__ import print_function
import re
import operator
import six
from collections import Counter

debug = False
test = False


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    splitter = re.compile('[^a-zA-Z0-9_[+][-]/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    sentence_delimiters = re.compile(u'[\\[\\]\n.!?,;:\t\\-\\"\\(\\)\\\'\u2019\u2013]')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_list):
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = '\\b' + word + '\\b'
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


#
# Function that extracts the adjoined candidates from a list of sentences and filters them by frequency
#
def extract_adjoined_candidates(sentence_list, stoplist, min_keywords, max_keywords, min_freq):
    adjoined_candidates = []
    for s in sentence_list:
        # Extracts the candidates from each single sentence and adds them to the list
        adjoined_candidates += adjoined_candidates_from_sentence(s, stoplist, min_keywords, max_keywords)
    # Filters the candidates and returns them
    return filter_adjoined_candidates(adjoined_candidates, min_freq)


# return adjoined_candidates

#
# Function that extracts the adjoined candidates from a single sentence
#
def adjoined_candidates_from_sentence(s, stop_list, min_keywords, max_keywords):
    candidates = []
    sl = s.lower().split()
    # For each possible length of the adjoined candidate
    for num_keywords in range(min_keywords, max_keywords + 1):
        # Until the third-last word
        for i in range(0, len(sl) - num_keywords):
            # Position i marks the first word of the candidate. Proceeds only if it's not a stopword
            if sl[i] not in stop_list:
                candidate = sl[i]
                j = 1
                keyword_counter = 1
                contains_stopword = False
                # Until the word count reaches the maximum number of keywords or the end is reached
                while keyword_counter < num_keywords and i + j < len(sl):
                    candidate = candidate + ' ' + sl[i + j]
                    # If it's not a stopword, increase the word counter. If it is, turn on the flag
                    if sl[i + j] not in stop_list:
                        keyword_counter += 1
                    else:
                        contains_stopword = True
                    j += 1
                # Adds the candidate to the list only if:
                # 1) it contains at least a stopword (if it doesn't it's already been considered)
                # 2) the last word is not a stopword
                # 3) the adjoined candidate keyphrase contains exactly the correct number of keywords (to avoid doubles)
                if contains_stopword and candidate.split()[-1] not in stop_list and keyword_counter == num_keywords:
                    candidates.append(candidate)
    return candidates


def filter_adjoined_candidates(candidates, min_freq):
    candidates_freq = Counter(candidates)
    filtered_candidates = []
    for candidate in candidates:
        freq = candidates_freq[candidate]
        if freq >= min_freq:
            filtered_candidates.append(candidate)
    return filtered_candidates


def generate_candidate_keywords(sentence_list, stop_word_pattern, stop_word_list, min_char_length=1, max_words_length=3,
                                min_words_length_adj=1, max_words_length_adj=1, min_phrase_freq_adj=2):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stop_word_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "" and is_acceptable(phrase, min_char_length, max_words_length):
                phrase_list.append(phrase)
    phrase_list += extract_adjoined_candidates(sentence_list, stop_word_list, min_words_length_adj,
                                               max_words_length_adj, min_phrase_freq_adj)
    return phrase_list


def is_acceptable(phrase, min_char_length, max_words_length):
    if len(phrase) < min_char_length:
        return 0

    words = phrase.split()
    if len(words) > max_words_length:
        return 0

    digits = 0
    alpha = 0
    for i in range(0, len(phrase)):
        if phrase[i].isdigit():
            digits += 1
        elif phrase[i].isalpha():
            alpha += 1

    if alpha == 0:
        return 0

    if digits > alpha:
        return 0
    return 1


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  # orig.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score, min_keyword_frequency=1):
    keyword_candidates = {}
    for phrase in phrase_list:
        if min_keyword_frequency > 1:
            if phrase_list.count(phrase) < min_keyword_frequency:
                continue
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path, min_char_length=3, max_words_length=5, min_keyword_frequency=1,
                 min_words_length_adj=1, max_words_length_adj=1, min_phrase_freq_adj=1):
        self.__stop_words_path = stop_words_path
        self.__stop_words_list = load_stop_words(stop_words_path)
        self.__min_char_length = min_char_length
        self.__max_words_length = max_words_length
        self.__min_keyword_frequency = min_keyword_frequency
        self.__min_words_length_adj = min_words_length_adj
        self.__max_words_length_adj = max_words_length_adj
        self.__min_phrase_freq_adj = min_phrase_freq_adj

    def run(self, text):
        sentence_list = split_sentences(text)
        stop_words_pattern = build_stop_word_regex(self.__stop_words_list)

        phrase_list = generate_candidate_keywords(sentence_list, stop_words_pattern, self.__stop_words_list,
                                                  self.__min_char_length, self.__max_words_length,
                                                  self.__min_words_length_adj, self.__max_words_length_adj,
                                                  self.__min_phrase_freq_adj)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores, self.__min_keyword_frequency)
        sorted_keywords = sorted(six.iteritems(keyword_candidates), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords
