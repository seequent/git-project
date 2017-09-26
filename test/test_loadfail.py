#!bin/env python

import subprocess
import os.path
import unittest, re


class TestSaveLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # ensure we start with a clean slate, just in case
        subprocess.call('rm -rf remote local 2>> /dev/null', shell=True)

        # Initialize "remote" repositories
        subprocess.call('mkdir remote; mkdir local', shell=True)
        subprocess.call('cd remote; mkdir parent; cd parent; git init --bare', shell=True)
        subprocess.call('cd remote; mkdir child; cd child; git init --bare', shell=True)

        # Initialize "local" repositories
        subprocess.call('cd local;  git clone ../remote/parent', shell=True)
        subprocess.call('cd local;  git clone ../remote/child', shell=True)

        # Add a .gitproj to the parent repo, and make child a subrepo of parent
        subprocess.call('cd local/parent;  echo "version: 0.1.0" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "repos:" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc child ../../remote/child" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "Initial Commit"; git push -u origin master', shell=True)


    def test_init(self):

        # Initialize git-project (clones child into parent)
        subprocess.call('cd local/parent;  git project init', shell=True)
        subprocess.call('cd local/parent;  git add .gitignore; git commit -m ".gitignore"; git push', shell=True)

        # Ensure child was cloned properly
        output = subprocess.call('test -d local/parent/child;', shell=True)
        self.assertEqual(output, 0)

        # Ensure child's origin is set correctly
        output = subprocess.check_output('cd local/parent/child; git remote show origin | grep Fetch | grep remote/child | wc -l', shell=True)

        self.assertEqual(output.strip(), '1')

        # Add a commit to the child and update parent's .gitproj
        subprocess.call('cd local/parent/child; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)
        subprocess.call('cd local/parent; git project save -f', shell=True)
        subprocess.call('cd local/parent; git add .gitproj; git commit -m "Save Sub-Repository State"', shell=True)

        # Change the .gitproj so it is invalid
        subprocess.call('cd local/parent; sed \$d .gitproj > .gitproj2; echo "    c master nonexistantcommit" >> .gitproj2', shell=True)

        # Ensure loading the invalid .gitproj returns a non-zero error code
        subprocess.call('cd local/parent; mv .gitproj2 .gitproj', shell=True)
        res = subprocess.call('cd local/parent; git project load', shell=True)
        self.assertEqual(res, 1)

    @classmethod
    def tearDownClass(self):

        # Remove remote and local repos
        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
