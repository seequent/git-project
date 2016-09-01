git-project
***********

.. image:: https://travis-ci.org/3ptscience/git-project.svg?branch=master&branch=master
    :target: https://travis-ci.org/3ptscience/git-project

Scripts extending git for better project and sub-repository management

Purpose
-------

git-project serves as an alternative to other git sub-module/sub-repo solutions.
It is meant to be used in situations where both the parent repository and sub-repositories
are rapidly changing. This differs from existing solutions such as git sub-modules which work
best when sub-repositories are mostly stable.

git-project keeps track of which branches you should be on in all your repositories when you are working 
on a given feature. So, if you're working on feature X on a given branch in your main repository, which depends 
on branch Y in sub-repo A and branch X in sub-repo B, git-project keeps track of that for you! Then, if you want
to stop and work on a different feature that depends on an entirely different set of branches, you can switch to it
with a single command.


Install
-------

Run :code:`make install` (or :code:`sudo make install`)
This will install the git-project bash script into your /usr/local/bin/. 

To uninstall, simply run :code:`make uninstall`

Setup
-----

To setup, first create a .gitproj file with the format

::

    repos:
        sub-repo-name sub-repo-url
        sub-repo2-name sub-repo2-url

Then run :code:`git project init` from the root of your project. This will attempt to clone the sub-repositories
and add them to your .gitignore. If you have already cloned the sub-repositories, skip this step, but make sure
the sub-repositories are listed in your .gitignore.


Usage
-----

git-project saves the *state* of your repository and subrepositories. A *state* is the collection of feature branches for 
each repository.

To save the *state*, call :code:`git project save` (or :code:`git project save -- repo1 repo2 ...` to save only given repos)
This writes the current branches for all your subrepositories, as well as the latest commit on each branch, into the .gitproj file.
You should then add and commit the .gitproj file

To return to this *state* later, just switch to the branch in your base repository where you saved the state, and run :code:`git project load`. Note that this resets your branch to the commit stored in the .gitproj file. If you have unpushed changes, you will be prompted to push these before updating your branch to ensure your commits aren't orphaned.

If you want to load the exact commits from when you saved the branch (on detatched heads), use :code:`git project load --commit`.

Optional parameters are:

::

    --autoclone (-a): Autoclone repos in .gitproj that aren't in the directory
    --automerge (-m): Automerge branch updates when loading
    --force (-f): don't prompt, will automatically merge or clone when loading, and overwrite .gitproj when saving
    --update (-u): when loading, will update all branches to the most recent commit on the saved branch (rather than the saved commit).
    -- : when saving, separates flags from the list of repos to save. If not specified, all repos will be saved


Bugs
----

git-project is still in the very early stages of development. Use at your own risk. To report bugs or request features, please email mfirmin@3ptscience.com





