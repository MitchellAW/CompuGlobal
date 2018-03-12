import compuglobal

# ----------------------------------------------------------------------------
# This an example of the information that can be obtained from a Screencap
# ----------------------------------------------------------------------------

# Futurama/Morbotron API
futurama = compuglobal.Morbotron()

# Get a screencap from The Simpsons using search terms: Nothing at all
screencap = futurama.search_for_screencap('Shutup and take my money')

# Returns: S07E03
episode_key = screencap.key

# Returns: 3
episode_number = screencap.episode

# Returns: 7
season_number = screencap.season

# Returns: Attack of the Killer App
episode_title = screencap.title

# Returns: Stephen Sandoval
director = screencap.director

# Returns: Patric M. Verrone
writer = screencap.writer

# Returns: 1-Jul-10
air_date = screencap.air_date

# Returns: https://en.wikipedia.org/wiki/Attack_of_the_Killer_App
wiki_url = screencap.wiki_url

# Returns: 343676
timestamp = screencap.timestamp

# Returns: 5:43
real_timestamp = screencap.get_real_timestamp()

# Returns: and the reception isn't very... Shut up and take my money!
# The new eyePhone is wonderful.
captions = screencap.caption
