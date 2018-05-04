# [Forensics 100] My Secret Stash

The purpose of this challenge is to put your git skills to the test and was incredibly simple to create. Though the solution is very simple as well, it requires obscure knowledge of git.

## Distributables
`secret-stuff.tar.gz`: Download and unzip this bad boy and you're good to go!

## Solution
Okay, on to the fun stuff! The solution:
* Step 1: `git fsck` output should show the hash of a dangling commit
* Step 2: `git checkout [dangling commit hash]`
* Step 5: "3 sir!"
* Step 3: `cat secrets`

So what happened? Some cool shit happened thats what.
Whenever you back out of an operation in git, you lose references to some of your changes. For data recovery purposes, git will still keep track of these chages in the form of dangling blobs and dangling commits for some period of time before running garbage collection (`git gc`). What `git fsck` does is verify the connectivity and validity of the objects in the database, meaning that it will list any objects that don't have references. Dangling commits can be checked out in the same way normal referenced commits can. So once you find the unreferenced changes, you can recover your previously lost data.

## Other Goodies
Make sure you check look at some of the easter eggs I threw in there:
* Run `git log` and see the cool commit messages I wrote
* `git checkout` all of the commits to read the dialog I had fun writing
