#!bin/env python

import subprocess
import os.path
import unittest, re


class TestSaveLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        subprocess.call('rm -rf remote local 2>> /dev/null', shell=True)

        subprocess.call('mkdir remote; mkdir local', shell=True)
        subprocess.call('cd remote; mkdir parent; cd parent; git init --bare', shell=True)
        subprocess.call('cd remote; mkdir child; cd child; git init --bare', shell=True)

        subprocess.call('cd local;  git clone ../remote/parent', shell=True)
        subprocess.call('cd local;  git clone ../remote/child', shell=True)

        subprocess.call('cd local/parent;  echo "version: 0.1.0" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "repos:" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc child ../../remote/child" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "Initial Commit"; git push -u origin master', shell=True)


    def test_init(self):

        subprocess.call('cd local/parent;  git project init', shell=True)
        subprocess.call('cd local/parent;  git add .gitignore; git commit -m ".gitignore"; git push', shell=True)

        output = subprocess.check_output('cd local/parent; ls | grep child | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child\n')

        output = subprocess.check_output('cd local/parent/child; git remote show origin | grep Fetch | grep remote/child | wc -l', shell=True)

        self.assertEqual(output.strip().replace('\n',''), '1')

        subprocess.call('cd local/parent/child; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)

        subprocess.call('cd local/parent; git project save -f', shell=True)

        subprocess.call('cd local/parent; git add .gitproj; git commit -m "Save Sub-Repository State"', shell=True)

        subprocess.call('cd local/parent; sed \$d .gitproj > .gitproj2; echo "    c master nonexistantcommit" >> .gitproj2', shell=True)

        subprocess.call('cd local/parent; mv .gitproj2 .gitproj', shell=True)
        res = subprocess.call('cd local/parent; git project load', shell=True)
        self.assertEqual(res, 1)

    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
