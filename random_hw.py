import numpy as np
import random
import time
import matplotlib.pyplot as plt
import re


def compare_modules():
    fig, ax = plt.subplots()
    time_array = []
    for i in range(1, 1001):
        cycle_time = 0
        for _ in range(1, 1001):
            start = time.time()
            np.random.rand(i)
            cycle_time += (time.time() - start)
        time_array.append(cycle_time / 1000)

    x = [_ for _ in range(1, 1001)]
    ax.plot(x, time_array, label='Numpy generation time')
    plt.show()


def bubble_sort(input_list):
    temp_list = input_list.copy()
    for i in range(len(temp_list) - 1, -1, -1):
        for j in range(1, i + 1):
            if temp_list[j] < temp_list[j - 1]:
                temp_list[j], temp_list[j - 1] = temp_list[j - 1], temp_list[j]
    return np.asarray(temp_list)


def check_sorting():
    fig, ax = plt.subplots()
    y_time = []
    y_stdev = []
    for length in range(1, 11):
        input_list = np.random.randint(0, 10000, size=length)
        sorted_list = bubble_sort(input_list)
        ind = np.random.randint(0, length, size=2)
        cycles_time = []
        for _ in range(1, 101):
            start = time.time()
            while not (input_list == sorted_list).all():
                input_list[ind[0]], input_list[ind[1]] = input_list[ind[1]], input_list[ind[0]]
                ind = np.random.randint(0, length, size=2)
            cycles_time.append(time.time() - start)

        y_time.append(sum(cycles_time) / 100)
        y_stdev.append(np.std(cycles_time))
    x = [_ for _ in range(1, 11)]
    ax.errorbar(x, y_time, yerr=y_stdev)
    plt.show()


def random_walk():
    steps = 100000
    x_steps = np.zeros(steps)
    y_steps = np.zeros(steps)
    for i in range(1, steps):
        x, y = np.random.randint(-1, 2, size=2)
        x_steps[i] = x_steps[i - 1] + x
        y_steps[i] = y_steps[i - 1] + y
    fig, ax = plt.subplots()
    ax.scatter(x_steps, y_steps)
    ax.set_title('scatter plot')
    plt.show()


def shuffle(lett_list, last):
    output = lett_list[1:last]
    random.shuffle(output)
    return ''.join(output)


def permutator(word):
    letters = list(word)
    if 1 <= len(letters) <= 2:
        return word
    if re.match(r"\w", letters[-1]):
        return f"{letters[0]}{shuffle(letters, -1)}{letters[-1]}"
    else:
        return f"{letters[0]}{shuffle(letters, -2)}{''.join(letters[-2:])}"


def text_shuffler(text):
    words_list = text.split(" ")
    print(*list(map(permutator, words_list)), sep=" ")


if __name__ == "__main__":
    compare_modules()
    check_sorting()
    random_walk()
    text_shuffler("По результатам илссоевадний одонго анлигсйокго унвиертисета, не иеемт занчнеия, ")
