import json

from utils import split_sentence, add_to_dict_list, Item, get_top_k, get_top_k_from_lsit, _contains_related_aspect
from model_training import SentimentModel ,FastText
from sentence import extract_sentence_aspects


class SentenceItem(Item):
    """
    存储句子文本
    是否是消极状态
    情绪的score
    """

    def __init__(self, content, isNeg, score):
        super().__init__(score, content)
        self.content = content
        self.isNeg = isNeg


class Business(object):
    """
    针对某一个特定的bussiness:
    1. 获取其中TOP 5的评价aspect
    2. 针对特定的aspect提取出TOP 5评论
    """
    BUSINESS_PATH = "./data/split_data/"
    FILE_SUFFIX = '.txt'

    # 把已经训练好的模型存放在文件里，并导入进来
    SENTIMENT_MODEL = SentimentModel()

    def __init__(self, business_id, buiness_name='default'):
        # 初始化变量以及函数
        self.business_id = business_id
        self.business_name = buiness_name
        self.aspects = list()
        self.aspects_reviews_neg = dict()
        self.aspects_reviews_pos = dict()
        self.business_path = Business.BUSINESS_PATH + business_id + Business.FILE_SUFFIX
        self.business_score = 0
        self.avg_score = 0.0

    def extract_aspects(self):
        """
        从一个business的review中抽取aspects

        """
        b_score = 0
        review_len = 0
        # 统计所有名次短语出现的次数

        all_aspects = dict()
        with open(self.business_path, 'r') as review_f:
            for line in review_f:
                if len(line) == 0:
                    continue
                review = json.loads(line.strip())
                review_len = review_len + 1
                b_score = b_score + review["stars"]
                # 抽取文本里面的名次短语
                sentence_aspects = extract_sentence_aspects(review['text'])
                for aspect in sentence_aspects:
                    if aspect in all_aspects:
                        all_aspects[aspect] = all_aspects[aspect] + 1
                    else:
                        all_aspects[aspect] = 1
        # 取出top5
        list = get_top_k(all_aspects, 5)
        self.avg_score = b_score / review_len
        for word in list:
            self.aspects.append(word.content)

        return self

    def aspect_based_summary(self):
        """
        返回一个business的summary. 针对于每一个aspect计算出它的正面负面情感以及TOP reviews.

        """
        with open(self.business_path, "r") as review_f:
            while True:
                line = review_f.readline()
                if len(line) == 0:
                    break
                review = json.loads(line)
                self._split_sentence_based_aspect(review["text"])

        summary = dict()
        for aspect in self.aspects:
            summary[aspect] = self._get_aspect_summary(aspect)
        return {'business_id': self.business_id,
                'buiness_name': self.business_name,
                'buiness_rating': self.avg_score,
                'aspect_summary': summary
                }

    def _split_sentence_based_aspect(self, text: str):
        """
        1. 分割review，
        2. 并判断是否包含某个aspect，判断是否包含某个特定aspect
        3. 如果包含则归到某个aspect下
        4. 预测其情感，归类到pos或者neg中
        :param sentence:
        :return:
        """
        sentences = split_sentence(text)
        for sentence in sentences:
            for aspect in self.aspects:
                if not _contains_related_aspect(aspect, sentence):
                    continue
                # 如果包含相关的aspect，就进行情感预测
                preview = self._preview_sentiment(sentence)
                item = SentenceItem(sentence, preview['isNeg'], preview["score"])
                if preview['isNeg']:
                    add_to_dict_list(self.aspects_reviews_pos, aspect, item)
                else:
                    add_to_dict_list(self.aspects_reviews_neg, aspect, item)
        # 到这里 就将所有的aspect中的 pos和neg 都提取出来了
        # 遍历所有的

    def _preview_sentiment(self, sentence: str):
        """
        预测句子包含的感情
        :param sentence:
        :return:
        """
        result = Business.SENTIMENT_MODEL.preview(sentence)
        return result

    def _get_aspect_summary(self, aspect: str):
        """
        获取相关aspect 的相关评论
        :param aspect:
        :return:
        """
        result = dict()
        try:
            neg_list = get_top_k_from_lsit(self.aspects_reviews_neg[aspect], 5)
            result["neg"] = self._get_review_text(neg_list)
            pos_list = get_top_k_from_lsit(self.aspects_reviews_pos[aspect], 5)
            result["pos"] = self._get_review_text(pos_list)
        except:
            pass
        return result

    def _get_review_text(self, sentence_item_list):
        reviews = []
        for sentence_item in sentence_item_list:
            reviews.append(sentence_item.content)
        return reviews

# 存放id - name
business_id_name_dict = {}
with open("./data/business_id.csv","r", encoding="utf8") as f:
    next(f)
    for line in f:
        lines = line.strip().split("\t")
        business_id_name_dict[lines[0]] = lines[1]


if __name__ == 'main':
    fast = FastText()
    fast.train()
    ids = "0-3kCit8mt8cCjiQXDyg8w" # business ID
    business = Business(ids, business_id_name_dict.get(ids))
    a = business.extract_aspects().aspect_based_summary()
    print(a)













