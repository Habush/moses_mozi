__author__ = 'Xabush Semrie'
import time
import os
import subprocess
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from pathlib import Path

default_list = "['-j', '6', '--balance', '1', '-m', '1000', '-W1', '1', '--output-cscore', '1', '--result-count', '100', '--reduct-knob-building-effort=1', '--hc-widen-search=1', '--enable-fs=1', '--fs-algo=smd', '--fs-target-size=4', '--hc-crossover-min-neighbors=5000', '--fs-focus=all', '--fs-seed=init', '--complexity-ratio=1', '--hc-fraction-of-nn=.3', '--hc-crossover-pop-size=1000']"


class CrossValidaton:
    def __init__(self, project_id, file_path, test_size, splits, opts=None):

        os.chdir("output/")
        self.id = project_id
        self.output = self.id
        self.file = file_path

        if opts is None:
            self.opts = default_list
        else:
            self.opts = opts

        self.test_size = test_size

        self.threshold = 50.0

        self.dataset = pd.read_csv(self.file)

        self.cv = StratifiedShuffleSplit(n_splits=splits, test_size=test_size)

        self.test = []

        self.train_file, self.test_file = "train_temp_" + self.id, "test_temp_" + self.id

    def run_moses(self):
        opts = self.opts.translate(str.maketrans("", "", "[],"))
        opts = "-i {0} -o {1} ".format(self.train_file, self.output) + opts
        # print self.opts
        cmd = "moses " + opts
        print(cmd)
        ret = subprocess.Popen(args=cmd, shell=True).wait()
        print(ret)
        return ret

    def run_eval(self):

        combo_program = self._format_combo(self.output)
        temp_out = "eval_" + self.id
        if combo_program:
            cmd = "eval-table -i {0} -C {1} -o {2} -u{3}".format(self.test_file, self.output, temp_out, "case")
            print(cmd)
            ret = subprocess.Popen(args=cmd, shell=True).wait()

            return ret

        return -1

    def _format_combo(self, input_file):
        temp_combo = "temp_combo_" + self.id
        cmd = " cut -d\" \" -f1 --complement " + input_file + " > " + "temp_combo_" + self.id + " && cat " + temp_combo + " > " + input_file
        subprocess.Popen(args=cmd, shell=True).wait()
        os.remove(temp_combo)
        return input_file

    def build_matrix(self):
        files = list(Path(".").glob("eval_" + self.id + "[0-9]*"))

        matrix = np.array([np.genfromtxt(files[i].name, dtype=int, delimiter="\n", skip_header=1) for i in
                           range(len(files))]).T  # transpose the matrix

        for file in files: os.remove(file.name)

        return matrix

    def reduce_matrix(self):
        matrix = self.build_matrix()
        return np.array(
            [1 if ((matrix[i].sum() / matrix.shape[1]) * 100) > self.threshold else 0 for i in range(matrix.shape[0])])

    def score(self):
        scores = self.reduce_matrix()

        print(scores)

        print(len(scores))

        true_positive, true_negative, false_postive, false_negative = 0, 0, 0, 0

        for i in range(len(scores)):
            if self.test.iloc[i] == 0:
                if scores[i] == 0:
                    true_negative += 1
                else:
                    false_postive += 1

            else:
                if scores[i] == 1:
                    true_positive += 1
                else:
                    false_negative += 1

        recall = (true_positive / (true_positive + false_negative)) * 100

        precision = (true_positive / (true_positive + false_postive)) * 100

        accuracy = ((true_positive + true_negative) / (
            true_positive + true_negative + false_negative + false_postive)) * 100

        return recall, precision, accuracy

    def shuffle_split(self):
        x, y = self.dataset.values, self.dataset.case

        i = 0

        for train_index, test_index in self.cv.split(x, y):
            x_train, x_test = x[train_index], x[test_index]

            self.output = self.id + "_" + str(i)
            i += 1
            self.test = y[test_index]

            pd.DataFrame(x_train, columns=self.dataset.columns.values).to_csv(self.train_file, index=False)

            pd.DataFrame(x_test, columns=self.dataset.columns.values).to_csv(self.test_file, index=False)

            self.run()

    def run(self):

        # self.run_eval(test_file)
        if self.run_moses() == 0:
            if self.run_eval() == 0:
                print("Successfully finished process!")

                rec, pre, acc = self.score()

                print("Recall: {0:.1f}\tPrecison:{1:.1f}\tAccuracy:{2:.1f}".format(rec, pre, acc))

            else:
                print("Couldn't run evaluation")

        else:
            print("Couldn't run moses")


if __name__ == "__main__":
    bin_file = "../../data/bin_truncated.csv"
    cross_val = CrossValidaton("5abcde", bin_file, 0.3, 3)

    cross_val.shuffle_split()
