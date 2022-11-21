ENCODING = 'gbk'
import re
from CBGM import *
from regex_preprocess import *
# from Evaluate import evaluation
from BMM import PortableBMM

"""def continue_singleton(seg):
    total_char = 0
    num = len(seg)
    continue_single = 0
    for i in len(seg):
        total_char += len(seg[i])
        if len(seg[i]) == 1 and len(seg[i + 1] == 1):
            continue_single += 1"""


def timestamp(seg):
    # print(seg[0])
    if len(seg[0]) > 1 and seg[0][0] == '§':
        newseg = []
        newseg.append('§')
        newseg.append(seg[0][1:])
        newseg.extend(seg[1:])
        return newseg
    return seg


def CBGM_poct(trainfile, testfile, outresultfile):
    # 初始化
    model = CharacterBasedGenerativeModel()
    pb = PortableBMM()
    # 训练两个模型
    model.train(trainfile)
    pb.train(trainfile)

    with open(testfile, 'r', encoding=ENCODING) as file, \
            open(outresultfile, 'w', encoding=ENCODING) as result:
        # 文件文本预处理
        for line in file:
            line = line.strip('\n')
            if line == '':
                result.write('\n')
                continue
            # 正则处理
            line, iter_list = regexreplace(line)
            # CBGM返回的label序列
            predict_token = model.segmentation(line)
            # label序列转成分出的词的列表
            seg = token2seg(predict_token, line)
            # 拆开【正则+汉字】形式的词
            seg = timestamp(seg)
            # 计算分词数与字数比，比值过大改用BMM
            if len(seg) / len(line) > 0.75:
                seg = pb.seg(line)

            # 还原正则
            post_regex_seg = []
            for word in seg:
                word, iter_list = regex_recover(word, iter_list)
                post_regex_seg.append(word)

            # 处理大写年份
            for i in range(len(post_regex_seg) - 1):
                if re.match(purehannum, post_regex_seg[i]) and post_regex_seg[i + 1] == '年':
                    post_regex_seg[i + 1] = post_regex_seg[i] + '年'
                    post_regex_seg.pop(i)
                    break
                # TODO 双版本
            # 过长序列做拆分，逻辑不太朴实，估计只对训练语料有效，第二版里没有这个
            if len(post_regex_seg[0]) > 19:
                post_regex_seg.insert(1, post_regex_seg[0][19:])
                post_regex_seg.insert(1, post_regex_seg[0][:19])
                post_regex_seg.pop(0)
            # 输出
            for word in post_regex_seg:
                result.write(str(word) + '/ ')
            result.write('\n')


# 跟第一版几乎一样 删去了长序列拆分这一步
def CBGM_poct2(trainfile, testfile, outresultfile):
    # 初始化
    model = CharacterBasedGenerativeModel()
    pb = PortableBMM()
    # 训练两个模型
    model.train(trainfile)
    pb.train(trainfile)

    with open(testfile, 'r', encoding=ENCODING) as file, \
            open(outresultfile, 'w', encoding=ENCODING) as result:
        # 文件文本预处理
        for line in file:
            line = line.strip('\n')
            if line == '':
                result.write('\n')
                continue
            # 正则处理
            line, iter_list = regexreplace(line)
            # CBGM返回的label序列
            predict_token = model.segmentation(line)
            # label序列转成分出的词的列表
            seg = token2seg(predict_token, line)
            # 拆开【正则+汉字】形式的词
            seg = timestamp(seg)
            # 计算分词数与字数比，比值过大改用BMM
            if len(seg) / len(line) > 0.75:
                seg = pb.seg(line)

            # 还原正则
            post_regex_seg = []
            for word in seg:
                word, iter_list = regex_recover(word, iter_list)
                post_regex_seg.append(word)

            # 处理大写年份
            for i in range(len(post_regex_seg) - 1):
                if re.match(purehannum, post_regex_seg[i]) and post_regex_seg[i + 1] == '年':
                    post_regex_seg[i + 1] = post_regex_seg[i] + '年'
                    post_regex_seg.pop(i)
                    break
            # 输出
            for word in post_regex_seg:
                result.write(str(word) + '/ ')
            result.write('\n')
if __name__ == '__main__':
    # print(timestamp(['§胜利', 'hao', 'd']))
    CBGM_poct('0203.txt', '199801_sent.txt', 'posttest.txt')

