#!bin/env python

import subprocess
import os.path
import unittest, re


class TestNewBranch(unittest.TestCase):

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

        subprocess.call('cd local/parent;  git project save --force', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "save initial state"; git push', shell=True)

    def test_new_branch(self):
        # check to ensure the child repo was cloned
        output = subprocess.check_output('cd local/parent; ls | grep child | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child\n')

        # ensure the child's remote is correct
        output = subprocess.check_output('cd local/parent/child; git remote show origin | grep Fetch | grep remote/child | wc -l', shell=True)
        self.assertEqual(output.strip().replace('\n',''), '1')

        # create a feature branch on the child that the parent does not know about
        subprocess.call('cd local/child; git checkout -b feature_branch', shell=True)
        subprocess.call('cd local/child; echo "ASDF" >> test.txt; git add test.txt; git commit -m "feature"; git push -u origin feature_branch', shell=True)
        # get the commit on that branch
        output = subprocess.check_output('cd local/child; git show | head -n1 | awk \'{print $2}\'', shell=True)

        # add the feature branch and commit to parent's .gitproj
        subprocess.call('cd local/parent; cat .gitproj | head -n3 > .gitproj.bak', shell=True)
        subprocess.call('cd local/parent; cat .gitproj.bak > .gitproj', shell=True)
        subprocess.call('cd local/parent; rm .gitproj.bak', shell=True)
        subprocess.call('cd local/parent; echo "\tchild feature_branch {}" >> .gitproj'.format(output.strip()), shell=True)

        # commit the .gitproj
        subprocess.call('cd local/parent; git add -u; git commit -m "update gitproj"; git push', shell=True)

        # load the feature branch
        subprocess.call('cd local/parent; git project load', shell=True)

        self.assertEqual(subprocess.call('cd local/parent/child; git branch | grep feature_branch', shell=True), 0)



    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
