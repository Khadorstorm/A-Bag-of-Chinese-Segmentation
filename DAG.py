from math import log
import re


def gen_pfdict(filename):
    lfreq = {}  # 保存前缀词典中的词及词频
    ltotal = 0  # 保存总的词数
    with open(filename, encoding='gbk') as fp:
        line = fp.readline()
        while len(line) > 0:
            # 保存离线词典中的词及词频
            spline = line.split()
            word = spline[0]
            freq = spline[2]
            freq = int(freq)
            lfreq[word] = freq
            ltotal += freq
            # 对于离线词典中的每个词，获取其前缀词
            for ch in range(len(word)):
                wfrag = word[:ch + 1]
                if wfrag not in lfreq:
                    lfreq[wfrag] = 0
            line = fp.readline()
    return lfreq, ltotal


def get_DAG(sentence, lfreq):
    DAG = {}
    N = len(sentence)
    for k in range(N):
        tmplist = []
        i = k
        frag = sentence[k]
        while i < N and frag in lfreq:
            if lfreq[frag] > 0:
                tmplist.append(i)
            i += 1
            frag = sentence[k:i + 1]
        if not tmplist:
            tmplist.append(k)
        DAG[k] = tmplist
    return DAG


def calc(sentence, DAG, route, lfreq, ltotal):
    #print(DAG)
    N = len(sentence)
    #print(N)
    route[N] = (0, 0)
    logtotal = log(ltotal)
    for idx in range(N - 1, -1, -1):  # 从 N-1 到 0 每次-1
        try:
            route[idx] = max((log(lfreq[sentence[idx:x + 1]] or 1) - logtotal + route[x + 1][0], x) for x in DAG[idx])
        except KeyError:
            route[idx] = max((-logtotal + route[x + 1][0], x) for x in DAG[idx])


lfreq = {'北京大学': 2053,
         '北': 17860,
         '北京': 34888,
         '北京大': 0,
         '大学': 20025,
         '大': 144099,
         '去': 123402,
         '玩': 4207,
         '京': 6583,
         '学': 17482}

if __name__ == '__main__':
    # print(get_DAG('去北京大学玩', lfreq))
    ch = re.compile(r'(百分之|千分之|万分之|第)*((一|二|三|四|五|六|七|八|九|十|零|两|○)+(千|万|亿|百|点|分之|比|几)*)+')
    lfreq, ltotal = gen_pfdict('dic.txt')
    # print(lfreq2,ltotal)

    line = '去北京大学一百二十八点三玩百分之八十'
    it = re.finditer(ch, line)
    line = re.sub(ch, 'è', line, 0)
    print(line)

    DAG = get_DAG(line, lfreq)
    route = {}
    calc(line, DAG, route, lfreq, ltotal)
    print(route)
    i = 0
    while i < len(line):
        if str(line[i:route[i][1] + 1]) == 'è':
            print(str(next(it).group()) + '/ ')
        else:
            print(str(line[i:route[i][1] + 1]) + '/ ')
        i = route[i][1] + 1
