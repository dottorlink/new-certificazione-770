# -*- coding: utf-8 -*-
"""
Thread with result

@File: result_thread.py
@Date: 2024-08-12
"""

# Built-in/Generic Imports
# Libs
from threading import Thread
from typing import Any

# Own modules

# Constants


class ResultThread(Thread):
    """Thread with result return value

    Args:
        Thread (thread): thread class
    """

    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
    ) -> None:
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._result = None

    def run(self) -> None:
        if self._target is not None:
            self._result = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._result

    @property
    def result(self) -> Any | None:
        return self._result
