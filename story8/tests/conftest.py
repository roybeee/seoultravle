import json
from pathlib import Path

import pytest

from story8.models import Actor, Bible
from story8.offline import OfflineProvider
from story8.studio import Studio

EX = Path(__file__).resolve().parents[1] / "examples"


@pytest.fixture
def studio(tmp_path):
    return Studio(tmp_path, OfflineProvider(), secret="test-secret")


@pytest.fixture
def bible():
    return Bible.model_validate_json((EX / "pianist_bible.json").read_text(encoding="utf-8"))


@pytest.fixture
def writer():
    return Actor(kind="human", id="writer-kim")
