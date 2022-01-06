#!/bin/bash

# This pipeline script is made to run the whole pipeline of files in this
# repository.

# This includes the following steps:
# 1. Filter specific sentence type (filter_data.py)
# 2. Predict the next word for the filtered sentences with all models.
# 3. Generate statistics for the predictions that were just made for this sentence type.
# 4. Generate the files with binary information about whether the correct prediction was found.
# 5. Test significance for all models.

# Make sure to include these three parameters.
input_file=$1
language=$2
search_term=$3

FILTERED=$"data/filtered_"$search_term"_data_"$language".tsv"

# 1.
python3 data/data_prep_tools/filter_data.py $input_file $language $search_term
# 2.
./scripts/predict_all_models_pipeline.sh $FILTERED $language $search_term
# 3.
python3 scripts/generate_stats.py $FILTERED $language $search_term
# 4.
./scripts/write_all_binary_files.sh $FILTERED $language $search_term 
# 5.
./scripts/significance_test_all_files.sh $language $search_term