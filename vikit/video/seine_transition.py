from loguru import logger
from urllib.request import urlretrieve
import asyncio

from vikit.video.video import Video, VideoBuildSettings
from vikit.common.decorators import log_function_params
from vikit.video.transition import Transition, url_exists


class SeineTransition(Transition):

    def __init__(
        self,
        source_video: Video,
        target_video: Video,
    ):
        """
        A Seine transition is a video that is generated between two videos
        """
        super().__init__(source_video=source_video, target_video=target_video)

    @log_function_params
    async def build(self, build_settings: VideoBuildSettings = None) -> Transition:
        """
        Apply the Seine transition between the source and target video

        Args:
            build_settings (VideoBuildSettings): The settings for building the video

        Returns:
            str: The path to the generated transition video
        """
        if self.are_build_settings_prepared:
            build_settings = self.build_settings

        await super().build(build_settings)

        if self.is_video_generated:
            return self

        if not self._source_video.is_video_generated:
            await self._source_video.build(build_settings=build_settings)
        if not self._target_video.is_video_generated:
            await self._target_video.build(build_settings=build_settings)

        assert self._source_video.is_video_generated, "source video must be generated"
        assert self._target_video.is_video_generated, "target video must be generated"
        assert url_exists(self._source_video.media_url), "source_video must exist"
        assert url_exists(self._target_video.media_url), "target_video must exist"

        logger.debug(
            f"Applying transition from {self._source_video.media_url} to {self._target_video.media_url}"
        )
        ml_gw = build_settings.get_ml_models_gateway()
        # We generate a transition
        link_to_transition_video = asyncio.run(
            ml_gw.generate_seine_transition_async(
                source_image_path=self._source_video.get_last_frame_as_image(),
                target_image_path=self._target_video.get_first_frame_as_image(),
            )
        )
        if link_to_transition_video is None:
            raise ValueError("No link to transition video generated")
        logger.debug(f"URL Retrieved to be interpolated {link_to_transition_video}")

        self.metadata.is_interpolated = build_settings.interpolate

        target_file_name = self.get_file_name_by_state(build_settings=build_settings)
        if build_settings.interpolate:
            interpolated_transition_link = asyncio.run(
                ml_gw.interpolate_async(link_to_transition_video)
            )
            urlretrieve(interpolated_transition_link, target_file_name)
        else:
            urlretrieve(link_to_transition_video, target_file_name)

        self.metadata.is_video_generated = True
        self._media_url = target_file_name

        return self
