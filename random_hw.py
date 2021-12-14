import numpy as np
import random
import time
import matplotlib.pyplot as plt
import re


def compare_modules():
    fig, ax = plt.subplots()
    time_array = []
    time_array_random = []
    time_array_np_loop = []
    # count of random numbers to generate
    numbers_count = 101
    cycles_repeat = 101
    for i in range(1, numbers_count):
        cycle_time_np = 0
        cycle_time_random = 0
        cycle_time_np_loop = 0
        # run cycles 1000 times and find average run time
        for _ in range(1, cycles_repeat):
            # np.random.rand with size parameter
            start = time.time()
            np.random.rand(i)
            cycle_time_np += (time.time() - start)
            # random.random in for loop
            start = time.time()
            for _ in range(i):
                random.random()
            cycle_time_random += (time.time() - start)
            # np.random.rand in loop
            start = time.time()
            for _ in range(i):
                np.random.rand()
            cycle_time_np_loop += (time.time() - start)
        time_array.append(cycle_time_np / cycles_repeat)
        time_array_random.append(cycle_time_random / cycles_repeat)
        time_array_np_loop.append(cycle_time_np_loop / cycles_repeat)

    x = [_ for _ in range(1, numbers_count)]
    ax.plot(x, time_array, label='numpy.random generation time')
    ax.plot(x, time_array_random, label='random.random() in loop')
    ax.plot(x, time_array_np_loop, label='numpy.random() in loop')
    ax.set_xlabel('number count')
    ax.set_ylabel('time, sec')
    plt.legend(loc="upper left")
    plt.show()


def is_sorted(input_list):
    for i in range(1, len(input_list)):
        if input_list[i] < input_list[i-1]:
            return False
    return True


def check_sorting():
    fig, ax = plt.subplots()
    y_time = []
    y_stdev = []
    for length in range(1, 10):
        input_list = np.random.randint(0, 10000, size=length)
        ind = np.random.randint(0, length, size=2)
        cycles_time = []
        for _ in range(1, 101):
            start = time.time()
            while not is_sorted(input_list):
                input_list[ind[0]], input_list[ind[1]] = input_list[ind[1]], input_list[ind[0]]
                ind = np.random.randint(0, length, size=2)
            cycles_time.append(time.time() - start)
        y_time.append(sum(cycles_time) / 100)
        y_stdev.append(np.std(cycles_time))
    x = [_ for _ in range(1, 10)]
    ax.errorbar(x, y_time, yerr=y_stdev)
    ax.set_xlabel('list size')
    ax.set_ylabel('time, sec')
    ax.set_title("Monkey sorting time depending on the list size")
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
    ax.set_title('Random walk in 2D')
    plt.show()


def shuffle(lett_list, last):
    output = lett_list[1:last]
    random.shuffle(output)
    return ''.join(output)


def sierpinski_triangle(steps):
    # initial triangle points
    x = [1, 6, 11]
    y = [1, 9.9, 1]
    points_index = [0, 1, 2]
    # start point
    x_p = [1]
    y_p = [1]
    for _ in range(steps):
        ind = random.choice(points_index)
        x_p.append((x[ind] + x_p[-1]) / 2)
        y_p.append((y[ind] + y_p[-1]) / 2)
    fig, ax = plt.subplots()
    ax.scatter(x_p, y_p)
    ax.set_title("Sierpinski's Triangle, random generation")
    plt.show()


def permutator(word):
    letters = list(word)
    if 0 <= len(letters) <= 3:
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
    sierpinski_triangle(5000)
    text_shuffler("По результатам илссоевадний одонго анлигсйокго унвиертисета, не иеемт занчнеия, ")
