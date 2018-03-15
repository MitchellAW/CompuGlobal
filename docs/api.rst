.. currentmodule:: compuglobal

API Reference
=============

CompuGlobal allows for both random and searchable screencaps, images and gifs
embedded with default or custom captions for the following shows:

*The Simpsons, Futurama, Rick and Morty, West Wing and 30 Rock.*

.. note::

    This library relies upon undocumented external APIs.

API Endpoints
-------------

.. autoclass:: CompuGlobalAPI

    .. automethod:: compuglobal.CompuGlobalAPI.get_screencap
    .. automethod:: compuglobal.CompuGlobalAPI.get_random_screencap
    .. automethod:: compuglobal.CompuGlobalAPI.search
    .. automethod:: compuglobal.CompuGlobalAPI.search_for_screencap
    .. automethod:: compuglobal.CompuGlobalAPI.get_frames
    .. automethod:: compuglobal.CompuGlobalAPI.generate_gif

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
