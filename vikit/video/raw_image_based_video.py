# Copyright 2024 Vikit.ai. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from urllib.request import urlretrieve

from loguru import logger

from vikit.common.decorators import log_function_params
from vikit.common.handler import Handler
from vikit.video.building.handlers.videogen_handler import VideoGenHandler
from vikit.video.video import Video
from vikit.video.video_build_settings import VideoBuildSettings
from vikit.video.video_types import VideoType


class RawImageBasedVideo(Video):
    """
    Generates a video from raw image prompt
    """

    def __init__(
        self,
        title: str = None,
        raw_image_prompt: str = None,
    ):
        """
        Initialize the video

        Args:
            raw_image_prompt (base64: The raw image prompt to generate the video from
            title (str): The title of the video

        Raises:
            ValueError: If the source media URL is not set
        """
        if raw_image_prompt is None:
            raise ValueError("raw_image_prompt cannot be None")

        super().__init__()

        self._image = raw_image_prompt
        self._needs_reencoding = False
        if title:
            self._title = title
        else:
            self._title = "notitle"
        self.duration = 4.0  # currently generated video are 4s long, this will be variabilized per models later

    @property
    def short_type_name(self):
        """
        Get the short type name of the video
        """
        return str(VideoType.RAWIMAGE)

    @log_function_params
    def get_title(self):
        if self._title:
            return self._title
        #  get the first and last words of the prompt
        splitted_prompt = self._title.split(" ")
        clean_title_words = [word for word in splitted_prompt if word.isalnum()]
        if len(clean_title_words) == 1:
            summarised_title = clean_title_words[0]
        elif len(clean_title_words) > 1:
            summarised_title = clean_title_words[0] + "-" + clean_title_words[-1]
        else:
            summarised_title = "ImagePrompt"
        # Add a unique identifier suffix to prevent several videos having the same title in a composite down the road
        self._title = summarised_title
        return self._title

    def get_duration(self):
        return self.duration

    def run_build_core_logic_hook(self, build_settings: VideoBuildSettings):
        return super().run_build_core_logic_hook(build_settings)

    def get_core_handlers(self, build_settings) -> list[Handler]:
        """
         Get the handler chain of the video. Order matters here.
         At this stage, we should already have the enhanced prompt and title for this video

        Args:
             build_settings (VideoBuildSettings): The settings for building the video

         Returns:
             list: The list of handlers to use for building the video
        """
        handlers = []
        handlers.append(VideoGenHandler(video_gen_text_prompt=self._image))
        return handlers
