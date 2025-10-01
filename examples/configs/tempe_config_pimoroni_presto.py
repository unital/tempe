# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

"""Example tempe_config file for the Pimoroni Presto.

This assumes that you have the Presto firmware installed
"""

from presto import Presto

from tempe_displays.picographics import PrestoDisplay


async def init_display():
    display = PrestoDisplay(Presto(full_res=True))
    return display
