# git-pull

git-pull auto pulls and pushes all git repositories in a directory.

## install.py

This file allows auto installation, which creates an installation in documents/git-pull. Just run this with
```python install.py```. This also creates a bat script in the desktop which can be run to pull all repositories. 
More options may be seen during installation.

## git-pull.py

This is the main script which pulls and pushes all git repositories in a directory. User doesn't need to run this
directly, unless desired. This script is run by the bat script created by install.py.

Arguments:

- ```-p``` or ```--push``` attempts to push all repositories after pulling them.
- ```-d``` or ```--destination``` full path to the parent directory that contains all the repositories.
- ```-r``` or ```--reset``` hard resets all repositories to their origin/master state before pulling 
to avoid merge conflicts. All changes will be lost.
