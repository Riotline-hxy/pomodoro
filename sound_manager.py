"""
音效管理 - 使用 winsound 生成不同旋律的提示音
"""

import threading
import winsound


def _play_melody(notes):
    """在一个后台线程中顺序播放多个音符"""
    def run():
        for freq, dur in notes:
            winsound.Beep(freq, dur)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def play_start():
    """工作开始 — 上行三音 C5→E5→G5"""
    _play_melody([(523, 150), (659, 150), (784, 200)])


def play_work_end():
    """工作结束 — 三声急促"""
    _play_melody([(880, 180)] * 3)


def play_short_break_end():
    """短休结束 — 下行双音 G5→E5"""
    _play_melody([(784, 200), (659, 200)])


def play_long_break_end():
    """长休结束 — 上行八度 C5→E5→G5→C6"""
    _play_melody([(523, 150), (659, 150), (784, 150), (1047, 300)])
