from functools import wraps
from unittest.mock import patch

from ninja.signature import is_async


def mock_signal_call(signal: str, called: bool = True):
    def _wrap(func):
        if is_async(func):

            async def _wrapper(*args, **kwargs):
                with patch(f"ninja_extra.signals.{signal}.send") as mock_:
                    await func(*args, **kwargs)
                    assert mock_.called == called

        else:

            def _wrapper(*args, **kwargs):
                with patch(f"ninja_extra.signals.{signal}.send") as mock_:
                    func(*args, **kwargs)
                    assert mock_.called == called

        return wraps(func)(_wrapper)

    return _wrap


def mock_log_call(level: str, called: bool = True):
    def _wrap(func):
        if is_async(func):

            async def _wrapper(*args, **kwargs):
                with patch(
                    f"ninja_extra.logger.request_logger.{level.lower()}"
                ) as mock_:
                    await func(*args, **kwargs)
                    assert mock_.called == called

        else:

            def _wrapper(*args, **kwargs):
                with patch(
                    f"ninja_extra.logger.request_logger.{level.lower()}"
                ) as mock_:
                    func(*args, **kwargs)
                    assert mock_.called == called

        return wraps(func)(_wrapper)

    return _wrap
