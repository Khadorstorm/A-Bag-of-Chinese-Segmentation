import time


# ppt上的trie树代码，请忽略
class TrieNode:
    def __init__(self, character, terminal, children):
        self.character = character
        self.terminal = terminal
        self.children = children

    def is_terminal(self):
        return self.terminal

    def set_terminal(self, terminal):
        self.terminal = terminal

    def get_character(self):
        return self.character

    def set_character(self, character):
        self.character = character

    def get_children(self):
        return self.children

    def get_child(self, character):
        if character not in self.children:
            return None
        return self.children[character]

    def get_child_if_not_exist_then_create(self, character):
        child = self.get_child(character)
        if not child:
            child = TrieNode(character, False, {})
            self.add_child(child)
        return child

    def add_child(self, child):
        self.children[child.character] = child

    def remove_child(self, child):
        self.children[child.character] = None


def contain(astr):
    # astr = astr.replace('  ', '')  # TODO 预处理，可能要改
    if len(astr) < 1:
        return False
    node = ROOT_NODE  # TODO now what?
    for i in astr:
        child = node.get_child(i)
        if not child:
            return False
        else:
            node = child
    return node.is_terminal()


def add_all(word_list):
    for word in word_list:
        add(word)


def add(word):
    # word = word.replace('  ', '')  # TODO 预处理，可能要改

    if len(word) < 1:
        return

    node = ROOT_NODE

    for i in word:
        child = node.get_child_if_not_exist_then_create(i)
        node = child

    node.set_terminal(True)


my_dict = {}
ROOT_NODE = TrieNode(None, False, my_dict)

dic = []


#def traditional_cigarette():
    #with open("plain-ab-dict.txt", "r", encoding='utf-8') as file:
        #for line in file:
            #dic.append(line.strip('\n'))
            #dic.sort()
            # print(dic)


# 二分查找
def binarySearch(arr, l, r, x):
    if r >= l:
        mid = int(l + (r - l) / 2)
        if arr[mid] == x:
            return True
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return False

#自己测试代码 请忽略
if __name__ == '__main__':
    print('hello Trie')
    #traditional_cigarette()
    add_all(dic)
    # print(ROOT_NODE.get_child('不'))
    time_start = time.time()
    print(contain('黑龙江'))
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    # print()
    time_start = time.time()
    print(binarySearch(dic, 0, len(dic) - 1, '黑龙江'))
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
