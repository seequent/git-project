git-project
***********

.. image:: https://travis-ci.com/3ptscience/git-project.svg?token=UXRQdDyJzZHqcFWUiw4y&branch=master
    :target: https://travis-ci.com/3ptscience/git-project

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

To save the *state*, call :code:`git project save`
This writes the current branches for all your subrepositories, as well as the latest commit on each branch, into the .gitproj file.
The .gitproj file is then automatically committed for you.

To return to this *state* later, just switch to the branch in your base repository where you saved the state, and run :code:`git project load`. If there are new commits on any of the branches in the *state*, git-project will prompt you to merge them in.

If you want to load the exact commits from when you saved the branch (on detatched heads), use :code:`git project load --commit`.

Optional parameters are:

::

    --autoclone (-a): Autoclone repos in .gitproj that aren't in the directory
    --automerge (-m): Automerge branch updates when loading
    --force (-f): don't prompt, will automatically merge or clone when loading, and overwrite .gitproj when saving
    --repos (-r): Only save/load the repos that follow. This must be the last command (NOT YET IMPLEMENTED)


Bugs
----

git-project is still in development. Use at your own risk. To report bugs or features, please email mfirmin@3ptscience.com





