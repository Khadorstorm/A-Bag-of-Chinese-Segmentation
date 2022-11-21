from unigram import unigram
from HMMC2 import characterHMM
from CBGM import CBGM
from PostProcess import CBGM_poct, CBGM_poct2
from Evaluate import ten_fold

trainfile = 'all.txt'
# 测试文件路径
testfile = ''
resultfile = 'seg_LM.txt'
dicfile = 'dic.txt'

# 一次跑一个
# 最大概率
# unigram(dicfile, testfile, resultfile)
# 字HMM
# characterHMM(trainfile, testfile, resultfile)
# 二元字生成式
CBGM(trainfile, testfile, resultfile)

# 3.6版本1
CBGM_poct(trainfile, testfile, resultfile)
# 3.6版本2
CBGM_poct2(trainfile, testfile, resultfile)


# 使用三个月数据的十折测试
# 由于我是苹果环境，运行时可能需要到Evaluate.py中修改文件路径，时间紧张来不及改的更友好了，抱歉（
# 输入参数: fmm, bmm, unigram, hmm, cbgm, cbgmpoct，测试对应模型
# ten_fold()

