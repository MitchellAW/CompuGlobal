CompuGlobal
===========

Unofficial API wrapper for the following undocumented APIs:

`Frinkiac`_, `Morbotron`_, `Master Of All Science`_, `Capital Beat Us`_
and `Good God Lemon`_

Allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

Basic Usage
-----------

.. code:: py

    import compuglobal

    simpsons = compuglobal.Frinkiac()

    # Random
    screencap = simpsons.get_random_screencap()

    # Search
    screencap = simpsons.search_for_screencap('stupid sexy flanders')

    # Images/Gifs
    image = screencap.get_meme_url()
    gif = screencap.get_gif_url()


For documented examples, check `here.`_

Credits
-------
Creators of `Frinkiac`_, `Morbotron`_, `Master of All Science`_, `Good God Lemon`_ and `Capital Beat Us`_:  

`Paul Kehrer`_ 

`Sean Schulte`_  

`Allie Young`_  

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
.. _CompuGlobalHyperMegaCap: https://langui.sh/2017/07/30/master-of-all-science-rick-and-morty/
