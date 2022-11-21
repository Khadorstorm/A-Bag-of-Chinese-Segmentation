from DictionaryCreate import dicDrain
from FMM import FMM
from BMM import BMM
from unigram import unigram
from HMMC2 import characterHMM
from CBGM import CBGM
from PostProcess import CBGM_poct


def get_answer(rawfile, outfilename, testfilename):
    # 吃一个原始语料文件rawfile，输出分词结果格式到outfilename
    with open(rawfile, "r", encoding='gbk') as file, \
            open(outfilename, "w", encoding='gbk') as answer, \
            open(testfilename, 'w', encoding='gbk') as test:
        for line in file:
            line = line.strip('\n')
            sp = line.split('  ')
            for pair in sp:
                wordandtype = pair.split('/')
                if wordandtype[0] == '':
                    continue
                answer.write(wordandtype[0].strip('[') + '/ ')  # 处理专有名词
                test.write(wordandtype[0].strip('['))
            answer.write('\n')
            test.write('\n')


def words_pos_set(line):
    # 把一行分词结果中所有词的起止下标做成一个集合
    line.strip('\n')
    words = line.split('/ ')
    begin = 0
    pos_set = set()
    for word in words:
        if len(word) == 0:
            continue
        pos_set.add((begin, begin + len(word) - 1))
        begin += len(word)
    # print(pos_set)
    return pos_set


def evaluation(resultfile, answerfile, analfile):
    TT, rtotal, atotal = 0, 0, 0
    with open(resultfile, "r", encoding='gbk') as result, \
            open(answerfile, "r", encoding='gbk') as answer, \
            open(analfile, 'w', encoding='gbk') as anal:
        for r_line, a_line in zip(result, answer):
            if r_line == '\n':
                continue
            rset = words_pos_set(r_line)
            aset = words_pos_set(a_line)
            rtotal += len(rset)
            atotal += len(aset)
            TT += len(rset & aset)
            if len(rset & aset) / len(rset) < 0.6:
                anal.write('=========\n')
                anal.write(r_line + '\n')
                anal.write(a_line + '\n')
                anal.write(str(len(rset)) + ' ' + str(len(aset)) + ' ' + str(len(rset & aset)) + '\n')

        precison = TT / rtotal
        recall = TT / atotal
        F1 = 2 * precison * recall / (precison + recall)
        print("precison: " + str(precison) + '\n' + "recall: " + str(recall))
        print("F1 score: " + str(F1))
        print('\n')
        return precison, recall, F1


def participation(k, testfile, answerfile, rawfile):
    # k为折数 size为每折大小
    # 把无标注语料 & 对应分词结果 & 抽词典用原始语料 文件分成十折
    with open(testfile, "r", encoding='gbk') as testf, \
            open(answerfile, "r", encoding='gbk') as answerf, \
            open(rawfile, "r", encoding='gbk') as rawdicfile:
        test_list = []
        ans_list = []
        raw_list = []
        for line in testf:
            test_list.append(line)
        for line in answerf:
            ans_list.append(line)
        for line in rawdicfile:
            raw_list.append(line)

        for i in range(k):
            with open('/Users/khador/PycharmProjects/NLP-E1/Parts/test' + str(i) + '.txt', "w", encoding='gbk') as part, \
                    open('/Users/khador/PycharmProjects/NLP-E1/Parts/ans' + str(i) + '.txt', "w",
                         encoding='gbk') as ans, \
                    open('/Users/khador/PycharmProjects/NLP-E1/Parts/rawdic' + str(i) + '.txt', "w",
                         encoding='gbk') as raw:
                j = i
                while j < len(test_list):
                    part.write(test_list[j])
                    ans.write(ans_list[j])
                    raw.write(raw_list[j])
                    j += 10
                """for j in range(size):
                    # testfile.readline()
                    part.write(testf.readline())
                    ans.write(answerf.readline())
                    raw.write(rawdicfile.readline())
                    j += 1"""
                i += 1


def concator(testlist):
    # 输入一个用于训练的下标list
    with open('./Parts/concatrd.txt', 'w', encoding='gbk') as crd:
        # open('concattest.txt', 'w', encoding='gbk') as:
        for index in testlist:
            with open('./Parts/rawdic' + str(index) + '.txt', 'r', encoding='gbk') as file:
                # open('test'+str(index)+'.txt', 'r', encoding='gbk'):
                crd.write(file.read())


def ten_fold(method):
    resultfilename = './PartDics/' + method + '_10foldresult.txt'
    tpresicion, trecall, tF1 = 0, 0, 0
    for i in range(0, 10):
        testfilename = './Parts/test' + str(i) + '.txt'
        print('Fold ' + str(i + 1))
        list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        list.remove(i)
        concator(list)
        dicDrain('./Parts/concatrd.txt', './PartDics/folddic.txt')
        if method == 'fmm':
            FMM('./PartDics/folddic.txt', testfilename, resultfilename)
        if method == 'bmm':
            BMM('./PartDics/folddic.txt', testfilename, resultfilename)
        if method == 'unigram':
            unigram('./PartDics/folddic.txt', testfilename, resultfilename)
        if method == 'hmm':
            characterHMM('./Parts/concatrd.txt', testfilename, resultfilename)
        if method == 'cbgm':
            CBGM('./Parts/concatrd.txt', testfilename, resultfilename)
        if method == 'cbgmpoct':
            CBGM_poct('./Parts/concatrd.txt', testfilename, resultfilename)
        p, r, f = evaluation(resultfilename, './Parts/ans' + str(i) + '.txt', 'analtemp.txt')
        tpresicion += p
        trecall += r
        tF1 += f
        # print('fold '+str(i)+' is done!')
    tpresicion /= 10
    trecall /= 10
    tF1 /= 10
    print('10 fold result:')
    print("precison: " + str(tpresicion) + '\n' + "recall: " + str(trecall))
    print("F1 score: " + str(tF1))


def acc_FBMM():
    # 分析FMM，BMM性能使用
    list = []
    for i in range(10):
        print('acc' + str(i + 1))
        list.append(i)
        concator(list)
        dicDrain('./Parts/concatrd.txt', './PartDics/folddic.txt')
        FMM('./PartDics/folddic.txt', './Parts/01test9.txt', 'Facctemp.txt')
        BMM('./PartDics/folddic.txt', './Parts/01test9.txt', 'Bacctemp.txt')
        print('FMM:')
        evaluation('Facctemp.txt', './Parts/01ans9.txt', 'fanaltemp.txt')
        print('BMM:')
        evaluation('Bacctemp.txt', './Parts/01ans9.txt', 'Banaltemp.txt')


if __name__ == '__main__':
    # get_answer('199802.txt',"02_answer.txt",'02_test.txt')
    # a = words_pos_set("19980101-01-001-002/ 中共中央/ 总书记/ 、/ 国家/ 主席/ 江/ 泽民/ ")
    # b = words_pos_set("19980101-01-001-002中共中央总书/ 记/ 、/ 国家/ 主席/ 江泽/ 民/ ")
    # print(a&b)
    evaluation('CBGMtestrun.txt', 'gbk_seg_answer.txt','CBGManalysis.txt')
    # evaluation('gbk_seg_answer.txt','lhx199801_seg&pos_true.txt')
    # participation(10, '199801_sent.txt',"gbk_seg_answer.txt",'199801_seg&pos.txt')
    # concator([0, 1, 2, 3, 4, 5, 6, 7, 8])
    # ten_fold('hmm')
    # acc_FBMM()

