from HMMC2 import token2seg, word2token
from regex_preprocess import regexreplace, regex_recover
from numpy import log
import math

ENCODING = 'gbk'
PLACEHOLDER = ('', 'PLD')


class Distribution:
    def __init__(self):
        self.dic = {}
        self.total = 0

    def get(self, key):
        if self.dic.__contains__(key):
            return self.dic[key] / self.total
        else:
            # print("this key "+str(key)+" doesn't exist")
            return 0

    def get_num(self, key):
        if self.dic.__contains__(key):
            return self.dic[key]
        else:
            # print("this key "+str(key)+" doesn't exist")
            return 0

    def add(self, key, delta):
        if self.dic.__contains__(key):
            self.dic[key] += delta
        else:
            self.dic[key] = delta
        self.total += delta
        return self.dic[key]

    def getdic(self):
        return self.dic

    def gettotal(self):
        return self.total

    def print(self):
        print(self.dic)


class CharacterBasedGenerativeModel:
    def __init__(self):
        self.unigram = Distribution()
        self.bigram = Distribution()
        # self.trigram = Distribution()

    def corpus_prepare(self, filename):
        # 把原始语料打包成（字，label）形式的二维列表
        linelist = []
        with open(filename, 'r', encoding=ENCODING) as file:
            for line in file:
                pair_of_line = []
                line = line.strip('\n')
                if line == '':
                    continue
                sp = line.split('  ')
                # print(sp)
                for pair in sp:
                    pair = pair.split('/')
                    # print(pair)
                    processed_word, _ = regexreplace(pair[0])
                    token_of_word = word2token(processed_word)
                    pair_of_line.append((processed_word, token_of_word))
                linelist.append(pair_of_line)
            return linelist

    def cal_prob(self, firstword, secondword):
        # 计算两个tokem间转换的条件概率
        # print((firstword, secondword))
        try:
            # 二元里有用二元
            if (firstword, secondword) in self.bigram.getdic():
                ret = self.bigram.get_num((firstword, secondword)) / self.unigram.get_num(firstword)
            # 二元没有回退到一元
            else:
                ret = self.unigram.get(secondword)
            # print(ret)
        # 一元未登录+1平滑
        except ZeroDivisionError:
            return 1 / self.unigram.gettotal()
        return ret

    def train(self, filename):
        data = self.corpus_prepare(filename)
        for line in data:
            # print(line)
            window = [PLACEHOLDER, PLACEHOLDER]
            self.unigram.add(PLACEHOLDER, 2)
            self.bigram.add((PLACEHOLDER, PLACEHOLDER), 1)
            for pair in line:
                for i in range(len(pair[0])):
                    window.append((pair[0][i], pair[1][i]))  # 当前（字，词中位置）加入窗口
                    # 更新各元组‍出现频率
                    self.unigram.add((pair[0][i], pair[1][i]), 1)
                    self.bigram.add(tuple(window[1:]), 1)
                    # self.trigram.add(tuple(window), 1)
                    window.pop(0)  # 弹出第一项
        # self.unigram.print()
        # self.bigram.print()

    def segmentation(self, line):
        # 分词动态规划，记住0-3分别对应SBME
        # 记录上一个字四种取值的最优概率和序列 即报告中的动态规划变量 psi_{t-1}(l)
        # last_best_result[0]代表psi_{t-1}(S)，以此类推
        last_best_result = [[0, []], [0, []], [0, []], [0, []]]
        for i in range(len(line)):
            # 单独处理第一个字
            if i == 0:
                for x in range(4):
                    last_best_result[x][0] = (log(self.cal_prob(('', 'PLD'), (line[i], x))))
            # 初始化psi_{t}(l)
            best_result = [[float('-inf'), []], [float('-inf'), []], [float('-inf'), []], [float('-inf'), []]]
            # 两层循环，计算所有可能第t-1和t个字的分类结果的概率（16种情况），从而计算出psi_{t}(l)
            for last_label in range(4):
                for label in range(4):
                    p = last_best_result[last_label][0] + log(
                        self.cal_prob((line[i - 1], last_label), (line[i], label)))
                    if p > best_result[label][0]:
                        best_result[label] = [p, last_best_result[last_label][1] + [label]]
            # 每步过后psi_{t}(l)变成psi_{t-1}(l)
            last_best_result = best_result
        # 取最后一步的最大值，即报告中式（9）
        plist = list(last_best_result[x][0] for x in range(4))
        best_index = plist.index(max(plist))

        return last_best_result[best_index][1]


def CBGM(trainfile, testfile, outresultfile):
    model = CharacterBasedGenerativeModel()
    model.train(trainfile)
    with open(testfile, 'r', encoding=ENCODING) as file, \
            open(outresultfile, 'w', encoding=ENCODING) as result:
        for line in file:
            line = line.strip('\n')
            if line == '':
                result.write('\n')
                continue
            line, iter_list = regexreplace(line)
            predict_token = model.segmentation(line)
            # print(predict_token)
            seg = token2seg(predict_token, line)
            # print(seg)
            for word in seg:
                word, iter_list = regex_recover(word, iter_list)
                result.write(str(word) + '/ ')
            result.write('\n')


if __name__ == '__main__':
    CBGM('0203.txt', '199801_sent.txt', 'CBGMtestrun.txt')
    """str='19980101-01-001-012台湾是中国领土不可分割的一部分。完成祖国统一，是大势所趋，民心所向。任何企图制造“两个中国”、“一中一台”、“台湾独立”的图谋，都注定要失败。希望台湾当局以民族大义为重，拿出诚意，采取实际的行动，推动两岸经济文化交流和人员往来，促进两岸直接通邮、通航、通商的早日实现，并尽早回应我们发出的在一个中国的原则下两岸进行谈判的郑重呼吁。'
    line, iter_list = regexreplace(str)
    print(line)
    print(regex_recover(line, iter_list))"""
