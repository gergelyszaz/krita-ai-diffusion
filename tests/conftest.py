import sys
import pytest
from pathlib import Path
from PyQt5.QtCore import QCoreApplication

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from ai_diffusion import eventloop
from ai_diffusion.settings import settings, Settings


def pytest_addoption(parser):
    parser.addoption("--test-install", action="store_true")


class QtTestApp:
    def __init__(self):
        self._app = QCoreApplication([])
        eventloop.setup()

    def run(self, coro):
        task = eventloop.run(coro)
        while not task.done():
            self._app.processEvents()
        return task.result()


@pytest.fixture(scope="session")
def qtapp():
    return QtTestApp()


@pytest.fixture()
def temp_settings():
    yield settings
    settings.restore()
