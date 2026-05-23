# 🍅 番茄钟 (Pomodoro Timer)

一个简单好用的终端番茄钟程序，帮助提高专注力。

## 使用方法

```bash
# 默认设置（25min工作 + 5min短休 + 15min长休）
py pomodoro.py

# 自定义时间
py pomodoro.py --work 30 --short 10 --long 20 --cycles 3
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--work` | 25 | 工作时间（分钟） |
| `--short` | 5 | 短休息时间（分钟） |
| `--long` | 15 | 长休息时间（分钟） |
| `--cycles` | 4 | 每轮包含的番茄数 |

## 操作

- 按 `Ctrl+C` 停止番茄钟
