from .screencap import Screencap


class AIOScreencap(Screencap):
    async def get_gif_url(self, caption=None, before=3000, after=4000):
        """Gets the timestamps of the frames before and after the timestamp
        of the screencap using the frames endpoint for the screencap's API
        and returns the url for the gif with an embedded caption.

        Parameters
        ----------
        caption: str, optional
            The caption to embed in the gif, if it is None, it will use the
            screencaps original caption.
        before: int, optional
            The number of milliseconds before the screencap's timestamp to
            begin the gif, defaults to 3 seconds (3000ms).
        after: int, optional
            The number of milliseconds after the screencap's timestamp to
            begin the gif, defaults to 4 seconds (4000ms).

        Returns
        -------
        str
            The gif url for the screencap with an embedded caption.

        Note
        ----
        Defaults gif duration to  ~7 seconds (7000ms)."""

        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = await self.api.get_frames(self.key, self.timestamp,
                                           int(before), int(after))
        start = frames[0].timestamp
        end = frames[-1].timestamp
        return self.gif_url.format(self.key, start, end, b64_caption)

    async def get_mp4_url(self, caption=None, before=3000, after=4000):
        """Gets the timestamps of the frames before and after the timestamp
        of the screencap using the frames endpoint for the screencap's API
        and returns the url for the mp4 with an embedded caption.

        Parameters
        ----------
        caption: str, optional
            The caption to embed in the mp4, if it is None, it will use the
            screencaps original caption.
        before: int, optional
            The number of milliseconds before the screencap's timestamp to
            begin the mp4, defaults to 3 seconds (3000ms).
        after: int, optional
            The number of milliseconds after the screencap's timestamp to
            begin the mp4, defaults to 4 seconds (4000ms).

        Returns
        -------
        str
            The mp4 url for the screencap with an embedded caption.

        Note
        ----
        Defaults mp4 duration to  ~7 seconds (7000ms)."""

        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = await self.api.get_frames(self.key, self.timestamp,
                                           int(before), int(after))
        start = frames[0].timestamp
        end = frames[-1].timestamp
        return self.mp4_url.format(self.key, start, end, b64_caption)

    def __str__(self):
        return (str(self.frame) + ': ' + self.title + ' (' +
                self.get_real_timestamp() + ')')
