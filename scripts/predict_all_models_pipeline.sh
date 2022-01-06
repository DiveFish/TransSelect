#!/bin/bash

# This script creates a directory to store predictions for all models.
# The predictions for all models are stored in json files.

in_file=$1
language=$2
search_term=$3

PREDICT_DIR=$"predictions/$language/$search_term/"


if [ ! -d "$PREDICT_DIR" ]
then
    mkdir "$PREDICT_DIR"
else
    # Check whether directory is empty and ask for overwriting.
    if [ "$(ls -A $PREDICT_DIR)" ]
    then
        echo "The directory $PREDICT_DIR already contains files."
        echo "It is possible that you overwrite files. Continue anyway? [yes/no]  "
        read overwrite
        if [ ! "$overwrite" = "yes" ]
        then
            exit
        fi
    fi
fi

# Actual predictions take place here.   

if [ $language = "german" ]
then
    MODELS=(
        "xlm-roberta-base"
        "xlm-roberta-large"
        "bert-base-german-dbmdz-cased"
        "bert-base-german-dbmdz-uncased"
        "bert-base-german-cased"
        "bert-base-multilingual-uncased"
        "bert-base-multilingual-cased"
    )
else
    MODELS=(
        "xlm-roberta-base"
        "xlm-roberta-large"
        "wietsedv/bert-base-dutch-cased"
        "bert-base-multilingual-uncased"
        "bert-base-multilingual-cased"
    )
fi

for model in "${MODELS[@]}"
do
    # If a slash is in the model name, it must be split by the slash.
    # Otherwise the slash will be interpreted as a directory split symbol.
    if [[ $model == *"/"* ]]
    then 
        # Cut by slash and only take the last field of the output.
        model_name=$(echo $model | rev | cut -d "/" -f 1 | rev)
    else
        model_name=$model
    fi

    json_file="$model_name-$language-out.json"
    python3 scripts/selective_preferences.py $in_file $language -m "$model" -o "$PREDICT_DIR$json_file"
done
