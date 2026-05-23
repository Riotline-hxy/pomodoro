"""
番茄钟核心逻辑 - 管理状态、时间、阶段切换
"""

from enum import Enum, auto


class Phase(Enum):
    WORK = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()

    @property
    def label(self):
        return {
            self.WORK: "工作中",
            self.SHORT_BREAK: "短休息",
            self.LONG_BREAK: "长休息",
        }[self]

    @property
    def color(self):
        return {
            self.WORK: "#FF6B35",
            self.SHORT_BREAK: "#F4A261",
            self.LONG_BREAK: "#E9C46A",
        }[self]


class PomodoroEngine:
    """管理番茄钟的计时逻辑、阶段切换"""

    def __init__(self, work_min=25, short_break_min=5, long_break_min=15, cycles=4):
        self.work_sec = work_min * 60
        self.short_break_sec = short_break_min * 60
        self.long_break_sec = long_break_min * 60
        self.cycles = cycles
        self.reset()

    def set_config(self, work_min, short_min, long_min, cycles):
        self.work_sec = work_min * 60
        self.short_break_sec = short_min * 60
        self.long_break_sec = long_min * 60
        self.cycles = cycles
        self.reset()

    def reset(self):
        self.phase = Phase.WORK
        self.running = False
        self.remaining = self.work_sec
        self.current_in_cycle = 1
        self.completed = 0

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def toggle(self):
        if self.running:
            self.pause()
        else:
            self.start()

    @property
    def paused(self):
        return not self.running and self.remaining < self.total_seconds

    def tick(self):
        """每秒调用一次。返回刚结束的阶段，无切换返回 None。"""
        if not self.running:
            return None

        self.remaining -= 1
        if self.remaining <= 0:
            ended = self.phase
            self._next_phase()
            return ended
        return None

    def _next_phase(self):
        if self.phase == Phase.WORK:
            self.completed += 1
            if self.current_in_cycle % self.cycles == 0:
                self.phase = Phase.LONG_BREAK
                self.remaining = self.long_break_sec
            else:
                self.phase = Phase.SHORT_BREAK
                self.remaining = self.short_break_sec
        else:
            self.phase = Phase.WORK
            if self.current_in_cycle % self.cycles == 0:
                self.current_in_cycle = 1
            else:
                self.current_in_cycle += 1
            self.remaining = self.work_sec

    @property
    def progress(self):
        total = {
            Phase.WORK: self.work_sec,
            Phase.SHORT_BREAK: self.short_break_sec,
            Phase.LONG_BREAK: self.long_break_sec,
        }[self.phase]
        return 1.0 - (self.remaining / total) if total > 0 else 0.0

    @property
    def total_seconds(self):
        return {
            Phase.WORK: self.work_sec,
            Phase.SHORT_BREAK: self.short_break_sec,
            Phase.LONG_BREAK: self.long_break_sec,
        }[self.phase]
