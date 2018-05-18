__author__ = 'Xabush Semrie'

import random
import subprocess
import os

default_list = "['-j', '6', '--balance', '1', '-m', '100', '-W1', '1', '--output-cscore', '1', '--result-count', '100', '--reduct-knob-building-effort=1', '--hc-widen-search=1', '--enable-fs=1', '--fs-algo=smd', '--fs-target-size=4', '--hc-crossover-min-neighbors=5000', '--fs-focus=all', '--fs-seed=init', '--complexity-ratio=1', '--hc-fraction-of-nn=.3', '--hc-crossover-pop-size=1000']"


class RandomSeed:
    def __init__(self, train_file, id, fold, opts=None, num_rands=None):

        if num_rands is None:
            self.num_rands = 5
        else:
            self.num_rands = num_rands

        self.rand_population = range(1, 1000)

        self.random_seeds = random.sample(self.rand_population, self.num_rands)

        self.id = id
        self.train_file = train_file

        if opts is None:
            self.opts = default_list
        else:
            self.opts = opts

        self.fold = str(fold)

        self.models = []

        self.files = []

    def run(self):

        for i in self.random_seeds:
            self.output = "{0}_fold_{1}_seed_{2}".format(self.id, self.fold, str(i))

            self.files.append(self.output)

            self.run_moses(i)

            self.output = self.format_combo(self.output)

            self.top_models()

            print("Run Fold: " + str(self.fold) + " Seed: " + str(i))

        file_name = "{0}_fold_{1}".format(self.id, self.fold)

        with open(file_name, 'w') as file:
            for model in self.models:
                file.write("{}".format(model))


        for file in self.files:
            os.remove(file)

    def top_models(self):
        N = 0
        with open(self.output, 'r') as combo_file:
            for line in combo_file:
                self.models.append(line)

                N += 1
                if N == 30: break;  # we will set the top M models here

    def run_moses(self, seed):
        opts = self.opts.translate(str.maketrans("", "", "[],"))
        opts = "-i {0} -o {1} --random-seed={2} ".format(self.train_file, self.output, str(seed)) + opts
        # print self.opts
        cmd = "moses " + opts
        print(cmd)
        ret = subprocess.Popen(args=cmd, shell=True).wait()
        print(ret)
        return ret

    def format_combo(self, input_file):
        temp_combo = "temp_combo_" + self.id
        cmd = " cut -d\" \" -f1 --complement " + input_file + " > " + "temp_combo_" + self.id + " && cat " + temp_combo + " > " + input_file
        subprocess.Popen(args=cmd, shell=True).wait()
        os.remove(temp_combo)
        return input_file
