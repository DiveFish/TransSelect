import csv
import json
import os
import sys

from selective_preferences import GER_BERT_MODELS
from selective_preferences import DUTCH_BERT_MODELS
from selective_preferences import LANG_MODEL_MAP
from selective_preferences import read_sentences_and_obj_positions
from selective_preferences import XLMR_MODELS
from typing import Dict
from typing import Tuple


def count_correct_predictions(
    pred_file: str, original_file: str
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

        num_correct_preds = 0
        rank_correct_pred = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for sentence, obj_position in sents_and_obj_positions:
            pred_list = pred_data[sentence]

            pred_found = False

            for rank, pred in enumerate(pred_list, start=1):
                # Three symbols are sometimes added to the predicted token string.
                # They must be stripped before comparison.
                token_str = pred["token_str"].strip("▁Ġ#").lower()

                if token_str == sentence.split()[obj_position].lower():
                    num_correct_preds += 1
                    rank_correct_pred[rank] += 1
                    pred_found = True

                if pred_found:
                    break

        return len(pred_data), num_correct_preds, rank_correct_pred


def write_model_comparison(original_path: str, stats_file: str, language: str, search_term: str):
    """
    Write the statistics to a tsv file.

    :param original_path: This is the TSV file that holds the actual sentences before
    masking, which also holds the metadata about the file.
    :param stats_file: The name of the output file.
    :param language: dutch or german
    """
    with open(stats_file, "w") as stats:
        writer = csv.writer(stats, delimiter="\t")
        writer.writerow(
            ["model","total", "correct", "accuracy", "rank 1", "rank 2", "rank 3", "rank 4", "rank 5"]
        )

        for model in XLMR_MODELS + LANG_MODEL_MAP[language]:
            # The one dutch model has a slash in its name, which makes the system
            # think it was a subdirectory. Therefore, the first part must be removed
            # from the name.
            model_name = model.split("/")[1] if "/" in model else model

            pred_path = os.path.join(
                "predictions",
                language,
                search_term,
                model_name + "-" + language + "-out.json",
            )

            total_preds, num_correct_preds, rank_counts = count_correct_predictions(
                pred_path, original_path
            )

            writer.writerow(
                [
                    model,
                    total_preds,
                    num_correct_preds,
                    round(((num_correct_preds / total_preds) * 100), 3),
                    rank_counts[1],
                    rank_counts[2],
                    rank_counts[3],
                    rank_counts[4],
                    rank_counts[5],

                ]
            )


if __name__ == "__main__":

    # original: one of the filtered files in the data/ directory
    original_path = sys.argv[1]  
    language = sys.argv[2]
    search_term = sys.argv[3]

    write_model_comparison(
        original_path, "statistics/correct_predictions_" + language + "_" + search_term + ".tsv", language, search_term
    )
