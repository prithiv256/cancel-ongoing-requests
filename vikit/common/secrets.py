from os import getenv, path

from dotenv import load_dotenv
from loguru import logger

# Get the absolute path to the directory this file is in.
dir_path = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
env_file = path.join(dir_path, ".env.secrets." + getenv("CONFIG_ENVIRONMENT", "dev"))
assert path.exists(env_file), f"Secrets file {env_file} does not exist"
logger.debug(f"Loading secrets from {env_file}")

load_dotenv(dotenv_path=env_file)


def get_sendinblue_api_key():
    sendinblue_api_key = getenv("SENDINBLUE_API_KEY", "dev")
    if sendinblue_api_key is None:
        raise Exception("SENDINBLUE_API_KEY is not set")
    return sendinblue_api_key


def get_openai_whisper_api_key():
    openai_whisper_api_key = getenv("OPENAI_WHISPER_MODEL_ID", "dev")
    if openai_whisper_api_key is None:
        raise Exception("OPENAI_WHISPER_MODEL_ID is not set")
    return openai_whisper_api_key


def get_replicate_api_token():
    replicate_api_key = getenv("REPLICATE_API_TOKEN", "dev")
    if replicate_api_key is None:
        raise Exception("REPLICATE_API_TOKEN is not set")
    return replicate_api_key


def get_vikit_api_token():
    replicate_api_key = getenv("VIKIT_API_TOKEN", "dev")
    if replicate_api_key is None:
        raise Exception("VIKIT_API_TOKEN is not set")
    return replicate_api_key


def get_eleven_labs_api_key():
    eleven_labs_api_key = getenv("ELEVEN_LABS_KEY", "dev")
    if eleven_labs_api_key is None:
        raise Exception("ELEVEN_LABS_KEY is not set")
    return eleven_labs_api_key


def get_discord_api_key():
    discord_api_key = getenv("DISCORD_API_KEY", "dev")
    if discord_api_key is None:
        raise Exception("DISCORD_API_KEY is not set")
    return discord_api_key