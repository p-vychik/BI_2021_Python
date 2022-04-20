#!/usr/bin/env python3
import argparse
import time
import itertools
import datetime
from multiprocessing import Process, Manager
from typing import Tuple, Generator


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
                id = line.split(' ')[0][1:]
                seq = []
            else:
                seq.append(line)
        if id:
            yield id, ''.join(seq)


def count_chars(in_queue, out_list):
    while True:
        entry = in_queue.get()
        if entry:
            line_id, line = entry
            stats = {}
            chars = set(line)
            for char in chars:
                stats[char] = line.count(char)
            count_stats = ", ".join([f"{char}: {occurance}" for char, occurance in stats.items()])
            result = (f"Contig {line_id}:\t", count_stats)
            out_list.append(result)
        else:
            return


if __name__ == '__main__':
    start_time = time.time()
    print('Job started at: {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.")))
    parser = argparse.ArgumentParser(prog='hw_parallel.py',
                                    usage='\n%(prog)s <path to the fasta file> <number of threads to use>',
                                    epilog='Pavel Vychyk, 2022',
                                    description='counts ')
    parser.add_argument('--fasta_source', type=str, help='path to fasta file')
    parser.add_argument('--threads', type=str, help='path to folder with .hmm models ')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.00 (April 20, 2022)')
    args = parser.parse_args()
    # start with args
    threads = int(args.threads)
    fasta_path = args.fasta_source
    manager = Manager()
    results = manager.list()
    work = manager.Queue(threads)
    # create a queue
    pool = []
    for _ in range(threads):
        p = Process(target=count_chars, args=(work, results))
        p.start()
        pool.append(p)
    # read data with a generator chain
    reader_chain = itertools.chain(fasta_reader(fasta_path), (None, )*threads)
    for line in reader_chain:
        work.put(line)
    for p in pool:
        p.join()
    # get the results
    print("\n".join([f"{contig} {stat}" for contig, stat in results]))
    print(f"Total time, sec: {time.time() - start_time}")
