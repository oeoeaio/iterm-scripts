#!/usr/bin/env python3

import iterm2
import sys

runners = [
    { 'name': 'dev', 'start': 'auto/dev' },
]

usage = "Usage: run.py runner_name [command]"

if len(sys.argv) < 2:
  sys.exit("Too few args. " + usage)
if len(sys.argv) > 3:
  sys.exit("Too many args. " + usage)

runner = next((r for r in runners if r['name'] == sys.argv[1]), { 'name': 'default', 'start': None })
command = sys.argv[2] if len(sys.argv) == 3 else None
runner_session_ref_var = "user." + runner['name'] + "_session_id"

async def main(connection):
    app = await iterm2.async_get_app(connection)
    curr_session = get_current_session(app)
    runner_session = await find_or_create_runner_session(app, curr_session)
    await runner_session.async_activate()
    if command:
        await runner_session.async_send_text(command + "\n")

async def find_or_create_runner_session(app, curr_session):
    runner_session_id = await curr_session.async_get_variable(runner_session_ref_var)
    runner_session = None
    if runner_session_id:
        runner_session = app.get_session_by_id(runner_session_id)
    if runner_session is None:
        runner_session = await curr_session.async_split_pane(True)
        await curr_session.async_set_variable(runner_session_ref_var, runner_session.session_id)
        if runner['start']:
            await runner_session.async_send_text(runner['start'] + "\n")
    return runner_session

def get_current_session(app):
    window = app.current_terminal_window
    if window is not None:
        tab = window.current_tab
        if tab is not None:
            return tab.current_session
        else:
            sys.exit("No current tab")
    else:
        sys.exit("No current window")

iterm2.run_until_complete(main)
