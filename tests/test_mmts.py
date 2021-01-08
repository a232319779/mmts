# -*- coding: utf-8 -*-
# @Time    : 2021/01/06 23:27:28
# @Author  : ddvv
# @Site    : https://ddvvmmzz.github.io
# @File    : test_mmdt.py
# @Software: Visual Studio Code


import unittest
import os
from mmts import de_dosfuscation_work


class TestDedosfuscation(unittest.TestCase):

    def test_process(self):
        base_path = os.path.dirname(__file__)
        samples_path = os.path.join(base_path, "samples")
        file_path = os.path.join(samples_path, "dosfuscation_cmd.txt")
        with open(file_path, 'r') as target:
            cmd_str = target.read()
            print('\nori cmd: {0}'.format(cmd_str))
            clear_cmd_str = de_dosfuscation_work(cmd_str)
            print('de cmd: {0}'.format(clear_cmd_str))
