from nltk.tokenize import word_tokenize #分词
from nltk.stem import WordNetLemmatizer # 词形还原
from nltk import pos_tag #词性标注
from nltk import RegexpParser #通过正则找到定义的名词短语



class Sentence(object):
    """
    提取评论中的aspect
    """

    #词形还原（Lemmatization）是文本预处理中的重要部分，与词干提取（stemming）很相似
    LEMMATIZER = WordNetLemmatizer()

    def __init__(self, origin_sentence: str):
        self.sentence = origin_sentence
        self.word_tokens = list()
        self.pos_tags = list()

    def word_tokenize(self):
        assert len(self.sentence) != 0
        self.word_tokens = word_tokenize(self.sentence)
        return self

    def pos_tag(self):
        assert len(self.word_tokens) != 0
        self.pos_tags = pos_tag(self.word_tokens)
        return self

    def lemmatize(self):
        assert len(self.word_tokens) != 0
        # 目前只针对名词，因为目标是提取名词短语
        self.word_tokens = [Sentence.LEMMATIZER.lemmatize(word) for word in self.word_tokens]
        return self

    def _noun_phrase(self):
        assert len(self.pos_tags) != 0
        grammar = ('''
               NP: {<DT|PP\$>?<JJ><NN>}     # chunk determiner/possessive, adjectives and noun 限定词/所有词，形容词和名词
              {<NNP>+}                      # chunk sequences of proper nouns 专有名词序列
              {<NN>+}                       # chunk consecutive nouns 连续名词
              ''')

        # 编译正则表达式的接口
        cp = RegexpParser(grammar)
        sentenceTree = cp.parse(self.pos_tags)
        nounPhrases = self._extract_np(sentenceTree)  # collect Noun Phrase
        return nounPhrases

    def _extract_np(self, psent):
        for subtree in psent.subtrees():
            if subtree.label() == 'NP':
                yield ' '.join(word for word, tag in subtree.leaves())

    def contain_aspect(self):
        aspects = list()
        for aspect in self._noun_phrase():
            aspects.append(aspect)
        return aspects


# sentence = Sentence('Steve Jobs was the CEO of Apple Corp.')
#
# print(sentence.word_tokenize().lemmatize().pos_tag().contain_aspect())

def extract_sentence_aspects(sentence: str):
    """
    从句子中获取相关的aspect
    :param sentence:
    :return:
    """
    sen = Sentence(sentence)
    return sen.word_tokenize().lemmatize().pos_tag().contain_aspect()
# print(extract_sentence_aspects("Steve Jobs was the CEO of Apple Corp."))