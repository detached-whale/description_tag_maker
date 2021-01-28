# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from janome.tokenizer import Tokenizer
import nltk
import numpy as np
import math
import requests
from bs4 import BeautifulSoup


class Maker(object):
    def __init__(self):
        self.trimmer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[!！?。〜]+|[A-z]+|[+/\-@&*%]+|[0-9]+|[０-９]+)')
        self.slicer = nltk.RegexpTokenizer(u'([^!！?。〜]+います|[^!！?。〜]+ました|[^!！?。〜]+[!！?。〜])')
        self.tokenizer = Tokenizer()
        self.mat_words = defaultdict(int)
        self.term_frequency = defaultdict(int)
        self.inverse_document_frequency = defaultdict(list)

    def _tfidf(self, sentences):
        for index, sentence in enumerate(sentences):
            sentence = sentence.replace(u'!！?。〜', '')
            self.mat_words[index] = []
            for token in self.tokenizer.tokenize(sentence):
                if '名詞' not in token.part_of_speech:
                    continue

                if '非自立' in token.part_of_speech or '接尾' in token.part_of_speech or '数' in token.part_of_speech:
                    continue

                self.mat_words[index].append(token.base_form)
                self.term_frequency[token.base_form] += 1

                if index not in self.inverse_document_frequency[token.base_form]:
                    self.inverse_document_frequency[token.base_form].append(index)

    def make_from_web(self, url, line=10, tag='', option=''):
        html = requests.get(url)
        parser = BeautifulSoup(html.text, 'html.parser')
        document = parser.find(tag, option).text
        result = self.make(document, line)
        return result

    def make(self, document, line=10):
        document = ''.join(self.trimmer.tokenize(document))
        sentences = self.slicer.tokenize(document)
        self._tfidf(sentences)

        n = len(self.mat_words)
        m = len(self.inverse_document_frequency)
        mat_tf_idf = np.zeros(shape=(n, m))
        vec_tf_idf = []
        for index, word in enumerate(self.inverse_document_frequency):
            vec_tf_idf.append([word, self.term_frequency[word] * math.log10(n/len(self.inverse_document_frequency[word]))])

        for line_num, sentence in enumerate(mat_tf_idf):
            for word_num, word in enumerate(mat_tf_idf[line_num]):
                if vec_tf_idf[word_num][0] in self.mat_words[line_num]:
                    mat_tf_idf[line_num][word_num] = vec_tf_idf[word_num][1]

        mat_correlation = np.dot(mat_tf_idf, np.transpose(mat_tf_idf))
        d = 0.85
        for index in range(mat_correlation.shape[0]):
            mat_correlation[index, index] = 0
            sum_column = np.sum(mat_correlation[:,index])
            if sum_column != 0:
                mat_correlation[:, index] /= sum_column
            mat_correlation[:, index] *= -d
            mat_correlation[index, index] = 1

        mat_damping = (1-d) * np.ones((mat_correlation.shape[0], 1))
        ranks = np.linalg.solve(mat_correlation, mat_damping)
        index_sentences = []
        result = []

        for index, tfidf in enumerate(ranks):
            index_sentences.append([tfidf, index])

        index_sentences.sort(key=lambda x: x[0], reverse=True)

        for index in index_sentences[:line]:
            result.append(sentences[index[1]])

        return result
