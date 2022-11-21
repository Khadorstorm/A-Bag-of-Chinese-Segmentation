import numpy as np
from numpy import log
from regex_preprocess import regexreplace, regex_recover

ENCODING = 'gbk'


def token2seg(tokenlist, line):
    # line为正则处理过的line
    seg_list = []
    temp=''
    for i in range(len(tokenlist)):
        if tokenlist[i]==3:#e
            temp=temp+line[i]
            seg_list.append(temp)
            temp=''
        elif tokenlist[i]== 0 or tokenlist[i]== 1: #S,B
            if temp!='':
                seg_list.append(temp)
                temp=''
            temp=temp+line[i]
        else:
            temp=temp+line[i]

    if temp!='':
        seg_list.append(temp)
    return seg_list


def word2token(word):
    # 词列表转标注序列
    # print(word)
    if len(word) == 1:
        return [0]
    elif len(word) > 1:
        list = [1]
        for i in range(len(word) - 2):
            list.append(2)
        list.append(3)
        return list
    else:
        # print('word length went wrong!')
        return []


def get_model(filename):
    #训练HMM
    A = np.zeros((4, 4))
    alldic = {}
    #加入GBK中单字
    for i in range(0x8140, 0xFEFE):
        try:
            # print(i.to_bytes(2, 'big').decode('gbk'))
            alldic[i.to_bytes(2, 'big').decode(ENCODING)] = 0.01
        except UnicodeDecodeError:
            pass
    B = [alldic.copy(), alldic.copy(), alldic.copy(), alldic.copy()]
    first_pi = np.zeros((1, 4))

    with open(filename, 'r', encoding=ENCODING) as file:
        for line in file:
            #预处理
            tokens = []
            line = line.strip('\n')
            if line == '':
                continue
            sp = line.split('  ')
            # print(sp)
            for pair in sp:
                pair = pair.split('/')
                # print(pair)
                processed_word, _ = regexreplace(pair[0])
                # print(processed_word)
                token_of_word = word2token(processed_word)
                # print(token_of_word)

                # 字典里有则+1，没有则初始化为1
                for i in range(len(processed_word)):
                    if B[token_of_word[i]].__contains__(processed_word[i]):
                        B[token_of_word[i]].update({processed_word[i]: B[token_of_word[i]][processed_word[i]] + 1})
                    else:
                        B[token_of_word[i]][processed_word[i]] = 1
                tokens.extend(token_of_word)
            first_pi[0][tokens[0]] += 1  # 不看时间戳 看第一个字
            for i in range(len(tokens) - 1):
                A[tokens[i]][tokens[i + 1]] += 1
    # B的平滑要在归一化之前
    A = A / A.sum(axis=1, keepdims=1)
    for i in B:
        sumBi = 0
        for b in i:
            sumBi += i[b]
        for b in i:
            i[b] /= sumBi
    first_pi = first_pi / first_pi.sum(axis=1, keepdims=1)
    # 返回模型参数
    return A, B, first_pi[0]


def vit(line, A, B, pi):
    # 维特比算法
    delta = np.zeros((len(line), len(A)))
    # phi = np.zeros((len(line), len(A)))
    phi = np.zeros((len(line), len(A)), dtype=np.int32)
    state = log(pi) + log(list(b[line[0]] for b in B))
    state = pi
    delta[0] = state
    phi[0] = np.argmax(state)

    for t in range(1, len(line)):
        # print((delta[t - 1] * A.T).max(axis=1))
        # print(list(b[line[t]] for b in B))
        try:
            # delta[t-1]中的第i个元素乘A的第i行
            delta[t] = ((delta[t - 1] + log(A.T)).max(axis=1)) + log(list(b[line[t]] for b in B))
            phi[t] = (delta[t - 1] + log(A.T)).argmax(axis=1)
        except KeyError:
            pass
        # print(delta[t])
        # print(phi[t])

    final_sequence = [delta[len(line) - 1].argmax()]
    for t in range(len(line) - 1, 0, -1):
        state_index = phi[t][final_sequence[-1]]
        final_sequence.append(state_index)
    # print("final_sequence: {}".format(final_sequence[::-1]))

    return final_sequence[::-1]


def characterHMM(trainfile, testfile, outresultfile):
    A, B, pi = get_model(trainfile)
    with open(testfile, 'r', encoding=ENCODING) as file, \
            open(outresultfile, 'w', encoding=ENCODING) as result:
        for line in file:
            line = line.strip('\n')
            if line == '':
                result.write('\n')
                continue
            line, iter_list = regexreplace(line)
            predict_token = vit(line, A, B, pi)
            seg = token2seg(predict_token, line)
            for word in seg:
                word, iter_list = regex_recover(word, iter_list)
                result.write(str(word) + '/ ')
            result.write('\n')


if __name__ == '__main__':
    obs = '去北京的北京大学北玩'
    ans = 'S B E S B M M E S S' \
          '0 1 3 0 1 2 2 3 0 0'
    A1 = np.array([[0.33, 0.66, 0, 0],
                   [0, 0, 0.5, 0.5],
                   [0, 0, 0.5, 0.5],
                   [0.7, 0.3, 0, 0]])
    B1 = [{'去': 0.25, '北': 0.25, '京': 0, '大': 0, '学': 0, '玩': 0.25, '的': 0.25},
          {'去': 0, '北': 1, '京': 0, '大': 0, '学': 0, '玩': 0, '的': 0},
          {'去': 0, '北': 0, '京': 0.5, '大': 0.5, '学': 0, '玩': 0, '的': 0},
          {'去': 0, '北': 0, '京': 0.5, '大': 0, '学': 0.5, '玩': 0, '的': 0}]
    pi = np.array([0.5, 0.5, 0, 0])
    # vit(obs, A1, B1, pi)
    # print(word2token(''))
    # A2, B2, pi2 = get_model('dictest.txt')
    # print(A2)
    # print(B2)
    # print(pi2)
    # print(vit('迈向充满希望的新世纪', A2, B2, pi2))
    print(token2seg([1, 3, 1, 3, 1, 3, 2, 2, 1, 3], '迈向充满希望的新世纪'))
    characterHMM('199801_seg&pos.txt', '199801_sent.txt', 'HMMtestrun1.txt')

