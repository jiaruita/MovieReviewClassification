def read_words(f, number):
    words = []
    text = f.read()
    lines = text.split('\n')
    for index, line in enumerate(lines):
        start = line.index('(')
        end = line.index(',')
        word = line[start + 2: end - 1]
        words.append(word)
        if index > number:
            break
    return words

def run():
    posf = open('posword.txt')
    negf = open('negword.txt')
    posl = read_words(posf, 1000)
    negl = read_words(negf, 1000)
    result = []
    pos1000 = open('pos1000.txt', 'w')
    neg1000 = open('neg1000.txt', 'w')
    for word in posl:
        if word not in negl:
            result.append(word)
            pos1000.write(word + '\n')
    for word in negl:
        if word not in posl:
            result.append(word)
            neg1000.write(word + '\n')
    return result
    pos1000.close()
    neg1000.close()


    


