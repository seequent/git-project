#!bin/env python

import subprocess
import os.path
import unittest, re


class TestInstall(unittest.TestCase):

    def test_installed(self):

        subprocess.call('rm gitproject.txt 2>> /dev/null; exit 0;', stderr=subprocess.STDOUT, shell=True)

        try:
            output = subprocess.check_output('git project', shell=True)
        except subprocess.CalledProcessError as err:
            self.assertEqual('gitproject.txt missing. Refer to the git-project readme\n', err.output)
            self.assertEqual(1, err.returncode)

        subprocess.call('echo "A" >> gitproject.txt', shell=True)

        try:
            output = subprocess.check_output('git project', shell=True)
        except subprocess.CalledProcessError as err:
            print err.output
            self.assertEqual('Usage: git project <init|save|load> [--repos <repos>]\n', err.output)
            self.assertEqual(1, err.returncode)

        subprocess.call('rm gitproject.txt', shell=True)

if __name__ == '__main__':
    unittest.main()
