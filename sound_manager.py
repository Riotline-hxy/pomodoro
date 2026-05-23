"""
音效管理 - 播放 sounds/ 目录下的 .wav 音效文件
"""

import os
import winsound

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")


def _play(name):
    path = os.path.join(SOUNDS_DIR, f"{name}.wav")
    winsound.PlaySound(path, winsound.SND_ASYNC | winsound.SND_FILENAME)


def play_start():
    _play("start")


def play_work_end():
    _play("work_end")


def play_short_break_end():
    _play("short_break_end")


def play_long_break_end():
    _play("long_break_end")
