from regex_preprocess import regexreplace, regexcheck
import SearchMethods
from DictionaryCreate import traditional_cigarette
import time
dic = []
# 最大token长度
MAX_TOKEN_LENGTH = 19


def RELX5():
    SearchMethods.add_all(dic)


def FMM(dicfile, testfile, outresultfile):
    # 参数： 词典文件，待分词文本文件，分词结果文件名
    # 把字典文件放进list后排序
    traditional_cigarette(dicfile, dic)
    # trie树构造 但用的是ppt带字典的写法，忽略即可
    # RELX5()

    with open(testfile, "r", encoding='gbk') as file, \
            open(outresultfile, "w", encoding='gbk') as FMMresult:
        # 计时
        time_start = time.time()
        # 按行读入
        for line in file:
            line = line.strip('\n')
            # line = regexreplace(line)
            # line=line.decode("utf-8")
            # print(line)
            start = 0
            length = MAX_TOKEN_LENGTH
            lenline = len(line)
            # print(line[start:start + length])
            while start < lenline:
                # print(line[start:start+length])
                # 找到了
                if start + length < lenline:
                    cur = line[start:start + length]
                else:
                    cur = line[start:lenline]
                # 确认是否在字典里，以下三条if各是一种查找方法，一次用一个
                #if SearchMethods.contain(cur):
                # 二分
                if SearchMethods.binarySearch(dic, 0, len(dic) - 1, cur):
                # 线性
                #if cur in dic:  # or other available search method
                    # print('find in dic')
                    # print(cur + '/')
                    FMMresult.write(cur + '/ ')
                    start = start + length
                    length = MAX_TOKEN_LENGTH
                # 不是词典中词则检查是否是符号序列，是则分成一个词
                elif regexcheck(cur):
                    # print(cur + '/')
                    FMMresult.write(cur + '/ ')
                    start = start + length
                    length = MAX_TOKEN_LENGTH
                # 单字分成一个词
                elif length == 1:
                    # print(cur + '/')
                    FMMresult.write(cur + '/ ')
                    start = start + length
                    length = MAX_TOKEN_LENGTH
                else:
                    # print(line[start:start+length]+'not in dic')
                    length = length - 1

            # print('end of one line')
            FMMresult.write('\n')
        time_end = time.time()
        print('time cost', time_end - time_start, 's')


# 跑这个
if __name__ == '__main__':
    dicfile='dic.txt'
    testfile='199801_sent.txt'
    outresultfile='seg_FMM.txt'
    FMM(dicfile, testfile, outresultfile)