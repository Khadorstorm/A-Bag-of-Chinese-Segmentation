import re

ch = re.compile(r'(百分之|千分之|万分之|第)*((一|二|三|四|五|六|七|八|九|十|零|两|○)+(千|万|亿|百|点|分之|比|几)*)+')
num = re.compile(r'(第)*([0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+')
seq = re.compile(r'(([A-Z]|[a-z]|[Ａ-Ｚ]|[ａ-ｚ]|[0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+)')
time = re.compile(r'([0-9]|[０-９])+(年|月|日|小时|点钟|时|分|秒)')
purehannum = re.compile(r'^(一|二|三|四|五|六|七|八|九|零|○)(一|二|三|四|五|六|七|八|九|零|○)+$')


# 把符合正则的部分替换成特定token，返回一个被替换部分的迭代器
def regexreplace(line):
    ch = re.compile(r'(百分之|千分之|万分之|第)*((一|二|三|四|五|六|七|八|九|十|零|两|○)+(千|万|亿|百|点|分之|比|几)*)+')
    num = re.compile(r'(第)*([0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+')
    seq = re.compile(r'(([A-Z]|[a-z]|[Ａ-Ｚ]|[ａ-ｚ]|[0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+)')
    time = re.compile(r'([0-9]|[０-９])+(年|月|日|小时|点钟|时|分|秒)')
    # TODO regexlist 解耦
    reg_list = [(ch, 'è'), (seq, '§')]  # 元素是正则表达式和对应token的二元组
    iter_list = []
    for reg in reg_list:
        it = re.finditer(reg[0], line)
        iter_list.append(it)
        line = re.sub(reg[0], reg[1], line, 0)
    return line, iter_list


# 将正则标记恢复原样
# 一个词里出现两个标记可能会出bug
def regex_recover(word, iter_list):
    # print(word)
    for i in range(len(word)):
        # print(word[i])
        if word[i] == 'è':
            # word[i] = str(next(iter_list[0]).group())
            try:
                word = word[:i] + str(next(iter_list[0]).group()) + word[i + 1:]
            except StopIteration:
                print('stopit')
            # print(i)
        if word[i] == '§':
            try:
                word = word[:i] + str(next(iter_list[1]).group()) + word[i + 1:]
            except StopIteration:
                print('stopit')
            # print(i)
    return word, iter_list


# 检查一个字符串是非汉字符号串
def regexcheck(line):
    eng_regex = r'^([A-Z]|[a-z]|[Ａ-Ｚ]|[ａ-ｚ]|[0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+$'
    # 这个暂时用不到
    date_regex = r'^(\d+-)+\d+$'
    if re.match(eng_regex, line):
        # print('eng')
        return True
    elif re.match(date_regex, line):
        return True
    return False


# 自己测试用，请忽略
if __name__ == '__main__':
    """with open('dividedemo.txt', "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n')
            line = regexcheck(line)
            # line=line.decode("utf-8")
            print(line)
"""
    seq = re.compile(r'(([A-Z]|[a-z]|[Ａ-Ｚ]|[ａ-ｚ]|[0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+)')  # re.I 表示忽略大小写
    pattern2 = re.compile(r'(([a-z]|[0-9])+)', re.I)
    time = re.compile(r'月|日|小时|点钟|时|分|秒')
    ch = re.compile(r'(百分之|千分之|万分之|第)*((一|二|三|四|五|六|七|八|九|十|零|两|○|)+(千|万|亿|百|点|分之|比|几)*)+')
    num = re.compile(r'(第)*([0-9]|[０-９]|-|－|—|%|％|\+|\.|．|·|:|∶|／)+')
    m = seq.findall('18-94年pc2我12%')
    # print(m[1].start())
    pline = re.sub(ch, '♟', '去北京大学第一玩', 0)
    print(m)
    print(pline)

    it = re.finditer(ch, '去北京大学第一玩')
    for match in it:
        print(match.group())

