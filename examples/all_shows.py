"""Example of the different APIs that are available for use."""

import asyncio

import aiohttp

import compuglobal


# Ensure aiohttp sessions are closed if any errors occur
async def main():
    async with aiohttp.ClientSession() as session:
        await example(session=session)


async def example(session: aiohttp.ClientSession):

    # The Simpsons
    simpsons = compuglobal.Frinkiac(session=session)
    await simpsons.get_random_screencap()

    # Futurama
    futurama = compuglobal.Morbotron(session=session)
    await futurama.get_random_screencap()

    # Rick and Morty
    rick_and_morty = compuglobal.MasterOfAllScience(session=session)
    await rick_and_morty.get_random_screencap()

    # West Wing
    west_wing = compuglobal.CapitalBeatUs(session=session)
    await west_wing.get_random_screencap()


if __name__ == "__main__":
    asyncio.run(main())
