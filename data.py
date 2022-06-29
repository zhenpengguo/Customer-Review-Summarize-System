import json
import os
from collections import defaultdict

#数据读取
def read_data():
    with open('../data/business.json') as f:
        index = 0
        for line in f:
            index = index + 1
            line_data = json.loads(line.strip())
            print(json.dumps(line_data, indent=4))
            if index == 1:
                break

    # 数据提取
    # 存放id - name
    business_file = open('../data/business_id.csv', 'w', encoding="utf8")
    with open("../data/business.json", encoding="utf8") as f:
        business_file.write("business_id" + "\t" + "name" + "\n")
        for line in f:
            line_data = json.loads(line.strip())
            business_file.write(line_data["business_id"] + "\t" + line_data["name"] + "\n")

    with open("../data/business.json") as f:
        index = 0
        for line in f:
            index = index + 1
            line_data = json.loads(line.strip())
            print(json.dumps(line_data, indent=4))
            if index == 1:
                break

    # 将每个id 的评论单独存放到一个文件，需要过滤到评论数不到100的商品。
    split_data_path = "split_data"
    split_data_dict = defaultdict(list)
    with open("../data/review.json", encoding="utf8") as f:
        for line in f:
            line_data = json.loads(line.strip())
            split_data_dict[line_data["business_id"]].append(line.strip())

    for key, value in split_data_dict.items():
        if len(value) >= 100:
            each_file = os.path.join(split_data_path, key + ".txt")
            with open(each_file, "w", encoding="utf8") as f:
                for line in value:
                    f.write(line + "\n")





def build_model_data():
    """
    建立模型训练和测试数据
    每条数据前面添加'__label__' 如果当前数据为1
    :return:
    """
    # __label__0 x x x x x x
    review_data = "../data/review.json "
    model_train_data = "../data/model_train.txt"
    label = '__label__'
    with open('//data/review.json', 'r', encoding='utf8') as review_f ,open(model_train_data, 'w', encoding='utf8') as train_f:
        for line in review_f:
            if len(line) ==0:
                continue
            review = json.loads(line.strip())
            sentence =''
            if review['stars'] >=4:
                text = review['text']
                text = text.replace('\n','')
                sentence = label + str(1) + ' ' + text + '\n'
            elif review['stars'] <=2 :
                text = review['text']
                text =text.replace('\n','')
                sentence = label + str(0) + ' ' + text + '\n'
            if not (len(sentence)==0 & sentence.isspace()):
                train_f.write(sentence)


if __name__ ==  '__main__':
    #读取数据，抽取数据
    read_data()
    #建立情感分类模型的训练和测试数据
    build_model_data()
    # 切分数据 50000条用于测试，剩余用作训练
    FAST_TEXT_TEST_DATA = "../data/data_test.txt"
    FAST_TEXT_TRAIN_DATA = "../data/data_train.txt"
    os.system("shuf ../data/model_train.txt -o ../data/model_train_shuffle.txt")

    with open("../data/model_train_shuffle.txt", "r", encoding="utf8") as f:
        index = 0
        train = open(FAST_TEXT_TRAIN_DATA, "w", encoding="utf8")
        test = open(FAST_TEXT_TEST_DATA, "w", encoding="utf8")
        for line in f:
            index = index + 1
            if index < 50000:
                test.write(line)
            else:
                train.write(line)

        train.close()
        test.close()




























