#!/usr/bin/env python3

import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)
    curr_window = app.current_terminal_window
    new_tab = await curr_window.async_create_tab()
    await new_tab.current_session.async_send_text("chdev\n")

iterm2.run_until_complete(main)

