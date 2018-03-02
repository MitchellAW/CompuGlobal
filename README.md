# CompuGlobal
Unofficial API wrapper for the following undocumented APIs:

[Frinkiac](https://frinkiac.com), [Morbotron](https://morbotron.com), [Master Of All Science](https://masterofallscience.com), 
[Capital Beat Us](https://capitalbeat.us) and [Good God Lemon](https://goodgodlemon.com)

Allows for both random and searchable screencaps, images and gifs embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

## Basic Usage
```py
import compuglobal

simpsons = compuglobal.Frinkiac()
screencap = simpsons.get_random_screencap()
image = screencap.get_meme_url()
gif = screencap.get_gif_url()
```

For a documented example, check [here.](https://github.com/MitchellAW/CompuGlobal/tree/master/examples)


## Credits
**Creators of [Frinkiac](https://frinkiac.com/), [Morbotron](https://morbotron.com/), 
[Master of All Science](https://masterofallscience.com/), [GoodGod Lemon](https://goodgodlemon.com/) and 
[Capital Beat Us](https://capitalbeat.us/):**  
[Paul Kehrer](https://twitter.com/reaperhulk)  
[Sean Schulte](https://twitter.com/sirsean)  
[Allie Young](https://twitter.com/seriousallie)  
