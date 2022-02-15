from math import sqrt
from Bio.Seq import Seq
from Bio import SeqIO
import os.path
import matplotlib.pyplot as plt
import numpy as np


class IncorrectSides(Exception):
    pass


class IncorrectPath(Exception):
    pass


class IncorrectBases(Exception):
    pass


class triangle:
    def __init__(self, a, b, c):
        try:
            if (a + b < c) or (a + c < b) or (b + c < a):
                raise IncorrectSides
            else:
                self.a = a
                self.b = b
                self.c = c
        except IncorrectSides:
            print("triangle doesn't exist")

    def square(self):
        p = self.perimeter() / 2
        sq = sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        return sq

    def perimeter(self):
        return self.a + self.b + self.c


class SeqRNA:
    valid_bases = set('AUGC')

    def __init__(self, input_seq=''):
        try:
            if not set(input_seq.upper()).issubset(self.valid_bases):
                raise IncorrectBases
            else:
                self.seq = Seq(input_seq.upper())
        except IncorrectBases:
            print('RNA seq contains non legal bases')

    def _translate(self):
        return self.seq.translate()

    def _reverse_transcribe(self):
        return self.seq.back_transcribe().reverse_complement()


class PositiveSet(set):
    def __init__(self, *args):
        self.number_set = {num for num in args if num > 0}

    def __repr__(self):
        return str(self.number_set)

    def add(self, elem):
        if elem > 0:
            self.number_set.add(elem)


def print(arg):
    return arg.fasta_path


class FastaStats:
    def __init__(self, input_path):
        try:
            if not os.path.isfile:
                raise IncorrectPath
            else:
                self.fasta_path = input_path
        except IncorrectPath:
            print("File doesn'exist")

    def count_entries(self):
        with open(self.fasta_path):
            seqs = list(SeqIO.parse(self.fasta_path))
            return len(seqs)

    def hist_lengths(self):
        with open(self.fasta_path):
            entries = list(SeqIO.parse(self.fasta_path, "fasta"))
            lengths = np.array([len(entry.seq) for entry in entries])
            if lengths.shape[0]:
                labels, counts = np.unique(lengths, return_counts=True)
                plt.bar(range(len(labels)), counts, align='center')
                plt.xticks(range(len(labels)), labels)
                plt.show()

    def count_gc(self):
        with open(self.fasta_path):
            entries = list(SeqIO.parse(self.fasta_path, "fasta"))
            lengths = np.array([((entry.seq.upper().count("G"))
                                + (entry.seq.upper().count("C")))
                                / len(entry.seq) for entry in entries])
            return round((np.average(lengths) * 100), 2)

    def __repr__(self):
        return str(self.fasta_path)

    def fourmers_count(self):
        fmers = {}
        with open(self.fasta_path):
            entries = list(SeqIO.parse(self.fasta_path, "fasta"))
            for entry in entries:
                seq = str(entry.seq)
                for i in range(len(seq) - 4 + 1):
                    fmer = seq[i:i + 4]
                    fmers[fmer] = fmers.get(fmer, 0) + 1
        if fmers.items():
            fmers = dict(sorted(fmers.items(), key=lambda x: x[1], reverse=True))
            labels, counts = list(fmers.keys()), list(fmers.values())
            plt.rcParams["figure.figsize"] = [37.50, 4.50]
            plt.rcParams["figure.autolayout"] = True
            plt.tick_params(axis='x', which='major', pad=10)
            plt.bar(range(len(labels)), counts, align='center')
            plt.xticks(range(len(labels)), labels, rotation='vertical')
            plt.xlabel("X-axis", labelpad=10)
            plt.show()
