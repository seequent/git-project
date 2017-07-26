#!bin/env python

import subprocess
import os.path
import unittest, re


class TestOldVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        subprocess.call('rm -rf remote local 2>> /dev/null', shell=True)

        subprocess.call('mkdir remote; mkdir local', shell=True)
        subprocess.call('cd remote; mkdir parent; cd parent; git init --bare', shell=True)
        subprocess.call('cd remote; mkdir child; cd child; git init --bare', shell=True)
        subprocess.call('cd remote; mkdir child2; cd child2; git init --bare', shell=True)

        subprocess.call('cd local;  git clone ../remote/parent', shell=True)
        subprocess.call('cd local;  git clone ../remote/child', shell=True)
        subprocess.call('cd local;  git clone ../remote/child2', shell=True)

        subprocess.call('cd local/parent;  echo "version: 99999999.9.9" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "repos:" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc child ../../remote/child" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc2 child/child2 ../../remote/child2" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "Initial Commit"; git push -u origin master', shell=True)


    def test_init(self):
        version = subprocess.check_output('git project version', shell=True).strip()

        try:
            subprocess.check_output('cd local/parent;  git project init', shell=True)
        except subprocess.CalledProcessError as err:
            self.assertEqual('git-project install is out of date. .gitproj version: 99999999.9.9, git-project version: {}. Aborting'.format(version), err.output.strip())
            self.assertEqual(1, err.returncode)

        subprocess.call('cd local/parent; rm .gitproj', shell=True)


    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
