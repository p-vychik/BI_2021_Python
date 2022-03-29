from typing import Tuple, Generator
import random


class FastaRandomPrinter:
    """Class object reads fasta file infinite,
        path - string with path to file,
        mutation_prob - float in range [0, 1] defining seq probability to mutate
        float probability
    """
    def __init__(self, path, mutation_prob):
        self.path = path
        self.id = ''
        self.seq = []
        self.mutation_prob = mutation_prob
        self.f = open(self.path, 'r', encoding='utf-8')
        self.entry = ''

    def get_mutated_seq(self, seq):
        amino_acids = ("G", "P", "A", "V", "L", "I", "M",
                       "C", "F", "Y", "W", "H", "K", "R",
                       "Q", "N", "E", "D", "S", "T")
        replacements_num = random.randint(1, len(seq) - 1)
        positions = random.sample(tuple(range(0, len(seq) - 1)), k=replacements_num)
        seq_list = [x if i not in positions
                    else random.choice(amino_acids) for i, x in enumerate(seq)]
        return ''.join(seq_list)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = self.f.readline().rstrip('\n')
            if line:
                if line.startswith('>'):
                    if self.id:
                        if random.uniform(0, 1) < self.mutation_prob:
                            self.entry = f"{self.id} {self.get_mutated_seq(''.join(self.seq))}"
                        else:
                            self.entry = f"{self.id} {''.join(self.seq)}"
                    self.id = line
                    self.seq = []
                    return self.entry
                else:
                    self.seq.append(line)
            else:
                self.f.close()
                self.f = open(self.path, 'r', encoding='utf-8')


def fasta_reader(path_fasta) -> Generator[Tuple[str, str], str, str]:
    """Generator function to read fasta files
        Args:
            path_fasta - the path to file in fasta format

        Yields:
             tuple with id: str, seq: str
    """
    with open(path_fasta, 'r', encoding='utf-8') as f:
        id = ''
        seq = []
        for line in f:
            line = line.replace('\n', '')
            if line.startswith('>'):
                if id:
                    yield id, ''.join(seq)
                id = line
                seq = []
            else:
                seq.append(line)
        if id:
            yield id, ''.join(seq)


def iter_append(iter, element):
    """Generator function adding one element to the end of iterable's queue
       Args:
            iter - any iterable object
            element - any iterable item

       Yields:
            element of iterable
    """
    if iter:
        yield iter[0]
        yield from iter_append(iter[1:], element)
    elif element:
        yield element


def nested_list_unpacker(nested_list):
    """Generator function to unpack nested list with unlimited depth
       Args:
            nested_list - a list with element lists of any depth

       Returns:
            a list with unpacked elements
    """
    def unpack_list(nested_list):
        for elem in nested_list:
            if type(elem) == list:
                yield from nested_list_unpacker(elem)
            else:
                yield elem

    return list(unpack_list(nested_list))


if __name__ == "__main__":
    # test for the first task
    reader = fasta_reader("sequences.fasta")
    print(type(reader))
    for id, seq in reader:
        print(f"{id} {seq[:50]}")
    # test for the third task
    test_list = [1, 2, 3, 4, 5]
    test_iter = iter_append(test_list, [10, 100])
    print(type(test_iter))
    for elem in test_iter:
        print(elem)
    # test for the fourth task
    nested_list = [1, 2, 3, 4, 5, [], [[7, 8, [9, 10, [[11]]]]]]
    print(nested_list)
    print(nested_list_unpacker(nested_list))
    # test for the second task
    printer = FastaRandomPrinter("sequences.fasta", 0.3)
    for i, item in enumerate(printer):
        print(item)
        if i > 500:
            print("Over 3 complete cycles over fasta finished. Break iteration")
            break
