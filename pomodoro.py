"""
番茄钟 (Pomodoro Timer)
一个简单的终端番茄钟程序

使用方法:
    python pomodoro.py            # 默认设置（25min工作, 5min短休, 15min长休）
    python pomodoro.py --work 30  # 自定义工作时间
"""

import time
import sys
import argparse


class PomodoroTimer:
    """番茄钟计时器类"""

    def __init__(self, work_min=25, short_break_min=5, long_break_min=15, cycles=4):
        self.work_sec = work_min * 60
        self.short_break_sec = short_break_min * 60
        self.long_break_sec = long_break_min * 60
        self.cycles = cycles
        self.pomodoros_completed = 0

    @staticmethod
    def format_time(seconds):
        """将秒数格式化为 MM:SS"""
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    @staticmethod
    def show_notification(message):
        """发出提示（铃声 + 文字）"""
        print(f"\n  === {message} ===  ")
        print("\a")
        sys.stdout.flush()

    def countdown(self, seconds, phase_name):
        """倒计时显示"""
        while seconds > 0:
            bar_len = 30
            filled = int((seconds / max(self.work_sec, self.short_break_sec, self.long_break_sec)) * bar_len)
            bar = "#" * filled + "-" * (bar_len - filled)
            print(f"\r  {phase_name}: {self.format_time(seconds)}  [{bar}]", end="", flush=True)
            time.sleep(1)
            seconds -= 1
        print()

    def run_work(self, session_num):
        """执行一个工作时间段"""
        self.show_notification(f"第 {session_num} 个番茄 - 开始工作！")
        self.countdown(self.work_sec, "工作中")
        self.pomodoros_completed += 1
        self.show_notification("工作时间到！")

    def run_break(self, session_num):
        """执行休息时间段"""
        if session_num % self.cycles == 0:
            self.show_notification("长休息时间！")
            self.countdown(self.long_break_sec, "长休息")
            self.show_notification("长休息结束！")
        else:
            self.show_notification("短休息时间！")
            self.countdown(self.short_break_sec, "短休息")
            self.show_notification("短休息结束！")

    def start(self):
        """启动番茄钟"""
        print("\n" + "=" * 50)
        print("          番茄钟 Pomodoro Timer")
        print("=" * 50)
        print(f"  工作时间: {self.work_sec // 60} 分钟")
        print(f"  短休息:   {self.short_break_sec // 60} 分钟")
        print(f"  长休息:   {self.long_break_sec // 60} 分钟")
        print(f"  每个循环: {self.cycles} 个番茄")
        print("=" * 50 + "\n")

        try:
            session = 1
            while True:
                self.run_work(session)
                if session % self.cycles == 0:
                    self.run_break(session)
                    print(f"\n  [完成一轮！共 {self.pomodoros_completed} 个番茄]\n")
                else:
                    self.run_break(session)
                session += 1

        except KeyboardInterrupt:
            print("\n\n  [番茄钟已停止]")
            print(f"  本日完成番茄: {self.pomodoros_completed} 个")
            print("  再见！\n")


def main():
    parser = argparse.ArgumentParser(description="番茄钟命令行工具")
    parser.add_argument("--work", type=int, default=25, help="工作时间（分钟），默认 25")
    parser.add_argument("--short", type=int, default=5, help="短休息时间（分钟），默认 5")
    parser.add_argument("--long", type=int, default=15, help="长休息时间（分钟），默认 15")
    parser.add_argument("--cycles", type=int, default=4, help="每轮番茄数，默认 4")
    args = parser.parse_args()

    timer = PomodoroTimer(
        work_min=args.work,
        short_break_min=args.short,
        long_break_min=args.long,
        cycles=args.cycles,
    )
    timer.start()


if __name__ == "__main__":
    main()
