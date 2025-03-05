# Git

## Introduction Sequence

### commits
`git commit`

### branches
branch early, and branch often
`git branch NAME`
`git checkout NAME`

`git checkout -b NAME` combines two commands above together

### merge
To combines two branches together, use `git merge NAME`, which merge the branch
`NAME` into the current branch.

### rebase
`git rebase NAME` change the parent commit to that the `NAME` branch on, which can
be used to make a nice linear sequence of commits.

## Ramping Up

### HEAD
`HEAD` is the symbolic name for the currently checked out commit.

### relative references
Moving around in Git by specifying commit hashes can get a bit tedious. You have
to use `git log` to see hashes.
So Git has relative refs:
* Moving upwards one commit at a time with `^`
* Moving upwards a number of times with `~<num>`
For example, `git checkout main^` and `git checkout HEAD~4`

### branch forcing
Relative refs are useful. For example, `git branch -f main HEAD~3` moves by force
the main branch to three parents behind HEAD.

### reverse changes
`git reset COMMIT` reverses changes by moving a branch reference backwards in
time to an older commit.
`git revert COMMIT` makes a new commit that introduces changes that exactly
reverses current commit. This is usually used for remote branches.

## Moving Work Around
Above concepts are enough to leverage 90% of the power of git repositories and
cover the main needs of developers. So I will learn the rest when in need.
