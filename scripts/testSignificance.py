
"""
This script has been taken from the repository: 
https://github.com/rtmdrr/testSignificanceNLP.git

It was slightly amended for the purposes of this project.
"""

import csv
import os
import sys
import numpy as np
from scipy import stats


def main():
    if len(sys.argv) < 3:
        print("You did not give enough arguments\n ")
        sys.exit(1)
    filename_A = sys.argv[1]
    filename_B = sys.argv[2]
    alpha = sys.argv[3]


    with open(filename_A) as f:
        data_A = f.read().splitlines()

    with open(filename_B) as f:
        data_B = f.read().splitlines()

    data_A = list(map(float,data_A))
    data_B = list(map(float,data_B))

    ### Statistical test

    output_file = sys.argv[4]

    with open(output_file, "a") as outf:
        writer = csv.writer(outf, delimiter="\t")
        if os.path.getsize(output_file) == 0:
            writer.writerow(("model1", "accuracy1", "model2", "accuracy2", "better_model", "wilcoxon_score", "is_significant"))

        mname_A = os.path.basename(filename_A)
        mname_B = os.path.basename(filename_B)

        # Calculations for accuracy counts
        total_preds = len(data_A)
        correct_A = sum(data_A)
        correct_B = sum(data_B)
        acc_A = round((correct_A / total_preds) * 100, 3)
        acc_B = round((correct_B / total_preds) * 100, 3)

        better_model = mname_A if acc_A > acc_B else mname_B

        output = [mname_A, acc_A, mname_B, acc_B, better_model]

        # Wilcoxon: Calculate the Wilcoxon signed-rank test.
        wilcoxon_results = stats.wilcoxon(data_A, data_B)

        if float(wilcoxon_results[1]) <= float(alpha):
            output.extend([wilcoxon_results[1], "yes"])
        else:
            output.extend([wilcoxon_results[1], "no"])

        writer.writerow(output)


if __name__ == "__main__":
    main()









