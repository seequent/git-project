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
        subprocess.call('cd remote; mkdir child2; cd child2; git init --bare', shell=True)

        subprocess.call('cd local;  git clone ../remote/parent', shell=True)
        subprocess.call('cd local;  git clone ../remote/child', shell=True)
        subprocess.call('cd local;  git clone ../remote/child2', shell=True)

        subprocess.call('cd local/parent;  echo "child ../../remote/child" >> gitproject.txt', shell=True)
        subprocess.call('cd local/parent;  echo "child/child2 ../../remote/child2" >> gitproject.txt', shell=True)
        subprocess.call('cd local/parent;  git add gitproject.txt; git commit -m "Initial Commit"; git push -u origin master', shell=True)

    def test_init(self):

        subprocess.call('cd local/parent;  git project init', shell=True)
        subprocess.call('cd local/parent;  git add .gitignore; git commit -m ".gitignore"; git push', shell=True)

        output = subprocess.check_output('cd local/parent; ls | grep child | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child\n')

        output = subprocess.check_output('cd local/parent/child; git remote get-url origin | grep remote/child | wc -l', shell=True)


        output = subprocess.check_output('cd local/parent/child; ls | grep child2 | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child2\n')

        output = subprocess.check_output('cd local/parent/child/child2; git remote get-url origin | grep remote/child2 | wc -l', shell=True)

        self.assertEqual(output, '       1\n')


        subprocess.call('cd local/parent/child; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)
        subprocess.call('cd local/parent/child/child2; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)

        subprocess.call('cd local/parent; git project save -f', shell=True)

        self.assertTrue(os.path.isfile('local/parent/.gitproj'))

        output = subprocess.check_output('cd local/parent; cat .gitproj | awk \'{print $1, $2}\'', shell=True)

        self.assertEqual(output, 'child master\nchild/child2 master\n')


        subprocess.call('cd local/parent; git checkout -b dev; cd child; git checkout -b dev; cd child2; git checkout -b feature', shell=True)

        subprocess.call('cd local/parent; git project save -f', shell=True)


        output = subprocess.check_output('cd local/parent; cat .gitproj | awk \'{print $1, $2}\'', shell=True)
        self.assertEqual(output, 'child dev\nchild/child2 feature\n')

        subprocess.call('cd local/parent; git checkout master; git project load', shell=True)

        output = subprocess.check_output('cd local/parent; cat .gitproj | awk \'{print $1, $2}\'', shell=True)
        self.assertEqual(output, 'child master\nchild/child2 master\n')



    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
