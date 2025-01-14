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

import warnings

import pytest
from loguru import logger

from vikit.common.context_managers import WorkingFolderContext
from vikit.video.raw_text_based_video import RawTextBasedVideo
from vikit.video.video import VideoBuildSettings

warnings.simplefilter("ignore", category=ResourceWarning)
warnings.simplefilter("ignore", category=UserWarning)
logger.add("log_test_CI_prviders_health_checks.txt", rotation="10 MB")


class TestProvidersHealthChecks:

    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.skip(
        reason="This test is not working now due to throtling error on Haiper provider"
    )
    async def test_haiper_provider_and_generate(self):
        with WorkingFolderContext():
            video = RawTextBasedVideo("This is a fantastic day today")
            await video.build_async(
                build_settings=VideoBuildSettings(
                    test_mode=False, target_model_provider="haiper"
                )
            )
            assert video.media_url is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_stabilityai_provider_and_generate(self):
        with WorkingFolderContext():
            video = RawTextBasedVideo("This is a fantastic day today")
            await video.build_async(
                build_settings=VideoBuildSettings(
                    test_mode=False, target_model_provider="stabilityai"
                )
            )
            assert video.media_url is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_videocrafter_provider_and_generate(self):
        with WorkingFolderContext():
            video = RawTextBasedVideo("This is a fantastic day today")
            await video.build_async(
                build_settings=VideoBuildSettings(
                    test_mode=False, target_model_provider="videocrafter"
                )
            )
            assert video.media_url is not None
