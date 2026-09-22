import os

from dotenv import load_dotenv


def test_openai_api_key_is_loaded():

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    assert api_key is not None
    assert api_key != ""
    assert api_key != "your_api_key_here"