import os
import unittest


def main():
    path = os.path.dirname(__file__)
    suite = unittest.TestLoader().discover(path)
    runner = unittest.TextTestRunner()
    return runner.run(suite)


if __name__ == '__main__':
    main()
