import asyncio
import random

import compuglobal.aio as compuglobal


# ----------------------------------------------------------------------------
# This an example of how to mimic the basic gifmaker functionality of Frinkiac
# ----------------------------------------------------------------------------
async def main():
    # The Simpsons
    simpsons = compuglobal.Frinkiac()

    # Get a screencap from The Simpsons using search terms: Nothing at all
    # NOTE: search_for_screencap() uses the first search result
    screencap = await simpsons.search_for_screencap('Nothing at all')

    # In order to specify the search result you'd like to use, use search() and
    # get_screencap() as shown below.
    # This example uses random.choice to select the search result used for the
    # screencap
    search_results = await simpsons.search('Nothing at all')
    random_result = random.choice(search_results)
    random_screencap = await simpsons.get_screencap(random_result['Episode'],
                                                    random_result['Timestamp'])

    # Get all frames that are 5,000ms before and 5,000ms after the screencap to
    # mimic behaviour used by Frinkiac
    # NOTE: before/after must be integers or they will be considered to be 0 by
    # the API
    frames = await simpsons.get_frames(screencap.key,
                                       screencap.timestamp,
                                       5000,
                                       5000)

    # Get image urls for displaying all the available frames before + after the
    # screencap
    frame_images = []
    for frame in frames:
        # Get the image url for the frame
        image_url = screencap.image_url.format(frame['Episode'],
                                               frame['Timestamp'])
        # Append the image_url
        frame_images.append(image_url)

    # Select start and end frames for custom gif (the start and end are chosen
    # as an example)
    start_frame = frames[0]
    end_frame = frames[-1]

    # Get timestamps of start and end frames for custom gif
    # NOTE: start_timestamp must be less than end_timestamp or an invalid frames
    # error will occur.
    start = start_frame['Timestamp']
    end = end_frame['Timestamp']

    # Encode the caption for custom gif
    # NOTE: Caption must be base64 encoded, you can b64 encode the caption
    # yourself or use encode_caption(caption), however, encode_caption() may
    # shorten the caption if it exceeds ~4 lines of dialogue.
    b64_caption = simpsons.encode_caption('Nothing at all.')

    # Format the url for the custom made gif
    # Returns this custom gif url:
    # https://frinkiac.com/gif/S11E10/313560/323560.gif?b64lines=IE5vdGhpbmcgYXQgYWxsLg==
    gif_url = screencap.gif_url.format(screencap.key, start, end, b64_caption)

    # Optional: Generate the gif
    # Returns this direct gif url:
    # https://frinkiac.com/video/S11E10/yM-FnJS2EMM1nuLj6nzhHtBnnOI=.gif
    # NOTE: Generating gifs requires waiting for the API to complete the
    # generating the gif. It is possible to get the direct url for the gif
    # before it is generated, but the direct url will not work until the gif
    # has been generated by the API.
    direct_url = await simpsons.generate_gif(gif_url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())