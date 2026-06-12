"""Timestamp module with helper class for working with timestamps."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from compuglobal.models.subtitle import Subtitle


class Timestamp:
    """Helper class for working with timestamps."""

    @staticmethod
    def get_minutes_seconds(milliseconds: int) -> tuple[int, int]:
        """Get minutes and seconds from milliseconds.

        Parameters
        ----------
        milliseconds : int
            The length of time in milliseconds

        Returns
        -------
        tuple[int, int]
            The minutes, and seconds as a tuple

        """
        seconds = int(milliseconds / 1000)
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        return minutes, seconds

    @staticmethod
    def get_real_timestamp(timestamp: int) -> str:
        """Get a readable timestamp for the frame in format `mm:ss`.

        Parameters
        ----------
        timestamp: int
            The timestamp to convert to readable string

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`.

        """
        minutes, seconds = Timestamp.get_minutes_seconds(timestamp)
        return f"{minutes}:{seconds:02d}"

    @staticmethod
    def get_duration(start_timestamp: int, end_timestamp: int) -> int:
        """Get the duration of the subtitle in milliseconds.

        Parameters
        ----------
        start_timestamp: int
            The start timestamp used in calculating the duration
        end_timestamp : int
            The start timestamp used in calculating the duration

        Returns
        -------
        int
            The duration in milliseconds.

        """
        return end_timestamp - start_timestamp

    @staticmethod
    def get_subtitles_duration(subtitles: list[Subtitle]) -> int:
        """Get the duration between the start of the earliest subtitle, and the end of the latest subtitle.

        Parameters
        ----------
        subtitles : list[Subtitle]
            The subtitles

        Returns
        -------
        int
            The duration in milliseconds

        """
        start_timestamp = min(subtitle.start_timestamp for subtitle in subtitles)
        end_timestamp = max(subtitle.end_timestamp for subtitle in subtitles)
        return Timestamp.get_duration(start_timestamp, end_timestamp)
