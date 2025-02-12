#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import filecmp
import os
import sys

from bayesopt_if.physbo_interface import PhysboInterface


def get_data_from_result_list(index):
    with open('./data/results.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    return float(l[index+1][0])


def test_physbo_interface():
    # dir setting
    candidates_path  = './data/candidates.csv'
    correct_candidates_path = './data/candidates-correct.csv'
    policy_load_dir = './data/load'
    policy_save_dir = './data/result'

    # Generate physbo
    pi = PhysboInterface(candidates_path, policy_load_dir, policy_save_dir, use_saved_policy=False, search_score='EI')
    pi.start_bayesopt()

    # Procedure of search and register data to PHYSBO
    # - Following procedure is important for correct generation of result data.
    # - search -> write (and update -> visualize)

    # Search with Random search for initial step
    for i in range(3):
        pi.search_next_param_random()
        result = get_data_from_result_list(pi.get_next_index())  # get result/evaluation data from experiment. (Result list is used for this test program).
        pi.write_result(result)  # write result to PHYSBO
    # Search with Bayesian optimization
    for i in range(17):
        pi.search_next_param_bayes()
        result = get_data_from_result_list(pi.get_next_index())
        pi.write_result(result)

    #input('Press enter to save and finish\n')
    pi.save_data(policy_save_dir)

    assert filecmp.cmp(candidates_path, correct_candidates_path)
