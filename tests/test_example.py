#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012-2013 qnub <qnub.ru@gmail.com>
# This file is distributed under the license LGPL version 3 or later
### END LICENSE

import sys
import os.path
import unittest
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from omweather import AboutOmweatherDialog


class TestExample(unittest.TestCase):
    def setUp(self):
        pass

    def test_AboutOmweatherDialog_members(self):
        pass

if __name__ == '__main__':
    unittest.main()
