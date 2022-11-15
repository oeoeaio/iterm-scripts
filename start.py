#!/usr/bin/env python3

import iterm2
import sys
from utils import *
import glob
import os

usage = "Usage: start.py target_dir"

project_directory = os.getcwd()
if len(sys.argv) == 2 and sys.argv[1] != '.':
    project_directory = sys.argv[1]
if len(sys.argv) > 2:
    sys.exit("Expected one argument: " + usage)

async def main(connection):
    app = await iterm2.async_get_app(connection)
    curr_session = get_current_session(app)
    split_session = curr_session
    split_vertical = True
    split_profile = profile_customisations()
    for runner in runners:
        if glob.glob(runner['start']):
            split_session = await find_or_create_runner_session(app, curr_session, runner, split_session, split_vertical, split_profile)
            split_vertical = False
    await curr_session.async_send_text("nvim " + project_directory + "\n")
    await curr_session.async_send_text(" t" + "\n")
    await curr_session.async_activate()

def profile_customisations():
    profile = iterm2.LocalWriteOnlyProfile()
    profile.set_initial_directory_mode(iterm2.profile.InitialWorkingDirectory.INITIAL_WORKING_DIRECTORY_CUSTOM)
    profile.set_custom_directory(project_directory)
    return profile

iterm2.run_until_complete(main)
