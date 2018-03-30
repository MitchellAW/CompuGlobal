.. currentmodule:: compuglobal

API Reference
=============

CompuGlobal allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

.. note::

    This library relies upon undocumented external APIs.

Contents
--------
.. toctree::
    full
    screencap
    frame

API Endpoints
-------------

.. autoclass:: CompuGlobalAPI
    :noindex:

    .. automethod:: compuglobal.CompuGlobalAPI.get_screencap
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.get_random_screencap
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.search
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.search_for_screencap
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.get_frames
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.get_nearby_frames
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.view_episode
        :noindex:
    .. automethod:: compuglobal.CompuGlobalAPI.generate_gif
        :noindex:

Errors
------
.. autoclass:: APIPageStatusError
    :members:

.. autoclass:: NoSearchResultsFound
    :members:

Supported APIs
--------------

Frinkiac
~~~~~~~~
.. autoclass:: Frinkiac
    :members:
    :noindex:

Morbotron
~~~~~~~~~
.. autoclass:: Morbotron
    :members:
    :noindex:

Master Of All Science
~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: MasterOfAllScience
    :members:
    :noindex:

Good God Lemon
~~~~~~~~~~~~~~
.. autoclass:: GoodGodLemon
    :members:
    :noindex:

Capital Beat Us
~~~~~~~~~~~~~~~
.. autoclass:: CapitalBeatUs
    :members:
    :noindex:

FrinkiHams
~~~~~~~~~~
.. autoclass:: FrinkiHams
    :members:
    :noindex:
