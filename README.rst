###########
git-project
###########

.. image:: https://travis-ci.org/aranzgeo/git-project.svg?branch=master&branch=master
    :target: https://travis-ci.org/aranzgeo/git-project

Scripts extending git for better project and sub-repository management

*******
Purpose
*******

git-project serves as an alternative to other git sub-module/sub-repo solutions.
It is meant to be used in situations where both the parent repository and sub-repositories
are rapidly changing. This differs from existing solutions such as git sub-modules which work
best when sub-repositories are mostly stable.

git-project keeps track of which branches you should be on in all your repositories when you are working
on a given feature. So, if you're working on :code:`feature X` on a given branch in your main repository, which depends
on :code:`branch Y` in :code:`sub-repo A` and :code:`branch X` in :code:`sub-repo B`, git-project keeps track of that for you! Then, if you want
to stop and work on a different feature that depends on an entirely different set of branches, you can switch to it
with a single command.


*******
Install
*******

Run :code:`make install` (or :code:`sudo make install`)
This will install the git-project python script into your /usr/local/bin/.

To uninstall, simply run :code:`make uninstall`

*****
Setup
*****

1. Create a .gitproj file with the format

    ::

        repos:
            subrepo1-name local/path/to/repo1 remote-url-subrepo1
            subrepo2-name local/path/to/repo2 remote-url-subrepo2

    The first column (subrepo-name) is a memorable key for each repository that you will use when saving or loading that repo (see below).

    The second column is the local directory where you would like to store each repository (relative to the .gitproj file).

    The final column is the remote url from which to clone the repository.

2. Run :code:`git project init` from the root of your project. This will attempt to clone the sub-repositories and add them to your .gitignore. 

    If you have already cloned the sub-repositories, skip the :code:`git project init` step, but make sure the sub-repositories are listed in your .gitignore.


*****
Usage
*****

git-project is used to save and load the *state* of your repository and subrepositories. A *state* is the collection of feature branches for
each repository.

Saving
======

To save the current *state* of all subrepositories, call 

:code:`git project save`

To save only certain specified repositories, use 

:code:`git project save -- repo1-name repo2-name ...` 

This writes the current branch as well as the latest commit on that branch for each subrepository, into the .gitproj file.
You should then add and commit the .gitproj file like normal:

:code:`git add .gitproj && git commit -m "Update gitproj"`

Loading
=======

To return to this *state* later, just switch to the branch in your base repository where you saved the state, and run 

:code:`git project load`. 

This resets your subrepository's local branch to the commit stored in the .gitproj file. If you have unpushed changes in the subrepository, you will be prompted to push these before updating your branch to ensure your commits aren't orphaned.

If you want to load the exact commits on detached heads rather than resetting your local branch, use 

:code:`git project load --commit`.

Similar to saving, you can load only specific repositories with 

:code:`git project load -- repo1-name repo2-name`


Other
=====

Optional parameters are:

:code:`--autoclone (-a)`: Autoclone repos in .gitproj that aren't in the directory

:code:`--automerge (-m)`: Automerge branch updates when loading

:code:`--force (-f)`: don't prompt, will automatically merge or clone when loading, and overwrite .gitproj when saving

:code:`--update (-u)`: when loading, will update all branches to the most recent commit on the saved branch (rather than the saved commit).

:code:`--`: separates flags from the list of repos to save/load. If not specified, all repos will be saved/loaded


****
Bugs
****

If you run into any problems with `git-project`, please make an
`issue <https://github.com/aranzgeo/git-project/issues>`_
