# 此文件包含模型的训练。 给定数据集，训练出情感分类模型，并把模型文件存放在 model文件夹里。
FAST_TEXT_TEST_DATA = "./data/data_test.txt"
FAST_TEXT_TRAIN_DATA = "./data/data_train.txt"
import fasttext
FAST_TEXT_MODEL = "./model/fast_text.bin"
class FastText(object):
    def __init__(self):
        pass

    def train(self):
        model = fasttext.train_supervised(input=FAST_TEXT_TRAIN_DATA, lr=1.0, epoch=25, wordNgrams=2, bucket=200000,
                                          dim=50, loss='hs')
        model.save_model(FAST_TEXT_MODEL)
        print(model.test(FAST_TEXT_TEST_DATA, k=-1))

    def preview(self, review: str):
        model = fasttext.load_model(FAST_TEXT_MODEL)
        result = model.predict(text=review, threshold=0.5)

        isNeg = (result[0][0] == '__label__0')
        score = result[1][0]

        print(isNeg)
        print(score)


# fast = FastText()
# fast.train()


class SentimentModel(object):
    def __init__(self):
        self.model = fasttext.load_model(FAST_TEXT_MODEL)

    def preview(self, review: str):
        result = self.model.predict(text=review, threshold=0.5)
        isNeg = (result[0][0] == '__label__0')
        score = result[1][0]
        # print(isNeg)
        # print(score)
        return {'isNeg': isNeg, 'score': "{:.4f}".format(score)}
#
# fast_predict = SentimentModel()
# fast_predict.preview('Tastes great')