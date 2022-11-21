import SearchMethods


def dicDrain(filename, outfilename):
    dictionary = {}
    with open(filename, "r", encoding='gbk') as file:
        for line in file:
            line = line.strip('\n')
            sp = line.split('  ')
            # print(sp)
            for pair in sp:
                # plain ver
                # print(pair)
                # entry=pair.split('/')
                # print(entry)
                # if len(entry)==2:
                # dictionary[entry[0]]=entry[1]
                # dictionary[entry[0]] = entry[1]

                # fun ver
                if dictionary.__contains__(pair):
                    dictionary.update({pair: dictionary[pair] + 1})
                else:
                    dictionary[pair] = 1
            # print(dictionary)

    with open(outfilename, "w", encoding='gbk') as file:
        for key in dictionary:
            entry = key.split('/')
            # file.write(key+' '+str(dictionary[key])+'\n')
            if len(entry) == 2:
                # 词 词性 词频
                file.write(entry[0] + ' ' + entry[1] + ' ' + str(dictionary[key]) + '\n')
                # 只有词
                # file.write(entry[0] + '\n')
        file.close()


def traditional_cigarette(filename, dic):
    with open(filename, "r", encoding='gbk') as file:
        for line in file:
            # dic.append(line.strip('\n'))
            dic.append(line.split(' ')[0].strip('\n'))
        dic.sort()
        # print(dic)


def RELX5(dic):
    # 你要不要来一棵
    trie = SearchMethods.add_all(dic)


if __name__ == '__main__':
    filename = '199801_seg&pos.txt'
    outfilename = 'gbkdic.txt'
    dicDrain(filename, outfilename)

