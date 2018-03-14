.. image:: https://orig00.deviantart.net/43c8/f/2012/137/f/8/internet_king_popup_banner_by_blueamnesiac-d503b3x.png
        :align: right
        :alt: Internet King Popup Banner by BLUEamnesiac

CompuGlobal
===========

.. image:: https://img.shields.io/pypi/v/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal
.. image:: https://img.shields.io/pypi/pyversions/compuglobal.svg
   :target: https://pypi.python.org/pypi/compuglobal

Python wrapper for the following undocumented APIs:

`Frinkiac`_, `Morbotron`_, `Master Of All Science`_, `Capital Beat Us`_
and `Good God Lemon`_

Allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

Installation
------------
To install the library, you can just run the following command:

::

    python3 -m pip install -U compuglobal

For the async version of the library, you can run the following command:

::

    python3 -m pip install -U git+https://github.com/MitchellAW/CompuGlobal@async


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

Preview
------------
.. image:: https://frinkiac.com/gif/S11E10/315560/322560.gif?b64lines=IFdFTEwsIElUIEFMTE9XUyBGT1IKIE1BWElNVU0gTU9CSUxJVFkuCiBGRUVMUyBMSUtFIEknTSBXRUFSSU5HCiBOT1RISU5HIEFUIEFMTC4=

Credits
------------

Creators and contributors of `Frinkiac`_, `Morbotron`_, `Master of All Science`_, `Good God Lemon`_ and `Capital Beat   Us`_:  

- `Paul Kehrer`_ 
- `Sean Schulte`_  
- `Allie Young`_ 
- `Max`_, `Jon Bernhardt`_, `Nick Beatty`_, `Vimp`_, `juz`_, Iconfactory and `Ged Maheux`_

`BLUEamnesiac`_ for the Internet King Popup Banner

*Named CompuGlobal as shorthand for* `CompuGlobalHyperMegaCap`_, *as the family of websites are named.*

.. _Frinkiac: https://frinkiac.com/
.. _Morbotron: https://morbotron.com/
.. _Master Of All Science: https://masterofallscience.com/
.. _Capital Beat Us: https://capitalbeat.us/
.. _Good God Lemon: https://goodgodlemon.com/
.. _here.: https://github.com/MitchellAW/CompuGlobal/tree/master/examples
.. _Master of All Science: https://masterofallscience.com/
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
