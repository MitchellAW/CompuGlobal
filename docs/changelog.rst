.. currentmodule:: compuglobal

Changelog
=========
0.4.0
-----

Breaking Changes
~~~~~~~~~~~~~~~~
- Many model methods have been changed to be properties, see the following section for a full list
- Comic/Gif methods now support overriding (:class:`OverlayFormat`) instead of only :class:`FontFamily`:
    - :meth:`AsyncCompuGlobalAPI.get_comic_panel_url`
    - :meth:`AsyncCompuGlobalAPI.get_comic_strip_url`
    - :meth:`AsyncCompuGlobalAPI.get_gif_url`
- Timestamp helper method get_readable_timestamp() renamed to :meth:`Timestamp.get_timecode`
- FontColorRGB class renamed to :class:`FontColor`

.. code-block:: py

    # Before
    frinkiac.get_gif_url(screencap, font_family=FontFamily.JOST)

    # After
    overlay_format = OverlayFormat(font_family=FontFamily.JOST)
    frinkiac.get_gif_url(screencap, overlay_format=overlay_format)

Added
~~~~~
- Added some useful properties to models:
    - Screencap: :attr:`Screencap.key`, :attr:`Screencap.timestamp`, :attr:`Screencap.timecode`, :attr:`Screencap.duration`, :attr:`Screencap.start`, :attr:`Screencap.end`, :attr:`Screencap.caption`, :attr:`Screencap.captions`
    - ScreencapMoment: :attr:`ScreencapMoment.key`, :attr:`ScreencapMoment.timecode`
    - Frame: :attr:`Frame.timecode`
    - Subtitle: :attr:`Subtitle.duration`
    - Stream: :attr:`Stream.caption`, :attr:`Stream.encoded`
    - ComicPanel: :attr:`ComicPanel.encoded`
    - ComicStrip: :attr:`ComicStrip.encoded`
- :class:`OverlayFormat` for defining format preferences to use in overlays
- Optional argument for overriding overlay formatting, overlay_formats:
    - This enables overriding font, color, size, uppercase/lowercase in all overlays.
    - These can override all overlays in the entire gif/comic, or you can specify different formats for each overlay by providing a list.
    - See :meth:`OverlayFormat.normalise` for more details on how formats are resolved.
- Methods for gif/comic maker urls, these urls take you straight to the website to edit there:
    - :meth:`AsyncCompuGlobalAPI.get_comic_maker_url`
    - :meth:`AsyncCompuGlobalAPI.get_gif_maker_url`
- Logging throughout the library for:
    - API requests/responses
    - Endpoint validation
    - Non-default behaviour (subtitles/overlay formats overrides)

0.3.8
-----

Added
~~~~~
- :class:`Timestamp` helper class for handling timestamps

0.3.7
-------

Added
~~~~~
- Optional season filters, season_minimum, and season_maximum for the following methods:
    - :meth:`AsyncCompuGlobalAPI.search`
    - :meth:`AsyncCompuGlobalAPI.search_for_screencap`
    - :meth:`AsyncCompuGlobalAPI.get_random_screencap`

Miscellaneous
~~~~~~~~~~~~~
- Add support for optional query parameters with validation

0.3.6
-------

Breaking Changes
~~~~~~~~~~~~~~~~
- All instances of :class:`AsyncCompuGlobalAPI` now always require :class:`aiohttp.ClientSession`
- Search methods :meth:`AsyncCompuGlobalAPI.search` and :meth:`AsyncCompuGlobalAPI.search_for_screencap` now return lists containing :class:`FrameResult` instead of :class:`Frame`
- Rename :class:`NoSearchResultsFound` to :class:`NoSearchResultsFoundError`

Added
~~~~~
- :class:`FrameResult` model for search results
- :class:`~compuglobal.models.base.BaseCompuGlobalModel` as parent for all models with desired serialization/validation behaviour

Fixed
~~~~~
- Custom subtitles not being applied for comic panels
- Font color length validation
- Subtitle duration calculation
- Extra slash (/) in gif url

Miscellaneous
~~~~~~~~~~~~~
- Add unit tests for all models and API calls
- Add integration tests with real APIs
- Apply ruff rules to entire project

0.3.5
-------

Added
~~~~~
- :meth:`Subtitle.get_duration` for getting Subtitle duration

Fixed
~~~~~
- Incorrect path param using in :meth:`AsyncCompuGlobalAPI.get_frames`
- Custom subtitles not being used in comics/gifs

0.3.4
-------

Fixed
~~~~~
- Incorrect frames used in :class:`ComicStrip`
- Missing field alias in :class:`EpisodeSummary`

0.3.3
-------

Fixed
~~~~~
- Missing panels in :class:`ComicStrip`

0.3.2
-------

Added
~~~~~
- Methods for missing API endpoints:
    - :meth:`AsyncCompuGlobalAPI.browse_episode`
    - :meth:`AsyncCompuGlobalAPI.get_transcript`
    - :meth:`AsyncCompuGlobalAPI.navigator`

- Methods for getting caption as a string:
    - :meth:`StreamOverlay.get_caption`
    - :meth:`Screencap.get_caption`

- Methods for building models from a :class:`Screencap` directly:
    - :meth:`ComicPanel.from_screencap`, :meth:`ComicStrip.from_screencap`, and :meth:`Stream.from_screencap` for

Fixed
~~~~~
- Missing panels in :class:`ComicStrip`


0.3.1
-------

Breaking Changes
~~~~~~~~~~~~~~~~
- Made all models immutable

Added
~~~~~
- All models to compuglobal import scope

0.3.0
-------

Breaking Changes
~~~~~~~~~~~~~~~~
These changes are to accommodate the extensive update to the APIs with new features:

- All synchronous implementations of the package have been removed
- The async endpoints persist and are now accessible via :mod:`compuglobal` or :mod:`compuglobal.aio` as done previously
- The Master Of All Science API appears to be unavailable at this point in time and redirects to Frinkiac, I have added a deprecation warning to this API and it will remain unless the API returns
- The package now requires Python 3.13+
- Image, comic, and gif generation are all now performed using the API rather than from a Screencap:
    - :meth:`AsyncCompuGlobalAPI.get_image_url`
    - :meth:`AsyncCompuGlobalAPI.get_gif_url`

.. code-block:: py

    # This is now async
    simpsons = compuglobal.Frinkiac()

    # Previous usage
    await screencap.get_gif_url()

    # New usage
    await simpsons.get_gif_url(screencap)

Added
~~~~~
- Endpoints for comic panels/strips:
    - :meth:`AsyncCompuGlobalAPI.get_comic_panel_url`
    - :meth:`AsyncCompuGlobalAPI.get_comic_strip_url`
- Models for comics:
    - :ref:`See Comic models here <comics>`
- Default font for APIs to use in text Overlays

Miscellaneous
~~~~~~~~~~~~~
- Moved fonts to its own module
- Added default values to :class:`Stream`
