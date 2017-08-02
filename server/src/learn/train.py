#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

import sys, os
from learner import InteractiveLearner, InteractiveLearnerNaiveBayes, DenseArch
from io_utils import *

if len(sys.argv) != 5:
	exit('Params: param_str train_dir validation_dir model_dir')

param_str = sys.argv[1]
input_dir = sys.argv[2]
valid_dir = sys.argv[3]
model_dir = sys.argv[4]

if not os.path.exists(input_dir):
	exit('Input directory does not exist: "{}"'.format(input_dir))

documents = read_documents(input_dir)
inst_labels = read_instance_labels(input_dir)
feat_labels = read_feature_labels(input_dir)
# feat_tasks = feat_labels.keys()
feat_tasks = []

valid_doc = read_documents(valid_dir)
valid_lbl = read_instance_labels(valid_dir)
if len(valid_lbl) > 0:
	valid_set = (valid_doc, valid_lbl)
else:
	valid_set = None

if 'sparse' in param_str:
	# learner = InteractiveLearnerNaiveBayes(max_vocab = 10000, feat_label_pseudo_count = 10.)
	learner = InteractiveLearner(is_sparse = True, max_vocab = 10000, num_epoch = 10, batch_size = 128)
else:
	learner = InteractiveLearner(is_sparse = False, max_vocab = 10000, dense_architecture = DenseArch.ONE_LAYER)
	# learner = InteractiveLearner(is_sparse = False, max_vocab = 10000, dense_architecture = DenseArch.TWO_LAYER_AVG_EMB)

learner.fit(documents, inst_labels, feat_labels, feat_tasks, model_dir, valid_set)

