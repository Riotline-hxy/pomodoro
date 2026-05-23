"""
番茄钟图形界面 - Tkinter 实现圆形进度条
"""

import tkinter as tk
from pomodoro_core import PomodoroEngine, Phase

# ---------- 暖色调色板 ----------
COLORS = {
    "bg": "#1C1410",
    "frame_bg": "#2C1F1A",
    "text_primary": "#FFE8D6",
    "text_secondary": "#B8A89A",
    "progress_track": "#3D322D",
    "button_bg_work": "#FF6B35",
    "button_bg_break": "#F4A261",
    "input_bg": "#3D322D",
    "input_fg": "#FFE8D6",
    "stats_fg": "#B8A89A",
}

FONTS = {
    "timer": ("Segoe UI", 52, "bold"),
    "phase": ("Segoe UI", 20),
    "stats": ("Segoe UI", 12),
    "label": ("Segoe UI", 11),
    "button": ("Segoe UI", 13, "bold"),
    "title": ("Segoe UI", 22, "bold"),
    "header": ("Segoe UI", 10),
}


class PomodoroApp(tk.Tk):
    """番茄钟主窗口"""

    def __init__(self):
        super().__init__()
        self.title("🍅 番茄钟")
        self.configure(bg=COLORS["bg"])
        self.resizable(False, False)

        self.engine = PomodoroEngine()

        self._build_ui()
        self._refresh_display()
        self._update_loop()

    # ===================== UI 构建 =====================

    def _build_ui(self):
        self._build_title()
        self._build_timer_canvas()
        self._build_stats_bar()
        self._build_settings()
        self._build_controls()

    def _build_title(self):
        """页头标题"""
        tk.Label(
            self,
            text="🍅 番 茄 钟 🍅",
            font=FONTS["title"],
            fg=COLORS["button_bg_work"],
            bg=COLORS["bg"],
        ).pack(pady=(24, 0))

    def _build_timer_canvas(self):
        """圆形进度条 + 中心倒计时"""
        self.canvas_size = 320
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_size,
            height=self.canvas_size,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        self.canvas.pack(pady=(10, 0))

        # 圆弧参数
        self.pad = 25
        self.arc_width = 14

        # 背景轨道
        self.canvas.create_arc(
            self.pad, self.pad,
            self.canvas_size - self.pad,
            self.canvas_size - self.pad,
            start=90, extent=359,
            style="arc", width=self.arc_width,
            outline=COLORS["progress_track"],
        )

        # 前景进度弧
        self.progress_arc = self.canvas.create_arc(
            self.pad, self.pad,
            self.canvas_size - self.pad,
            self.canvas_size - self.pad,
            start=90, extent=0,
            style="arc", width=self.arc_width,
            outline=COLORS["button_bg_work"],
            capstyle="round",
        )

        # 中心倒计时文字
        cy = self.canvas_size // 2
        self.timer_text = self.canvas.create_text(
            self.canvas_size // 2, cy - 18,
            text="25:00",
            font=FONTS["timer"],
            fill=COLORS["text_primary"],
            anchor="center",
        )

        # 阶段名称（含 emoji）
        self.phase_text = self.canvas.create_text(
            self.canvas_size // 2, cy + 35,
            text="🍅 工作中",
            font=FONTS["phase"],
            fill=COLORS["text_secondary"],
            anchor="center",
        )

        # 装饰小番茄
        self.canvas.create_text(
            18, self.canvas_size - 18,
            text="🍅", font=("Segoe UI", 14),
            anchor="center",
        )
        self.canvas.create_text(
            self.canvas_size - 18, 18,
            text="⏱", font=("Segoe UI", 14),
            anchor="center",
        )

    def _build_stats_bar(self):
        """番茄进度信息"""
        frame = tk.Frame(self, bg=COLORS["bg"])
        frame.pack(pady=(4, 0))

        self.stats_label = tk.Label(
            frame,
            text="🍅 番茄 1/4  ·  ✅ 已完成 0 个",
            font=FONTS["stats"],
            fg=COLORS["stats_fg"],
            bg=COLORS["bg"],
        )
        self.stats_label.pack()

    def _build_settings(self):
        """可自定义的参数区域"""
        frame = tk.Frame(self, bg=COLORS["frame_bg"], padx=24, pady=14)
        frame.pack(pady=(14, 0), padx=30, fill="x")

        # 标题
        tk.Label(
            frame, text="⚙️ 自定义设置",
            font=FONTS["header"],
            fg=COLORS["text_secondary"], bg=COLORS["frame_bg"],
        ).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 10))

        # 参数配置: (label, key, default, min, max) 带 emoji
        configs = [
            ("⏱ 工作时间", "work", 25, 1, 120),
            ("☕ 短休息",  "short", 5, 1, 30),
            ("🧘 长休息",  "long", 15, 1, 60),
            ("🔄 每轮",    "cycles", 4, 1, 10),
        ]

        self.inputs = {}
        for i, (label, key, default, min_v, max_v) in enumerate(configs):
            c = (i % 2) * 3
            r = i // 2 + 1

            tk.Label(
                frame, text=label,
                font=FONTS["label"],
                fg=COLORS["text_primary"], bg=COLORS["frame_bg"],
            ).grid(row=r, column=c, sticky="e", padx=(0, 4), pady=4)

            var = tk.StringVar(value=str(default))
            entry = tk.Entry(
                frame, textvariable=var,
                width=5, justify="center",
                font=FONTS["label"],
                bg=COLORS["input_bg"], fg=COLORS["input_fg"],
                relief="flat", bd=0,
            )
            entry.grid(row=r, column=c + 1, sticky="w", pady=4)

            tk.Label(
                frame, text="分钟" if key != "cycles" else "个",
                font=FONTS["header"],
                fg=COLORS["text_secondary"], bg=COLORS["frame_bg"],
            ).grid(row=r, column=c + 2, sticky="w", padx=(2, 16), pady=4)

            self.inputs[key] = (var, min_v, max_v)

        # 应用按钮 — 单独一行居中
        self.apply_btn = tk.Button(
            frame, text="✅ 应用",
            font=FONTS["header"],
            bg=COLORS["button_bg_work"], fg="#1C1410",
            activebackground="#E55A2B", activeforeground="#1C1410",
            relief="flat", bd=0, padx=18, pady=3,
            cursor="hand2",
            command=self._apply_settings,
        )
        self.apply_btn.grid(row=3, column=0, columnspan=6, pady=(6, 0))

    def _build_controls(self):
        """开始 / 暂停 / 重置 按钮"""
        frame = tk.Frame(self, bg=COLORS["bg"])
        frame.pack(pady=(18, 22))

        self.toggle_btn = tk.Button(
            frame,
            text="▶  开始",
            font=FONTS["button"],
            bg=COLORS["button_bg_work"], fg="#1C1410",
            activebackground="#E55A2B", activeforeground="#1C1410",
            relief="flat", bd=0,
            width=10, height=1,
            cursor="hand2",
            command=self._on_toggle,
        )
        self.toggle_btn.pack(side="left", padx=6)

        self.reset_btn = tk.Button(
            frame,
            text="↺  重置",
            font=FONTS["button"],
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            activebackground="#4A3A2A", activeforeground=COLORS["text_primary"],
            relief="flat", bd=0,
            width=10, height=1,
            cursor="hand2",
            command=self._on_reset,
        )
        self.reset_btn.pack(side="left", padx=6)

    # ===================== 事件处理 =====================

    def _apply_settings(self):
        defaults = {"work": 25, "short": 5, "long": 15, "cycles": 4}

        def _get(key):
            var, min_v, max_v = self.inputs[key]
            try:
                val = int(var.get())
                return max(min_v, min(val, max_v))
            except ValueError:
                var.set(str(defaults[key]))
                return defaults[key]

        work = _get("work")
        short = _get("short")
        long = _get("long")
        cycles = _get("cycles")

        self.engine.set_config(work, short, long, cycles)
        self._refresh_display()

    def _on_toggle(self):
        self.engine.toggle()
        self._refresh_display()

    def _on_reset(self):
        self.engine.reset()
        self._refresh_display()

    # ===================== 显示刷新 =====================

    def _refresh_display(self):
        eng = self.engine

        # 倒计时文本
        m, s = divmod(eng.remaining, 60)
        self.canvas.itemconfig(self.timer_text, text=f"{m:02d}:{s:02d}")

        # 阶段名称 + 颜色（含 emoji）
        phase_emojis = {
            Phase.WORK: "🍅",
            Phase.SHORT_BREAK: "☕",
            Phase.LONG_BREAK: "🧘",
        }
        emoji = phase_emojis.get(eng.phase, "🍅")
        self.canvas.itemconfig(self.phase_text, text=f"{emoji} {eng.phase.label}")

        color = eng.phase.color
        self.canvas.itemconfig(self.phase_text, fill=color)
        self.canvas.itemconfig(self.timer_text, fill=color)
        self.canvas.itemconfig(self.progress_arc, outline=color)

        # 进度圆弧
        extent = -359 * eng.progress
        self.canvas.itemconfig(self.progress_arc, extent=extent)

        # 统计文字
        stats = f"🍅 番茄 {eng.current_in_cycle}/{eng.cycles}  ·  ✅ 已完成 {eng.completed} 个"
        self.stats_label.config(text=stats)

        # 切换按钮文字
        if eng.running:
            self.toggle_btn.config(text="⏸  暂停")
            self.apply_btn.config(state="disabled")
        elif eng.paused:
            self.toggle_btn.config(text="▶  继续")
            self.apply_btn.config(state="disabled")
        else:
            self.toggle_btn.config(text="▶  开始")
            self.apply_btn.config(state="normal")

        # 按钮颜色跟随阶段
        btn_bg = COLORS["button_bg_work"] if eng.phase == Phase.WORK else COLORS["button_bg_break"]
        self.toggle_btn.config(bg=btn_bg, activebackground=btn_bg)

    def _update_loop(self):
        """每秒更新一次"""
        self.engine.tick()
        self._refresh_display()
        self.after(1000, self._update_loop)


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
