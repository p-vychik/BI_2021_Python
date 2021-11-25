import re
import matplotlib.pyplot as plt
import numpy as np


# 1. parse ftp links in file
with open("./hw_regex/data/references.txt", 'r') as f_in:
    references = ''.join(f_in.readlines())
    ftps = re.findall(r"(ftp\S+?)(?=ftp|;|\t{1,}|\s{1,}|$)", references)
    with open("./hw_regex/data/ftps", 'w') as f_out:
        f_out.writelines('\n'.join(ftps))

# 2. get all digits
with open("./hw_regex/data/2430AD.txt", 'r') as f_in:
    text = ''.join(f_in.readlines())
    digits = re.findall(r"(([0-9]+)(\.([0-9]+))?)", text)
    print(f"total digits count: {len(digits)}")
    print(*list(map(lambda x: x[0], digits)), sep=" ")

# 3.  get all exclamatory sentences
with open("./hw_regex/data/2430AD.txt", 'r') as f_in:
    text = ''.join(f_in.readlines())
    words = re.findall(r"[a-zA-Z]*[Aa][a-zA-Z]*", text)
    print(f"total 'a'-containing words count: {len(words)}")
    print(*words, sep=" ")

# 4.  get all exclamatory sentences
with open("./hw_regex/data/2430AD.txt", 'r') as f_in:
    text = ''.join(f_in.readlines())
    sentences = re.findall(r"[^.!?\"]*[!]", text)
    print(f"total exclamatory sentences count: {len(sentences)}")
    print(*sentences, sep="\n")

# 5.  get all exclamatory sentences
with open("./hw_regex/data/2430AD.txt", 'r') as f_in:
    text = f_in.readlines()
    text = re.sub(r'\n{1,}', ' ', ''.join(text))
    un_words = re.findall(r"(\b\S+\b)(?!.*\1)", text)
    un_words_len = list(map(lambda x: len(x.encode("utf-8").decode('unicode-escape')),
                            un_words))
    labels, counts = np.unique(un_words_len, return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.gca().set_xticks(labels)
    plt.show()
    with open("./hw_regex/data/u_words", 'w') as f_out:
        f_out.writelines('\n'.join(un_words))
