#!/usr/bin/env python3

# There is an alias for this script in my .zshrc (chdev).
# When run, it uses fzf to fuzzy search for a project
# directory under ~/projects. When a directory is selected
# it will cd into that directory and use dev (start.py) to
# start a dev environment.

import iterm2
import subprocess
import sys
from utils import *

async def main(connection):
    app = await iterm2.async_get_app(connection)

    fzf_command = "ls ~/projects | fzf --layout=reverse --border=rounded --height=20 --prompt='Directory: '"
    result = subprocess.run(["zsh", "-c", fzf_command], stdin=sys.stdin, stdout=subprocess.PIPE)

    if (result.returncode != 0): await app.current_window.current_tab.async_close()

    clean_project_name = result.stdout.decode('utf-8').replace('\n','')
    project_directory = "~/projects/" + clean_project_name
    current_session = get_current_session(app)
    await current_session.async_send_text("cd " + project_directory + "\n")
    await current_session.async_send_text("dev\n")

iterm2.run_until_complete(main)
