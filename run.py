#!/usr/bin/env python3

import iterm2
import sys
from utils import *

usage = "Usage: run.py runner_name [command]"

if len(sys.argv) < 2:
  sys.exit("Too few args. " + usage)
if len(sys.argv) > 3:
  sys.exit("Too many args. " + usage)

async def main(connection):
    app = await iterm2.async_get_app(connection)
    curr_session = get_current_session(app)
    runner = get_runner_by_name(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) == 3 else None
    runner_session = await find_or_create_runner_session(app, curr_session, runner)
    await runner_session.async_activate()
    if command:
        await runner_session.async_send_text(command + "\n")

iterm2.run_until_complete(main)
