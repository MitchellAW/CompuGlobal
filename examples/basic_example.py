"""Example of the basic image/comic/gif functionality available."""

import asyncio

import aiohttp

import compuglobal


# Ensure aiohttp sessions are closed if any errors occur
async def main():
    async with aiohttp.ClientSession() as session:
        await example(session=session)


async def example(session: aiohttp.ClientSession):
    # The API used as the example here is Frinkiac (The Simpsons)
    # Everything below can be used for any of the APIs (Morbotron, Master of All
    # Science etc.)
    frinkiac = compuglobal.Frinkiac(session=session)

    # Getting a screencap from The Simpsons using search terms
    searched_screencap = await frinkiac.search_for_screencap("Stupid Sexy Flanders")
    print(searched_screencap)

    # Getting a random screencap from The Simpsons
    random_screencap = await frinkiac.get_random_screencap()

    # Gets the image of the screencap without any captions
    image = await frinkiac.get_image_url(random_screencap)
    print(image)

    # Gets the image of the screencap with captions matching the quotes of the
    # screencap embedded in the image
    comic_panel = await frinkiac.get_comic_panel_url(random_screencap)
    print(comic_panel)

    # Gets a comic strip with mulitple screencaps and captions matching the quotes
    # of each screencap in the image
    comic_strip = await frinkiac.get_comic_strip_url(random_screencap)
    print(comic_strip)

    # Gets the gif of the screencap with captions embedded
    gif = await frinkiac.get_gif_url(searched_screencap)
    print(gif)


if __name__ == "__main__":
    asyncio.run(main())
