.. image:: https://raw.githubusercontent.com/MitchellAW/MitchellAW.github.io/refs/heads/master/images/internet-king.png
        :alt: Internet King Popup Banner by BLUEamnesiac

CompuGlobal
===========

.. image:: https://img.shields.io/pypi/v/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal

.. image:: https://img.shields.io/pypi/pyversions/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal

.. image:: https://img.shields.io/readthedocs/compuglobal
   :target: https://compuglobal.readthedocs.io/en/latest/

.. image:: https://img.shields.io/github/actions/workflow/status/MitchellAW/CompuGlobal/test.yml?label=tests
   :target: https://github.com/MitchellAW/CompuGlobal/actions/workflows/test.yml

.. image:: https://img.shields.io/github/license/mitchellaw/compuglobal
   :target: https://github.com/MitchellAW/CompuGlobal/blob/main/LICENSE

Python wrapper for all endpoints of the following undocumented APIs:

`Frinkiac`_, `Morbotron`_, `Master Of All Science`_, and `Capital Beat Us`_.

**Note**: I'll be keeping the wrapper up to date as more APIs are released.


CompuGlobal allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, and West Wing.*

Make sure to acquaint yourself with the API using the `documentation`_.

Installation
------------
To install the library, you can just run the following command:

::

    python3 -m pip install -U compuglobal


Basic Usage
------------

.. code-block:: py

    import asyncio

    import compuglobal


    async def main():
        simpsons = compuglobal.aio.Frinkiac()

        # Random
        screencap = await simpsons.get_random_screencap()

        # Search
        screencap = await simpsons.search_for_screencap('nothing at all')

        # Images/Gifs
        image = await simpsons.get_comic_panel_url(screencap)
        gif = await simpsons.get_gif_url(screencap)

    if __name__ == '__main__':
        asyncio.run(main())

For documented examples, check `here.`_

What's New
------------
**0.3.0 - Breaking changes**

These changes are to accommodate the extensive update to the APIs with new features:

- All synchronous implementations of the package have been removed
- The async endpoints persist and are now accessible via **compuglobal** or **compuglobal.aio** as done previously
- The `Master Of All Science`_ API appears to be unavailable at this point in time and redirects to Frinkiac, I have added a **deprecation warning** to this API and it will remain unless the API returns
- The package now requires **Python 3.13+**
- Image, comic, and gif generation are all now performed using the API rather than from a Screencap

.. code-block:: py

    # This is now async
    simpsons = compuglobal.Frinkiac()

    # Previous usage
    await screencap.get_gif_url()

    # New usage
    await simpsons.get_gif_url(screencap)

Preview
------------
.. image:: https://raw.githubusercontent.com/MitchellAW/MitchellAW.github.io/refs/heads/master/images/nothing-at-all.gif

Credits
------------

Creators and contributors of `Frinkiac`_, `Morbotron`_, `Master of All Science`_, and `Capital Beat Us`_:

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
