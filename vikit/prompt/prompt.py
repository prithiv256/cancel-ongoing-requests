import os
from abc import ABC
from typing import Any

import pysrt

from vikit.gateways.ML_models_gateway_factory import MLModelsGatewayFactory
from vikit.gateways.ML_models_gateway import MLModelsGateway
from vikit.common.decorators import log_function_params
import vikit.common.secrets as secrets
from vikit.wrappers.ffmpeg_wrapper import get_media_duration
from vikit.prompt.prompt_build_settings import PromptBuildSettings


os.environ["REPLICATE_API_TOKEN"] = secrets.get_replicate_api_token()
"""
A subtitle file content looks lke this:

1
00:00:00,000 --> 00:00:05,020
I am losing my interest in human beings, in the significance of their lives and their actions.

2
00:00:06,080 --> 00:00:11,880
Someone has said it is better to study one man than ten books. I want neither books nor men,
"""


class Prompt(ABC):
    """
    A class to represent a prompt, a user written prompt, a prompt
    generated from an audio file, or one sent or received from an LLM.

    This class is going to be used as a base class for new type of prompts as
    they are accepted by LLM's, like an image, a video, or an embedding...
    """

    @log_function_params
    def __init__(self, ml_gateway: MLModelsGateway = None):
        self.text = None
        self._subtitles: list[pysrt.SubRipItem] = None
        self._subtitle_extractor = None
        if ml_gateway is None:
            self._models_gateway = MLModelsGatewayFactory().get_ml_models_gateway()
        self.build_settings: PromptBuildSettings = PromptBuildSettings()
        self.title = "NoTitle"
        self._extended_fields: dict[str, Any] = {}

    @property
    def extended_fields(self) -> dict[str, Any]:
        return self._extended_fields

    @extended_fields.setter
    def extended_fields(self, value: dict[str, Any]):
        self._extended_fields = value
        if "title" in value:
            self.title = value["title"]

    @property
    def subtitles(self) -> list[pysrt.SubRipItem]:
        """
        Returns the subtitles of the prompt.

        Raises:
            ValueError: If the subtitles have not been prepared yet
        """
        if self._subtitles is None:
            raise ValueError("The subtitles have not been prepared yet")

        return self._subtitles

    def get_duration(self) -> float:
        """
        Returns the duration of the recording
        """
        if self._recorded_audio_prompt_path is None:
            raise ValueError("The recording is not there or generated yet")
        total_length = get_media_duration(self._recorded_audio_prompt_path)
        return total_length
