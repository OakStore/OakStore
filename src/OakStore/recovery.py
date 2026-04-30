import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess
from . import configFile


class RecoveryMode:
    def __init__(self, root):
        self.root = root
        self.root.title("恢复模式")
        self.root.resizable(False, False)
        self.root.geometry("250x350")
        self.root.minsize(250, 350)
        self.root.maxsize(250, 350)

        # 按钮框架
        frame = ttk.Frame(root)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.reset_btn = ttk.Button(
            frame,
            text="※ 重置应用 ※",
            command=self.reset_app,
            width=40
        )
        self.reset_btn.pack(pady=5)

        self.clear_btn = ttk.Button(
            frame,
            text="更改基本配置与可能影响启动的配置",
            command=self.change_settings,
            width=40
        )
        self.clear_btn.pack(pady=5)

        self.open_config_path = ttk.Button(
            frame,
            text="打开配置文件目录",
            command=lambda: os.startfile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config"),
            width=40
        )
        self.open_config_path.pack(pady=5)

        self.cache_btn = ttk.Button(
            frame,
            text="清除缓存",
            command=self.clear_cache,
            width=40
        )
        self.cache_btn.pack(pady=5)

        self.restart = ttk.Button(
            frame,
            text="软重启到正常模式",
            command=self.restart,
            width=40
        )
        self.restart.pack(pady=5)

        self.re_btn = ttk.Button(
            frame,
            text="软重启到恢复模式",
            command=lambda: RecoveryMode.restart(mode="--re"),
            width=40
        )
        self.re_btn.pack(pady=5)

        self.debug_btn = ttk.Button(
            frame,
            text="软重启到调试模式",
            command=lambda: RecoveryMode.restart(mode="--de"),
            width=40
        )
        self.debug_btn.pack(pady=5)

        self.cancel_btn = ttk.Button(
            frame,
            text="关闭",
            command=self.root.destroy,
            width=40
        )
        self.cancel_btn.pack(pady=5)

    def reset_app(self):
        messagebox.showinfo("", "无法完成")

    def change_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("更改基本设置")
        settings.geometry("550x300")
        settings.transient(self.root)
        settings.grab_set()

        # 主框架
        main_frame = ttk.Frame(settings, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建可编辑表格
        self.config_table = ImmediateEditTable(main_frame)
        self.config_table.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 添加预设的配置项
        config_data = [
            ("应用安装目录", configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/appInstallPath")),
            ("缓存路径", configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/cachePath")),
        ]

        for key, value in config_data:
            self.config_table.add_row(key, value)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        def save_settings():
            all_data = self.config_table.get_all_data()
            # 显示保存的配置
            save_window = tk.Toplevel(settings)
            save_window.title("保存的配置")
            save_window.geometry("400x300")
            save_window.transient(settings)
            save_window.grab_set()

            # 显示保存的数据
            frame = ttk.Frame(save_window, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)

            text_widget = tk.Text(frame, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True)

            text_widget.insert(tk.END, "保存的配置:\n\n")
            for key, value in all_data:
                text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.config(state=tk.DISABLED)

            ttk.Button(frame, text="确定", command=save_window.destroy).pack(pady=10)

            print("保存的配置:")
            for key, value in all_data:
                print(f"  {key}: {value}")

        def cancel():
            settings.destroy()

        ttk.Button(button_frame, text="保存", command=save_settings, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=cancel, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(button_frame, text="此功能是未完工的半成品").pack(side=tk.RIGHT)

    def clear_cache(self):
        if messagebox.askyesno("确认", "清除缓存，确定吗？"):
            messagebox.showinfo("完成", "缓存已清除")

    @staticmethod
    def restart(mode=None):
        args = [sys.executable, sys.argv[0]]
        if mode is not None:
            args.append(mode)
        subprocess.Popen(args)
        sys.exit(0)


class ImmediateEditTable(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # 创建表格
        columns = ("配置项", "值")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=4)  # 减少行高为4

        # 设置列标题
        self.tree.heading("配置项", text="配置项")
        self.tree.heading("值", text="值")

        # 优化列宽比例：配置项占30%，值占70%
        self.tree.column("配置项", width=150, anchor='w', minwidth=120)
        self.tree.column("值", width=350, anchor='w', minwidth=250)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定双击编辑事件
        self.tree.bind("<Double-1>", self.on_double_click)

        self.edit_widget = None
        self.current_item = None

    def add_row(self, key, value):
        self.tree.insert("", tk.END, values=(key, value))

    def get_all_data(self):
        """获取所有数据"""
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            data.append((values[0], values[1]))
        return data

    def on_double_click(self, event):
        # 获取点击的行和列
        item = self.tree.identify_row(event.y)
        if not item:
            return

        column = self.tree.identify_column(event.x)
        col_index = int(column.replace("#", "")) - 1

        # 只允许编辑值列
        if col_index != 1:
            return

        # 获取单元格位置和大小
        x, y, width, height = self.tree.bbox(item, column)
        if not all([x, y, width, height]):
            return

        # 获取当前值
        current_value = self.tree.item(item, "values")[col_index]

        self.edit_widget = ttk.Entry(self.tree)
        self.edit_widget.place(x=x, y=y, width=width, height=height)
        self.edit_widget.insert(0, current_value)
        self.edit_widget.focus_set()

        self.current_item = item

        self.edit_widget.bind("<KeyRelease>", self.on_key_release)  # 每次按键都保存
        self.edit_widget.bind("<FocusOut>", self.save_edit)  # 失去焦点时保存
        self.edit_widget.bind("<Escape>", self.cancel_edit)  # ESC取消

    def on_key_release(self, event=None):
        if self.edit_widget and self.current_item:
            new_value = self.edit_widget.get()
            # 获取当前行的所有值
            values = list(self.tree.item(self.current_item, "values"))
            values[1] = new_value
            self.tree.item(self.current_item, values=values)

    def save_edit(self, event=None):
        if self.edit_widget and self.current_item:
            new_value = self.edit_widget.get()
            values = list(self.tree.item(self.current_item, "values"))
            values[1] = new_value
            self.tree.item(self.current_item, values=values)

        self.cleanup_edit()

    def cancel_edit(self, event=None):
        self.cleanup_edit()

    def cleanup_edit(self):
        if self.edit_widget:
            self.edit_widget.destroy()
            self.edit_widget = None
            self.current_item = None


if __name__ == "__main__":
    root = tk.Tk()
    app = RecoveryMode(root)
    root.mainloop()