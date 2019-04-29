#! /usr/local/bin/python

from git import Repo
import os
import io
import shutil
import sys
import getopt
import tempfile
import argparse

IGNORE_PATTERNS = ('.git', ".DS_Store")
SAFE_CHARS = ["-", "_", "."]
DEFAULT_STEP_BRANCH = "master"
IS_BRANCH_STRING = "Step"

MAX_LENGTH = 100

def makeBranches(repo_directory, branch_code_steps):
    print repo_directory
    print branch_code_steps
    repo = Repo(repo_directory)

    repo.git.checkout(branch_code_steps)
    for commitHash in repo.git.rev_list(branch_code_steps).split("\n"):
        commit = repo.commit(commitHash)

        branch_name = get_branch_name_from_commit_message(commit.message)

        if IS_BRANCH_STRING in branch_name:
            if branch_name in repo.branches:
                repo.git.branch(branch_name, "-D")
            new_branch = repo.create_head(branch_name)
            new_branch.set_commit(commitHash)

            # print "Would create: ", branch_name, " for commit ", commitHash 
            

def get_branch_name_from_commit_message(message):
    first_line = message.split("\n")[0]
    just_title = first_line.split(" ")[0]
    safe_message = "".join(
        c for c in just_title if c.isalnum() or c in SAFE_CHARS).strip()
    return (safe_message[:MAX_LENGTH]
            if len(safe_message) >
            MAX_LENGTH else safe_message)




DESCRIPTION = "This script "

EPILOG = " To make changes to "


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--directory',
                        default=os.getcwd(),
                        help="the directory of the repository")

    parser.add_argument('-b', '--branch', default=DEFAULT_STEP_BRANCH,
                        help="branch where the steps are. Default is master")

    parsed = parser.parse_args()

    makeBranches(
        parsed.directory,
        parsed.branch
        )


if __name__ == "__main__":
    sys.exit(main())