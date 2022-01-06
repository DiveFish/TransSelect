import argparse
import json

from selective_preferences import read_sentences_and_obj_positions
from typing import Dict
from typing import Tuple


def write_binary_results(
    pred_file: str, original_file: str, out_file: str
) -> Tuple[int, Dict[int, int]]:
    """
    Count the sentences where the actual masked object was in one of the 5 predictions.
    Also count the ranks where the actual masked object was found.
    :param pred_file: A json file with predictions for masked objects.
    :param original_file: The original tsv file with the sentences.
    :return: The counts for correct predictions and correct prediction ranks.
    """
    with open(pred_file) as pred:
        pred_data = json.load(pred)
        # Note that the original file is opened inside this imported function.
        sents_and_obj_positions = read_sentences_and_obj_positions(original_file)

        binary_results = []

        for sentence, obj_position in sents_and_obj_positions:
            pred_list = pred_data[sentence]

            bin_result = 0

            for pred in pred_list:
                # Three symbols are sometimes added to the predicted token string.
                # They must be stripped before comparison.
                token_str = pred["token_str"].strip("▁Ġ#").lower()

                if token_str == sentence.split()[obj_position].lower():
                    bin_result = 1
                    break

            binary_results.append(bin_result)

    with open(out_file, "w") as outf:
        for bin_result in binary_results:
            outf.writelines(str(bin_result) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Set up a list of binary (correct/incorrect) values for predictions."
    )
    parser.add_argument("input_file", type=str)
    parser.add_argument("original_file", type=str)
    parser.add_argument("output_file", type=str)
    args = parser.parse_args()

    write_binary_results(args.input_file, args.original_file, args.output_file) 
