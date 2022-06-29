import re
import operator
from queue import PriorityQueue

def split_sentence(sentence: str):
    """
    基于某种规则分割句子
    :param sentence:
    :return:
    """
    return re.split("[;,.!?\\n]",sentence)

def add_to_dict_list(container:dict,key,value):
    if key in container:
        container[key].append(value)
    else:
        data =list()
        data.append(value)
        container[key] =data

class Item(object):
    def __init__(self,priority,content):
        super().__init__()
        self.priority = priority
        self.content = content

    def __lt__(self, other):
        return operator.lt(self.priority, other.priority)


#优先级队列
def get_top_k(data:dict,k:int):
    """
    获取top k最大的子项
    :param data:
    :param k:
    :return:
    """
    priority = PriorityQueue(maxsize=k)
    for key ,value in data.items():
        if not priority.full():
            priority.put_nowait(Item(value,key))

        else:
            minor = priority.get_nowait()
            if minor.priority < value:
                priority.put_nowait(Item(value,key))
            else:
                priority.put_nowait(minor)
    ans =[]
    while not  priority.empty():
        ans.append(priority.get_nowait())

    return ans


def get_top_k_from_lsit(data:list,k:int):
    """
    从列表中获取top k最大的子项
    :param data:
    :param k:
    :return:
    """
    priority = PriorityQueue(maxsize=k)

    for value in data:
        if not priority.full():
            priority.put_nowait(value)
        else:
            minor = priority.get_nowait()
            if minor.priority < value.priority:
                priority.put_nowait(value)
            else:
                priority.put_nowait(minor)


    ans =[]
    while not priority.empty():
        ans.append(priority.get_nowait())

    return ans

def _contains_related_aspect(aspect: str, sentence: str):
    """
    当前句子中是否包含相关aspect  利用正则
    :param aspect:
    :return:
    """
    if re.search(aspect, sentence.lower()) is None:
        return False
    else:
        return True









