#!/usr/bin/env python3

# This needs to be installed as an iterm2 AutoLaunch script
# so that we can create a keyboard shortcut that invokes the
# new_dev_tab() function.

import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)

    @iterm2.RPC
    async def new_dev_tab():
        curr_window = app.current_window
        new_tab = await curr_window.async_create_tab()
        await new_tab.current_session.async_send_text("chdev\n")
    await new_dev_tab.async_register(connection)

iterm2.run_forever(main)

