#!/usr/bin/env python3

# There is an alias for this script in my .zshrc (dev).
# When run, this scripts boots a dev environment in the
# current working directory. This involves looking for
# any scripts which match the runners defined in utils.py
# and setting up a new pane for those that exist, as well
# starting nvim.

import iterm2
import sys
from utils import *
import glob
import os

project_directory = os.getcwd()

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
    await find_or_create_runner_session(app, curr_session, default_runner, split_session, split_vertical, split_profile)
    await curr_session.async_send_text("nvim .\n")

def profile_customisations():
    profile = iterm2.LocalWriteOnlyProfile()
    profile.set_initial_directory_mode(iterm2.profile.InitialWorkingDirectory.INITIAL_WORKING_DIRECTORY_CUSTOM)
    profile.set_custom_directory(project_directory)
    return profile

iterm2.run_until_complete(main)
