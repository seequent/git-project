#!bin/env python

import subprocess
import os.path
import unittest


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

        subprocess.call('cd local/parent;  echo "version: 1.0.0" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "repos:" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc child ../../remote/child" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  echo "\tc2 child2 ../../remote/child2" >> .gitproj', shell=True)
        subprocess.call('cd local/parent;  git add .gitproj; git commit -m "Initial Commit"; git push -u origin master', shell=True)


    def test_single(self):

        subprocess.call('cd local/parent;  git project init', shell=True)
        subprocess.call('cd local/parent;  git add .gitignore; git commit -m ".gitignore"; git push', shell=True)

        output = subprocess.check_output('cd local/parent; ls | grep child | awk \'{print $1}\'', shell=True)
        self.assertEqual(output, 'child\nchild2\n')

        output = subprocess.check_output('cd local/parent/child; git remote show origin | grep Fetch | grep remote/child | wc -l', shell=True)

        self.assertEqual(output.strip().replace('\n',''), '1')

        output = subprocess.check_output('cd local/parent/child2; git remote show origin | grep Fetch | grep remote/child2 | wc -l', shell=True)

        self.assertEqual(output.strip().replace('\n',''), '1')


        subprocess.call('cd local/parent/child; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)
        subprocess.call('cd local/parent/child2; echo "Asdf" > test.txt; git add test.txt; git commit -m "Initial Commit"; git push', shell=True)


        subprocess.call('cd local/parent; git project save -f', shell=True)

        subprocess.call('cd local/parent; git add .gitproj; git commit -m "Save Sub-Repository State"', shell=True)


        self.assertTrue(os.path.isfile('local/parent/.gitproj'))

        output = subprocess.check_output('cd local/parent; cat .gitproj | tail -n2 | awk \'{print $1, $2}\'', shell=True)

        self.assertEqual(output, 'c master\nc2 master\n')

        subprocess.call('cd local/parent; git checkout -b dev; cd child; git checkout -b dev; cd ../child2; git checkout -b feature', shell=True)

        # tests saving a single repo
        subprocess.call('cd local/parent; git project save -f -- c', shell=True)

        subprocess.call('cd local/parent; git add .gitproj; git commit -m "Save Sub-Repository State"', shell=True)


        output = subprocess.check_output('cd local/parent; cat .gitproj | tail -n2 | awk \'{print $1, $2}\'', shell=True)
        self.assertEqual(output, 'c dev\nc2 master\n')

        subprocess.call('cd local/parent; git project save -f -- c2', shell=True)

        subprocess.call('cd local/parent; git add .gitproj; git commit -m "Save Sub-Repository State"', shell=True)

        output = subprocess.check_output('cd local/parent; cat .gitproj | tail -n2 | awk \'{print $1, $2}\'', shell=True)
        self.assertEqual(output, 'c dev\nc2 feature\n')



    @classmethod
    def tearDownClass(self):

        subprocess.call('rm -rf remote local', shell=True)

if __name__ == '__main__':
    unittest.main()
