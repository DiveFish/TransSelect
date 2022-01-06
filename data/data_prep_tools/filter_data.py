import csv
import re
import sys


def filter_tsv_data(in_file: str, out_file: str, token_num: int = 5):
    """
    Filter all sentences from a TSV file.
    - exactly 5 (token_num) tokens
    - the word order SVO
    - vlight constructions.

    :param in_file: TSV input file.
    :param out_file: TSV output file with filtered lines.
    :param token_num: Number of tokens of the sentence.
    """
    with open(in_file) as gold, open(out_file, "w") as filtered:
        reader = csv.reader(gold, delimiter="\t")
        writer = csv.writer(filtered, delimiter="\t")

        svo = re.compile(".*\[S\].*\[V\].*\[O\].*")

        for line in reader:
            tokenized_sent = line[4].split()

            if (
                svo.match(line[0])
                and "vlight" in line[1]
                and len(tokenized_sent) == token_num
            ):
                writer.writerow(line)


def filter_all_vlight_constr(in_file: str, out_file: str, search_term: str):
    """
    Filter all sentences with vlight constructions from a TSV file.

    :param in_file: TSV input file.
    :param out_file: TSV output file with filtered lines.
    """
    with open(in_file) as gold, open(out_file, "w") as filtered:
        reader = csv.reader(gold, delimiter="\t")
        writer = csv.writer(filtered, delimiter="\t")

        for line in reader:
            if search_term in line[1]:
                writer.writerow(line)


if __name__ == "__main__":

    # These three input parameters are necessary for the script.
    in_file = sys.argv[1]
    language = sys.argv[2]
    search_term = sys.argv[3]
    out_file = "data/filtered_" + search_term + "_data_" + language + ".tsv" 

    filter_all_vlight_constr(in_file, out_file, search_term)

    # To use the filter_tsv_data method, it must be called here.
