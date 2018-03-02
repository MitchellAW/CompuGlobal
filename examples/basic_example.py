import asyncio

from apis.frinkiac import Frinkiac


async def main():
    # The API used as the example here is Frinkiac (The Simpsons)
    # Everything below can be used for any of the APIs (Morbotron, Master of All
    # Science etc.)
    frinkiac = Frinkiac()

    # Getting a screencap from The Simpsons using search terms
    searched_screencap = await frinkiac.search_for_screencap('Stupid Sexy '
                                                             'Flanders')

    # Getting a random screencap from The Simpsons
    random_screencap = await frinkiac.get_random_screencap()

    # Gets the image of the screencap without any captions
    image = random_screencap.get_image_url()

    # Gets the image of the screencap with captions matching the quotes of the
    # screencap embedded in the image
    captioned_image = random_screencap.get_meme_url()

    # Gets the image of the screencap with 'Aurora Borealis?' embedded as the
    # caption
    custom_meme = random_screencap.get_meme_url(caption='Aurora Borealis?')

    # Gets the gif of the screencap with captions embedded
    # All gifs use a default gif length of ~7,000ms (7 sec) (starting
    # 3,000ms (3 sec) before the screencap and ending 4,000ms (4 sec) after the
    # screencap and will include the correct caption
    gif = await random_screencap.get_gif_url()

    # Gets the gif of the screencap with 'Steamed Hams' embedded as the caption
    custom_gif = await random_screencap.get_gif_url(caption='Steamed Hams')

    # Gets the gif of the screencap lasting ~10,000ms (10 sec). The gif will
    # start 1,000ms (1 sec) befor the screencap and end 9,0000ms (9 sec) after
    # the screencap.
    custom_length_gif = await random_screencap.get_gif_url(before=1000,
                                                           after=9000)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())