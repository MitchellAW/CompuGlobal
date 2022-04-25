.. image:: https://orig00.deviantart.net/43c8/f/2012/137/f/8/internet_king_popup_banner_by_blueamnesiac-d503b3x.png
        :alt: Internet King Popup Banner by BLUEamnesiac

CompuGlobal
===========

.. image:: https://img.shields.io/pypi/v/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal
.. image:: https://img.shields.io/pypi/pyversions/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal
.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
   :target: http://makeapullrequest.com

Python wrapper for all endpoints of the following undocumented APIs:

`Frinkiac`_, `Morbotron`_, `Master Of All Science`_, `Capital Beat Us`_
and `Good God Lemon`_

**Note**: I'll be keeping the wrapper up to date as more APIs are released.


CompuGlobal allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

Make sure to acquaint yourself with the API using the `documentation`_.

Installation
------------
To install the library, you can just run the following command:

::

    python3 -m pip install -U compuglobal


Basic Usage
------------

.. code:: py

    import compuglobal

    simpsons = compuglobal.Frinkiac()

    # Random
    screencap = simpsons.get_random_screencap()

    # Search
    screencap = simpsons.search_for_screencap('nothing at all')

    # Images/Gifs
    image = screencap.get_meme_url()
    gif = screencap.get_gif_url()


For documented examples, check `here.`_

Async Usage
-----------

.. code:: py

    import asyncio

    import compuglobal


    async def main():
        simpsons = compuglobal.aio.Frinkiac()

        # Random
        screencap = await simpsons.get_random_screencap()

        # Search
        screencap = await simpsons.search_for_screencap('nothing at all')

        # Images/Gifs
        image = screencap.get_meme_url()
        gif = await screencap.get_gif_url()

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

For documented examples, check `here.`_

What's New
------------
**0.2.7 - Breaking changes**

These changes are intended to provide more flexibility in the formatting
of captions:

- Added `format_caption()` method to CompuGlobalAPI objects. This
  replaces the formatting logic previously within the `encode_caption()`
  method. The `encode_caption()` method now only takes a caption parameter.
- Captions will no longer be formatted and shortened before
  generation of memes, gifs, and mp4 urls if a caption is given.
  Behaviour remains the same if no caption is given or if `format_caption()`
  is used on the caption beforehand.

**0.2.1 - Breaking Changes**

- Added Frame object: `search()`, `get_frames()` and `get_nearby_frames()`
  now all return a list of Frame objects instead of the json response.


Preview
------------
.. image:: https://frinkiac.com/gif/S11E10/315560/322560.gif?b64lines=IFdFTEwsIElUIEFMTE9XUyBGT1IKIE1BWElNVU0gTU9CSUxJVFkuCiBGRUVMUyBMSUtFIEknTSBXRUFSSU5HCiBOT1RISU5HIEFUIEFMTC4=

Credits
------------

Creators and contributors of `Frinkiac`_, `Morbotron`_, `Master of All Science`_, `Good God Lemon`_ and `Capital Beat Us`_:

- `Paul Kehrer`_ 
- `Sean Schulte`_  
- `Allie Young`_ 
- `Max`_, `Jon Bernhardt`_, `Nick Beatty`_, `Vimp`_, `juz`_, Iconfactory and `Ged Maheux`_

`BLUEamnesiac`_ for the Internet King Popup Banner

*Named CompuGlobal as shorthand for* `CompuGlobalHyperMegaCap`_, *as the family of websites are named.*

.. _documentation: http://compuglobal.readthedocs.io/
.. _Frinkiac: https://frinkiac.com/
.. _Morbotron: https://morbotron.com/
.. _Master Of All Science: https://masterofallscience.com/
.. _Capital Beat Us: https://capitalbeat.us/
.. _Good God Lemon: https://goodgodlemon.com/
.. _here.: https://github.com/MitchellAW/CompuGlobal/tree/master/examples
.. _Paul Kehrer: https://twitter.com/reaperhulk
.. _Sean Schulte: https://twitter.com/sirsean
.. _Allie Young: https://twitter.com/seriousallie
.. _Max: http://codepen.io/MyXoToD/
.. _Jon Bernhardt: http://www.dafont.com/akbar.font
.. _Nick Beatty: https://twitter.com/bumlaser
.. _Ged Maheux: https://twitter.com/gedeon
.. _Vimp: http://kornykattos.deviantart.com/
.. _juz: http://screenpeepers.com/profile/juz
.. _BLUEamnesiac: https://blueamnesiac.deviantart.com/
.. _CompuGlobalHyperMegaCap: https://langui.sh/2017/07/30/master-of-all-science-rick-and-morty/
