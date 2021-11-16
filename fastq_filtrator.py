import argparse


def passed_gc_filter(seq_block, threshold_dict):
    seq = seq_block.copy()
    seq[1] = seq[1].rstrip('\n')
    seq[3] = seq[3].rstrip('\n')
    threshold = threshold_dict["gc_bounds"]
    gc_content = ((seq[1].upper().count('G') + seq[1].upper().count('C')) / len(seq[1])) * 100
    if threshold[0] <= gc_content <= threshold[1]:
        return True
    else:
        return False


def passed_quality_filter(seq_block, threshold_dict):
    seq = seq_block.copy()
    seq[1] = seq[1].rstrip('\n')
    seq[3] = seq[3].rstrip('\n')
    threshold = threshold_dict["quality_threshold"]
    seq_score = []
    for score in seq[3]:
        seq_score.append(ord(score) - 33)
    if len(seq_score) != 0:
        avr_quality = sum(seq_score) / len(seq_score)
        if avr_quality >= threshold:
            return True
        else:
            return False
    else:
        return False


def passed_length_filter(seq_block, threshold_dict):
    seq = seq_block.copy()
    seq[1] = seq[1].rstrip('\n')
    seq[3] = seq[3].rstrip('\n')
    threshold = threshold_dict["length_bounds"]
    length = len(seq[1])
    if threshold[0] <= length <= threshold[1]:
        return True
    else:
        return False


FILTERS = [passed_gc_filter,
           passed_quality_filter,
           passed_length_filter]


def main(input_fastq, output_file_prefix, gc_bounds=(0, 100), length_bounds='2**32', quality_threshold=0,
         save_filtered=False):
    threshold_dict = {"gc_bounds": gc_bounds,
                      "length_bounds": length_bounds,
                      "quality_threshold": quality_threshold}
    filtered_reads = []
    passed_filters_reads = []
    with open(input_fastq, 'r') as f:
        seq_block = []
        counter = 1
        for line_num, seq in enumerate(f):
            seq_block.append(seq)
            if counter == 4:
                if all(result is True for result in [filter(seq_block, threshold_dict) for filter in FILTERS]):
                    passed_filters_reads.append(''.join(seq_block))
                elif save_filtered:
                    filtered_reads.append(''.join(seq_block))
                seq_block = []
                counter = 1
            else:
                counter += 1
    with open(f"{output_file_prefix}_passed.fastq", 'w') as output_file:
        output_file.writelines(''.join(passed_filters_reads))
    if save_filtered:
        with open(f"{output_file_prefix}_failed.fastq", 'w') as output_file:
            output_file.writelines(''.join(filtered_reads))


def createparser():
    parser = argparse.ArgumentParser(
             prog='fastq filtrator',
             usage='\nfastq_filtrator.py input_fastq, output_file_prefix, gc_bounds length_bounds'
                   'quality_threshold save_filtered',
             description='''This script allows FASTQ file reads filtering''',
             epilog='Pavel Vychyk, 2021')
    parser.add_argument('input_fastq',
                        help='path to input .fastq file.',
                        type=str)
    parser.add_argument('output_file_prefix',
                        help='path to output for reads passed filtering',
                        type=str)
    parser.add_argument('gc_bounds',
                        help='lower and upper bound, separated by comma,'
                               ' for reads filtering by GC content, default 0,100',
                        default='0,100',
                        nargs='?',
                        type=str)
    parser.add_argument('length_bounds',
                        help='lower and upper bound, separated by comma,'
                               ' for reads filtering by length, default 0,2**32',
                        default='0,2**32',
                        nargs='?',
                        type=str)
    parser.add_argument('quality_threshold',
                        help='threshold for reads filtering by Q-score, default 0',
                        default=0,
                        type=int,
                        nargs='?')
    parser.add_argument('save_filtered',
                        help='save reads not passed filters in separate file, default False',
                        type=bool,
                        default=False,
                        nargs='?')
    return parser


args = createparser()
enter = args.parse_args()
if "," in enter.gc_bounds:
    gc_bounds = list(map(int, enter.gc_bounds.split(',')))
else:
    gc_bounds = [0, int(enter.gc_bounds)]
if "," in enter.length_bounds:
    length_bounds = list(map(eval, enter.length_bounds.split(',')))
else:
    length_bounds = [0, int(enter.length_bounds)]
main(enter.input_fastq, enter.output_file_prefix, gc_bounds, length_bounds, enter.quality_threshold,
     enter.save_filtered)
