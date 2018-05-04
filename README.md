# SunshineCTF 2018 Challenges

This repo is to be used by challenge authors to host the sources of SunshineCTF 2018 challenges.

## Directory Structure

* Challenge category (e.g. `Web`, `Crypto`, `Pwn`)
   * Points-Challenge (e.g. `100-MyEasyChallenge`, `500-ThisIsLiterallyImpossible`)
      * The challenge itself

## Required Files

| File name         | Description
|-------------------|-------------
| `description.md`  | Markdown formatted description as should be displayed to players on the challenge description page.
| `README.md`       | Detailed information including a description of how the challenge works, steps to build and deploy this challenge, how to maintain it, and the intended solution. This will not be given to players.
| `flag.txt`        | The challenge's flag in the format `sun{flag_goes_here}`. If the flag is of a format different than this, please mention this explicitly in your `README.md` file.

If a challenge has files that should be downloadable from the challenge description, create a subdirectory `attachments` and place the files there.

An example challenge is available in [`Forensics/100-my-secret-stash`](Forensics/100-my-secret-stash).


## Submitting a Challenge

When adding a new challenge, please follow these steps:

1. Fork this repo to your own account by clicking the Fork button at the top-right of the screen (your fork will stay private).
2. Clone your repo locally (`git clone git@github.com:my_github_username/SunshineCTF-2018-Private.git && cd SunshineCTF-2018-Private`)
3. Create a git branch with the name of the challenge (`git checkout -b hello-friend`).
4. Create your challenge directory and the source files.
5. Stage your challenge files to be committed (`git add Stego/150-Hello-Friend && git status`).
6. Commit your changes (`git commit -m 'Added Hello Friend challenge'`)
7. Push the branch you created to your fork (`git push -u origin hello-friend`)
8. Back on the GitHub website for your fork, there should be a new button to create a pull request from the `hello-friend` branch on your repo to the upstream repo (the one on HackUCF's GitHub). Click that, fill out the details, and submit your pull request.
