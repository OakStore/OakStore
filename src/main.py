
import sys
import tkinter as tk
from OakStore.recovery import RecoveryMode

def main():
    # 检查启动参数
    if len(sys.argv) > 1 and sys.argv[1] in ("--re", "--recovery"):
        start_recovery_mode()
    elif len(sys.argv) > 1 and sys.argv[1] in ("--de", "--debug"):
        from OakStore import debug
        debug.Debug()
    else:
        start_normal_mode()


def start_recovery_mode():
    root = tk.Tk()
    app = RecoveryMode(root)
    root.mainloop()

def start_normal_mode():
    """启动正常模式"""
    print("启动正常模式")
    pass

if __name__ == "__main__":
    main()