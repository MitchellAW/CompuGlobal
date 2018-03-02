# CompuGlobal
Unofficial API wrapper for the following undocumented APIs:

[Frinkiac](https://frinkiac.com), [Morbotron](https://morbotron.com), [Master Of All Science](https://masterofallscience.com), 
[Capital Beat Us](https://capitalbeat.us) and [Good God Lemon](https://goodgodlemon.com)

Allows for both random and searchable screencaps, images and gifs embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

## Basic Usage
```py
import asyncio

import compuglobal


async def main():
    simpsons = compuglobal.Frinkiac()
    
    # Random
    screencap = await simpsons.get_random_screencap()
    
    # Search
    screencap = await simpsons.search_for_screencap('stupid sexy flanders')
    
    # Images/Gifs
    image = screencap.get_meme_url()
    gif = await screencap.get_gif_url()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

For documented examples, check [here.](https://github.com/MitchellAW/CompuGlobal/tree/async/examples)


## Credits
**Creators of [Frinkiac](https://frinkiac.com/), [Morbotron](https://morbotron.com/), 
[Master of All Science](https://masterofallscience.com/), [GoodGod Lemon](https://goodgodlemon.com/) and 
[Capital Beat Us](https://capitalbeat.us/):**  
[Paul Kehrer](https://twitter.com/reaperhulk)  
[Sean Schulte](https://twitter.com/sirsean)  
[Allie Young](https://twitter.com/seriousallie)  

*Named CompuGlobal as shorthand for [CompuGlobalHyperMegaCap](https://langui.sh/2017/07/30/master-of-all-science-rick-and-morty/), as the family of websites are named.*
