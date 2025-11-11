import asyncio


async def skippable_delay(
    skip_event: asyncio.Event, delay: float,
    *, clear_after_skip: bool = False,
    debug: bool = False
):
    """
    Allows for a skippable delay. `delay` is in seconds.
    """
    def debug_msg(msg: str):
        if debug:
            print(msg)
    try:
        await asyncio.wait_for(skip_event.wait(), timeout=delay)
        debug_msg("Wait skipped!")
    except asyncio.TimeoutError:
        debug_msg("Wait finished naturally.")
    if clear_after_skip:
        skip_event.clear()