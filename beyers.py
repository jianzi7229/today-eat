# 导入所需模块
import re, collections

# 定义一个函数，用于从文本中提取单词
def words(text):
    return re.findall('[a-z]+', text.lower())

# 定义一个函数，用于训练语言模型
def train(features):
    # 创建一个默认值为1的字典
    model = collections.defaultdict(lambda: 1)
    # 统计每个单词出现的次数
    for f in features:
        model[f] += 1
    return model

# 读取文本文件，并训练语言模型
NWORDS = train(words(open('big.txt').read()))

# 定义一个包含所有小写字母的字符串
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# 定义一个函数，用于生成所有与给定单词编辑距离为1的单词
def edits1(word):
    n = len(word)
    # 生成所有删除一个字母后的单词
    deletes = [word[0:i]+word[i+1:] for i in range(n)]
    # 生成所有相邻字母交换后的单词
    transposes = [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)]
    # 生成所有替换一个字母后的单词
    replaces = [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet]
    # 生成所有插入一个字母后的单词
    inserts = [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet]
    # 返回包含所有编辑距离为1的单词的集合
    return set(deletes + transposes + replaces + inserts)

# 定义一个函数，用于从所有编辑距离为1的单词中返回已知的单词集合
def known_edits2(word):
    # 生成所有编辑距离为2的单词集合
    edits2 = (e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    # 返回所有已知单词的集合
    return set(edits2)

# 定义一个函数，用于从给定单词集合中返回已知的单词集合
def known(words):
    # 返回所有已知单词的集合
    return set(w for w in words if w in NWORDS)

# 定义一个函数，用于纠正拼写错误
def correct(word):
    # 返回包含所有可能正确的单词的集合，优先级依次为已知单词、编辑距离为1的已知单词、编辑距离为2的已知单词、原始单词
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    # 返回在语言模型中出现频率最高的单词
    return max(candidates, key=lambda w: NWORDS[w])
