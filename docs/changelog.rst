.. currentmodule:: compuglobal

Changelog
=========

0.3.8
-----

Added
~~~~~
- Timestamp helper class for handling timestamps

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
- Remove all synchronous implementations
- Made image/gif methods asynchronous:

    - :meth:`AsyncCompuGlobalAPI.get_image_url`
    - :meth:`AsyncCompuGlobalAPI.get_gif_url`

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
