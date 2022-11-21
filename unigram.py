import regex_preprocess
from DAG import *


def unigram(dicfile, testfile, outresultfile):
    lfreq, ltotal = gen_pfdict(dicfile)
    with open(testfile, 'r', encoding='gbk') as file, \
            open(outresultfile, 'w', encoding='gbk') as result:
        for line in file:
            line = line.strip('\n')
            line, iter_list = regex_preprocess.regexreplace(line)
            # print(iter_list[1])
            # print(line)
            DAG = get_DAG(line, lfreq)
            route = {}
            calc(line, DAG, route, lfreq, ltotal)
            # print(route)
            i = 0
            while i < len(line):
                if str(line[i:route[i][1] + 1]) == 'è':
                    # print(str(next(iter_list[0]).group()) + '/ ')
                    result.write(str(next(iter_list[0]).group()) + '/ ')
                elif str(line[i:route[i][1] + 1]) == '§':
                    # print(str(next(iter_list[1]).group()) + '/ ')
                    result.write(str(next(iter_list[1]).group()) + '/ ')
                else:
                    #print(str(line[i:route[i][1] + 1]) + '/ ')
                    result.write(str(line[i:route[i][1] + 1]) + '/ ')
                i = route[i][1] + 1
            result.write('\n')


if __name__ == '__main__':
    unigram('dic.txt', '199801_sent.txt', 'unigram_test.txt')

