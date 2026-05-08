import asyncio

import compuglobal


# ----------------------------------------------------------------------------
# This an example of the information that can be obtained from a Screencap/Episode
# ----------------------------------------------------------------------------
async def main():
    # Futurama/Morbotron API
    futurama = compuglobal.Morbotron()

    # Get a screencap from The Simpsons using search terms: Nothing at all
    screencap = await futurama.search_for_screencap("Shut up and take my money")

    # Full episode object
    episode = screencap.episode

    # Returns: S07E03
    episode_key = episode.key
    print(episode_key)

    # Returns: 3
    episode_number = episode.episode_number
    print(episode_number)

    # Returns: 7
    season_number = episode.season
    print(season_number)

    # Returns: Attack of the Killer App
    episode_title = episode.title
    print(episode_title)

    # Returns: Stephen Sandoval
    director = episode.director
    print(director)

    # Returns: Patric M. Verrone
    writer = episode.writer
    print(writer)

    # Returns: 1-Jul-10
    air_date = episode.original_air_date
    print(air_date)

    # Returns: https://en.wikipedia.org/wiki/Attack_of_the_Killer_App
    wiki_url = episode.wiki_link
    print(wiki_url)

    # Returns: 343676
    timestamp = screencap.frame.timestamp
    print(timestamp)

    # Returns: 5:43
    real_timestamp = screencap.get_real_timestamp()
    print(real_timestamp)

    subtitles = screencap.subtitles
    print(subtitles)

    # Close API client connections
    await futurama.close()


if __name__ == "__main__":
    asyncio.run(main())
