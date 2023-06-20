#!/usr/bin/env python3

# Utility functions used by other scripts in this directory.

import iterm2
import sys

runners = [
    { 'name': 'dev', 'start': 'auto/dev' },
    { 'name': 'deploytools', 'start': 'auto/with-deploytools' },
    { 'name': 'db-shell', 'start': 'auto/db-shell*' },
]

default_runner = { 'name': 'default', 'start': None }

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

async def find_or_create_runner_session(app, main_session, runner, split_session = None, split_vertical = True, split_profile = None):
    split_session = main_session if not split_session else split_session
    runner_session_ref_var = "user." + runner['name'] + "_session_id"
    runner_session_id = await main_session.async_get_variable(runner_session_ref_var)
    runner_session = None
    if runner_session_id:
        runner_session = app.get_session_by_id(runner_session_id)
    if runner_session is None:
        runner_session = await split_session.async_split_pane(split_vertical, False, None, split_profile)
        await main_session.async_set_variable(runner_session_ref_var, runner_session.session_id)
        if runner['start']:
            await runner_session.async_send_text(runner['start'] + "\n")
    return runner_session

def get_runner_by_name(name):
    return next((r for r in runners if r['name'] == name), default_runner)

