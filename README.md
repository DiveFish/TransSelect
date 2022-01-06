# Transformer Selectional Preferences for Predictions
Code written by [janniss91](https://github.com/janniss91/).


The objective of this project is to investigate whether Transformer models have selectional preferences when making predictions.  
Traditional parsers make use of information about the associative strength between two words.  
E.g. there is a strong association between the words `eat` and `spaghetti` if `spaghetti` is an object. However, there is a weak association if it is a subject.

The question is whether Transformers make use of the same kind of information for their predictions.

## Setup

For the setup of this repository simply type:

    make

This will

- set up a virtual environment for this repository,
- install all necessary project dependencies.

Make sure that Python 3.7 or higher is installed in your virtual environment. Otherwise, there might be problems installing the `transformers` library.

## Virtual Environment

After having run the `make` command you will have installed a virtual environment.  
Always work in this environment to make sure to use the correct python interpreter and have access to the relevant dependencies.

To enter the environment in a shell, type:

    . env/bin/activate

If you work in an IDE like e.g. Pycharm, make sure that it also makes use of the correct Python interpreter.

To deactivate the virtual environment, type:

    deactivate

## Clean and Re-install

To reset the repository to its inital state, type:

    make dist-clean

This will remove the virtual environment and all dependencies.  
With the `make` command you can re-install them.

To remove temporary files like .pyc or .pyo files, type:

    make clean

## Pipeline (Recommended Usage)

You can run the pipeline of the whole repository very easily with just one command:

    ./scripts/pipeline.sh your-input-file.tsv language search_term

**your_input_file**: a tsv gold file from the SORTS repository  
**language**: german or dutch  
**search_term**: name for sentence type (e.g. vlight or base-acc)

This includes the following steps:

1. Filter specific sentence type.
2. Predict the next word for the filtered sentences with all models.
3. Generate statistics for the predictions that were just made for this sentence type.
4. Generate the files with binary information about whether the correct prediction was found.
5. Test significance for all models.

## Data Set and Data Preparation

The data that was used in this project comes from the SORTS project (https://github.com/DiveFish/SORTS).

### German

More specifically the `german_part-ambiguous_gold.tsv` file was filtered for sentence entries with light verbs.
The filtering was done by using the script `data/data_prep_tools/filter_data.py`.
The data can be found in the `data` folder; it is called `filtered_vlight_data.tsv`.

### Dutch

For dutch the `dutch_part-ambiguous_gold.tsv` file was filtered for sentence entries with light verbs.

To regenerate the filtered data, simply run:

<pre>
python3 data/data_prep_tools/filter_data.py <i>path_to_sorts_data</i>.tsv data/<i>filtered_file</i>.tsv <i>language</i> <i>search_term</i>
</pre>

The file names must be adapted to your case.

## Predicting

### German

Predictions have been done for the following transformer models:

- xlm-roberta-base
- xlm-roberta-large
- bert-base-german-dbmdz-cased
- bert-base-german-dbmdz-uncased
- bert-base-german-cased
- bert-base-multilingual-uncased
- bert-base-multilingual-cased

### Dutch

Predictions have been done for the following transformer models:

- xlm-roberta-base
- xlm-roberta-large
- wietsedv/bert-base-dutch-cased
- bert-base-multilingual-uncased
- bert-base-multilingual-cased

To make a prediction for a single of these models, run e.g.:

<pre>
python3 scripts/selective_preferences.py data/<i>filtered_file</i>.tsv -m xlm-roberta-base -o predictions/<i>name_of_output_file</i>.json
</pre>

If you do not want to store the results in a json file but print the output, just remove the `-o` flag and output file name from the command.

To make predictions for all models, run:
<pre>
./scripts/predict_all_models_pipeline.sh data/<i>filtered_file</i>.tsv <i>language</i> <i>search_term</i>
</pre>

## Setting up Prediction Statistics

To set up prediction statistics, run e.g.:

<pre>
python3 scripts/generate_stats.py data/<i>filtered_file</i>.tsv <i>language</i> <i>search_term</i>
</pre>

## Creating Binary Output Files for Subsequent Significance Testing

To create the binary file for one model, run:

<pre>
python3 binary_output_per_sentence.py statistics/binary_results/prediction_file.json data/<i>filtered_file</i>.tsv <i>binary_output_file</i>
</pre>

You can also create the binary files for all models at once.

<pre>
./write_all_binary_files.sh data/<i>filtered_file</i>.tsv <i>language</i> <i>search_term</i>
</pre>

## Significance Testing

You can test superiority of one model output over the other by running a significance test. To do this, run:

<pre>
./scripts/significance_test_all_files.sh <i>language</i> <i>search_term</i>
</pre>

The output can be found in the file ```statistics/significance_test_results.tsv```.  
It is split up into four columns: model1, model2 and p-value, is_significant.  
Usually a value under 0.05 indicates a significant result.  
Everything above is considered insignificant.

Note that the script ```scripts/testSignificance.py``` has been taken from this repository: https://github.com/rtmdrr/testSignificanceNLP.git

It has been amended (drastically shortened) for the purposes of this project and only makes use of the Wilcoxon significance test.  

IMPORTANT: The script was written in Python 2.7. It can be run with python 3.8 but if you encounter any problems, try running it with a python 2.7 interpreter outside of the virtual environment (make sure the library ```scipy``` is installed).
