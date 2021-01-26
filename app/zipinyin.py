
s='āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'

def yin_index():
    print(s.encode('gbk'))

def hanzi_tone():
    i = int('a8', 16)
    j = int('a1', 16)
    for k in range(24):
        b = bytes([i, j + k])
        print(b.decode('gbk'))

def hanzi_tone2():
    byte=bytearray()
    i = int('a8', 16)
    j = int('a1', 16)
    for k in range(24):
        byte.append(i)
        byte.append(j + k)
    print(byte.decode('gbk'))


#str 转换成 bytes 用 encode()

# 一个序列直接得到字节类型
# bytes([36,36,36])

# 直接从十六进制到字节类型
# bytes.fromhex("a8 a1")

# 逆运算
# int(b' '.hex(), base=16)

def word2gbk(word):
    return word.encode('gbk').hex()


if __name__ == '__main__':
    hanzi_tone()
    hanzi_tone2()