#!/usr/bin/env python

import os
import sys
import unittest


def main():
    path = os.path.dirname(__file__)
    suite = unittest.TestLoader().discover(path)
    runner = unittest.TextTestRunner()
    test_run = runner.run(suite)
    ret = not test_run.wasSuccessful()
    sys.exit(ret)


if __name__ == '__main__':
    main()
