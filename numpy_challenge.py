import numpy as np
from numpy.linalg import multi_dot


def check_shape(a, b):
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        if len(a.shape) == len(b.shape):
            if len(a.shape) == 2:
                if a.shape[1] == b.shape[0]:
                    return True
                else:
                    return False
            else:
                return True
        else:
            if len(a.shape) == 1:
                return False
            elif a.shape[1] == b.shape[0]:
                return True
            else:
                return False
    else:
        return False


def matrix_multiplication(a, b):
    if not isinstance(a, np.ndarray):
        try:
            a = np.array(a)
        except TypeError:
            return (None)
    if not isinstance(b, np.ndarray):
        try:
            b = np.array(b)
        except TypeError:
            return (None)
    if check_shape(a, b):
        return np.dot(a, b)


def multiplication_check(matrix_list):
    for i, mat in enumerate(matrix_list[1:]):
        if not isinstance(matrix_list[i], np.ndarray):
            matrix_list[i] = np.array(matrix_list[i])
        if not isinstance(matrix_list[i + 1], np.ndarray):
            matrix_list[i + 1] = np.array(matrix_list[i + 1])
        if not check_shape(matrix_list[i], mat):
            return False
    return True


def multiply_matrices(matrix_list):
    if multiplication_check(matrix_list):
        return (multi_dot(matrix_list))
    else:
        return None


def compute_2d_distance(a, b):
    if len(a) == 2 and len(b) == 2:
        return (np.sqrt(np.power((b[0] - a[0]), 2) + np.power((b[1] - a[1]), 2)))


def compute_multidimensional_distance(a, b):
    if len(a) == len(b):
        return np.sqrt(np.sum((b - a) ** 2))


def compute_pair_distances(a):
    d = np.zeros((a.shape[0], a.shape[0]))
    for i in range(0, a.shape[0]):
        for j in range(0, a.shape[0]):
            if i != j:
                d[i][j] = np.sqrt(np.sum((a[i] - a[j]) ** 2))
    return d


if __name__ == "__main__":
    # first way
    one_diag_1 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    # second one
    one_diag_2 = np.eye(3, 3)
    # third
    one_diag_3 = np.zeros((3, 3))
    for i in range(0, one_diag_3.shape[0]):
        one_diag_3[i][i] = 1

        
