# -*- coding: utf-8 -*-
"""
Thread with result

@File: result_thread.py
@Date: 2024-08-12
"""

# Built-in/Generic Imports
from typing import Any

# Libs
from threading import Thread

# Own modules

# Constants


class ResultThread(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
    ) -> None:
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self) -> None:
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

    @property
    def result(self) -> Any | None:
        return self._return
