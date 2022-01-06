import argparse
import csv
import json

from transformers import pipeline
from typing import List
from typing import Tuple


XLMR_MODELS = ["xlm-roberta-base", "xlm-roberta-large"]
GER_BERT_MODELS = [
    "bert-base-german-dbmdz-cased",
    "bert-base-german-dbmdz-uncased",
    "bert-base-german-cased",
    "bert-base-multilingual-uncased",
    "bert-base-multilingual-cased",
]
DUTCH_BERT_MODELS = [
    "wietsedv/bert-base-dutch-cased",
    "bert-base-multilingual-uncased",
    "bert-base-multilingual-cased",
]

LANG_MODEL_MAP = {"german": GER_BERT_MODELS, "dutch": DUTCH_BERT_MODELS}


def read_sentences_and_obj_positions(filename: str) -> List[Tuple[str, str]]:
    """
    Read sentences for predicting masked words from a file.
    The object position in each sentence is given as extra information.

    :param filename: TSV file containing sentences with vlight constructions.
    :return: A list of tuples of sentences and the position of their object.
    """
    with open(filename) as sentence_file:
        reader = csv.reader(sentence_file, delimiter="\t")

        # line[4] is a sentence and line[3] the position of the object
        # in this sentence.
        # Object position indexing starts at 1 so it must be reduced by 1.
        return [(line[4], int(line[3]) - 1) for line in reader]


def mask_sentence(sentence: str, mask_token: str, obj_pos: int, n_masked_tokens: int):
    """
    Mask all objects with the mask token.

    :param sentence: An input sentence.
    :param mask_token: A string that serves as a mask in transformer models.
    :param obj_pos: The position of the object in the sentence.
    """
    split_sent = sentence.split()
    # Replace all objects with the mask token.
    split_sent[obj_pos] = mask_token
    if n_masked_tokens > 1:
        for _ in range(n_masked_tokens-1):
            split_sent.insert(obj_pos, mask_token)

    return " ".join(split_sent)


def generate_with_pipeline(sents_and_obj_positions: List[Tuple[str, str]], model_type: str):
    """
    Generate suggestions for masked tokens with the default
    pipeline provided by the transformers library.

    :param sents_and_obj_positions: Sentences in the format specified above and 
    the positions of their objects.
    :param model_type: The type of model used for predictions.
    """
    nlp = pipeline("fill-mask", model=model_type)

    output = {}

    for sentence, obj_pos in sents_and_obj_positions:
        masked_sent = mask_sentence(sentence, nlp.tokenizer.mask_token, obj_pos)

        # Generate and print predictions for the masked token.
        output[sentence] = nlp(masked_sent)

    return output


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find out about selective preferences of Transformer models "
        "for subject-object resolution."
    )
    parser.add_argument("in_file", type=str)
    parser.add_argument("language", choices=["german", "dutch"],     type=str)
    parser.add_argument("--model_type", "-m", type=str)
    parser.add_argument("--output_file", "-o", type=str)
    parser.add_argument("--n_masked_tokens", "-t", type=str)
    args = parser.parse_args()

    model_type = args.model_type
    n_masked_tokens = args.n_masked_tokens

    while (
        not model_type or model_type not in XLMR_MODELS + LANG_MODEL_MAP[args.language]
    ):
        print("\nChoose one of the following models:\n")
        print("XLM-RoBERTa: " + repr(XLMR_MODELS))
        print("BERT:        " + repr(LANG_MODEL_MAP[args.language]) + "\n")

        model_type = input("Type the model name here: ")

    sents_and_obj_positions = read_sentences_and_obj_positions(args.in_file)
    pred_dict = generate_with_pipeline(sents_and_obj_positions, model_type, n_masked_tokens)

    if args.output_file:
        while not args.output_file.endswith(".json"):
            args.output_file = input(
                "Your file name does not have the "
                "correct file ending `.json`\nPlease change the file name: "
            )
        with open(args.output_file, "w") as json_out:
            json.dump(pred_dict, json_out, ensure_ascii=False, indent=4)
    else:
        print(pred_dict)
