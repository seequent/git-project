#!bin/env python

import subprocess
import os.path
import unittest, re


class TestSafety(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # clean up, just in case
        subprocess.call('rm -rf remote local 2>> /dev/null', shell=True)

        # Create "local" and "remote" repositories
        subprocess.call('mkdir remote; mkdir local', shell=True)
        subprocess.call('cd remote; mkdir parent; cd parent; git init --bare', shell=True)
        subprocess.call('cd remote; mkdir child; cd child; git init --bare', shell=True)

        subprocess.call('cd local;  git clone ../remote/parent', shell=True)
        subprocess.call('cd local;  git clone ../remote/child', shell=True)

        # initialize the git-project for local/parent
        subprocess.call('cd local/parent;  echo "repos:" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tchild ../../remote/child" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "Initial Commit"; git push -u origin master', shell=True)

        # clone the child repo into the parent through git project init
        subprocess.call('cd local/parent;  git project init', shell=True)
        subprocess.call('cd local/parent;  git add .gitignore; git commit -m ".gitignore"; git push', shell=True)

    def test_safety(self):
        # check to ensure the child repo was cloned
        output = subprocess.check_output('cd local/parent; ls | grep child | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child\n')

        # ensure the child's remote is correct
        output = subprocess.check_output('cd local/parent/child; git remote show origin | grep Fetch | grep remote/child | wc -l', shell=True)
        self.assertEqual(output.strip().replace('\n',''), '1')

        # add a commit and SAVE it into the git-project (simulate working inside the parent-repo's copy of child)
        subprocess.call('cd local/parent/child; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)
        subprocess.call('cd local/parent; git project save -f', shell=True)

        # ensure git project load DID update the child repo
        output = subprocess.check_output('cd local/parent/child; git status | grep "behind" | wc -l', shell=True)
        self.assertEqual(output.strip().replace('\n',''), '0')

        # create a commit we DO NOT WANT to include in the git-project
        subprocess.call('cd local/child; git pull', shell=True)
        subprocess.call('cd local/child; echo "asdf2" > test2.txt; git add test2.txt; git commit -m "Second Commit"; git push', shell=True)
        subprocess.call('cd local/parent; git project load', shell=True)

        # ensure git project load DID NOT update the child repo
        output = subprocess.check_output('cd local/parent/child; git status | grep "behind" | wc -l', shell=True)
        self.assertEqual(output.strip().replace('\n',''), '1')

        subprocess.call('cd local/parent; git project load --update -f', shell=True)

        # ensure git project load DID NOT update the child repo
        output = subprocess.check_output('cd local/parent/child; git status | grep "behind" | wc -l', shell=True)
        self.assertEqual(output.strip().replace('\n',''), '0')


    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
