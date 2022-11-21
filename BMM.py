import time
import SearchMethods
from DictionaryCreate import traditional_cigarette, dicDrain
from regex_preprocess import regexreplace, regexcheck

dic = []
MAX_TOKEN_LENGTH = 19


class PortableBMM:
    def __init__(self):
        self.dic = []
        self.maxlength=19

    def train(self, filename):
        dicDrain(filename, 'pbmmtempdic.txt')
        traditional_cigarette('pbmmtempdic.txt', self.dic)

    def seg(self, seg_list):
        if isinstance(seg_list, list):
            line=''
            for token in seg_list:
                line=line+token
        else:
            line = seg_list
        length = MAX_TOKEN_LENGTH
        lenline = len(line)
        right = lenline
        stack = []
        # print(line[19:right])
        while 0 < right:  # target!
            # print(line[start:start+length])
            # 找到了
            if 0 < right - length:
                cur = line[right - length:right]
            else:
                cur = line[0:right]
            if SearchMethods.binarySearch(self.dic, 0, len(self.dic) - 1, cur):  # or other available search method
                # print(cur+'/')
                stack.append(cur)
                right = right - length
                length = MAX_TOKEN_LENGTH
            elif length == 1:
                stack.append(cur)
                right = right - length
                length = MAX_TOKEN_LENGTH
            else:
                length = length - 1
        stack.reverse()
        return stack

    def get_dic(self):
        return self.dic




def BMM(dicfile, testfile, outresultfile):
    traditional_cigarette(dicfile, dic)

    with open(testfile, "r", encoding='gbk') as file, \
            open(outresultfile, "w", encoding='gbk') as BMMresult:
        time_start = time.time()
        for line in file:
            line = line.strip('\n')
            # line=line.decode("utf-8")
            # print(line)
            length = MAX_TOKEN_LENGTH
            lenline = len(line)
            right = lenline
            stack = []
            # print(line[19:right])
            while 0 < right:  # target!
                # print(line[start:start+length])
                # 找到了
                if 0 < right - length:
                    cur = line[right - length:right]
                else:
                    cur = line[0:right]
                if SearchMethods.binarySearch(dic, 0, len(dic) - 1, cur):  # or other available search method
                    # print(cur+'/')
                    stack.append(cur)
                    right = right - length
                    length = MAX_TOKEN_LENGTH

                elif regexcheck(cur):
                    # print(cur + '/')
                    # BMMresult.write(cur + '/ ')
                    stack.append(cur)
                    right = right - length
                    length = MAX_TOKEN_LENGTH
                elif length == 1:
                    # print(cur + '/')
                    # BMMresult.write(cur + '/ ')
                    stack.append(cur)
                    right = right - length
                    length = MAX_TOKEN_LENGTH
                else:
                    # print(cur+'not in dic')
                    length = length - 1
            # print('end of one line')
            i = len(stack) - 1
            while i >= 0:
                BMMresult.write(stack[i] + '/ ')
                i -= 1
            BMMresult.write('\n')
        time_end = time.time()
        print('time cost', time_end - time_start, 's')


if __name__ == '__main__':
    dicfile = 'dic.txt'
    testfile = '199801_sent.txt'
    outresultfile = 'seg_BMM.txt'
    #BMM(dicfile, testfile, outresultfile)
    # traditional_cigarette('gbk_complexdic_ultra.txt')
    pb=PortableBMM()
    pb.train('199802.txt')
    result = pb.seg(['今','天','天','气','晴朗'])
    print(result)

