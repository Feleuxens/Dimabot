import logging
import pytest

from dimabot.utils.logs import get_logger


class TestLogger:
    def test_get_logger(self):
        self.logger = None
        self.logger = get_logger(__name__)
        assert isinstance(self.logger, logging.Logger)

    def test_name(self):
        self.logger = get_logger(__name__)
        assert self.logger.__getattribute__("name") == "test_logs"

    def test_no_name(self):
        pytest.raises(TypeError, get_logger)

    def test_type_error(self):
        pytest.raises(TypeError, get_logger, 1)
