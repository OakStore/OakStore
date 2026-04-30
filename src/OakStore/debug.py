import tkinter as tk
from tkinter import ttk
import os
from . import configFile
from . import internet

def Debug():
    root = tk.Tk()
    root.title("调试窗口")
    root.geometry("550x400")

    # 创建 Notebook（标签页容器）
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # 创建第一个标签页
    home = ttk.Frame(notebook)
    notebook.add(home, text="主页")

    # 在标签页1中添加内容
    home_label = ttk.Label(home, text="调试模式主页", font=("微软雅黑", 14))
    home_label.pack(pady=20)
    whats_new = ttk.Label(home, text="""新功能预览
    添加了调试界面""")
    whats_new.pack(pady=0)

    # 创建第二个标签页
    download = ttk.Frame(notebook)
    notebook.add(download, text="下载与安装测试")

    download_label = ttk.Label(download, text="下载测试", font=("微软雅黑", 14))
    download_label.pack(pady=20)

    download_button = ttk.Button(download, text="从github下载测试包", command=lambda: internet.download("https://github.com/OakStore/OSP-File/raw/refs/heads/main/260401.zip", configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/cachePath"), progress_callback=download_test))
    download_button.place(x=20, y=75)
    download_progressbar = ttk.Progressbar(download, length=300)
    download_progressbar.place(x=150, y=76)


    def download_test(progress):
        download_progressbar["value"] = progress
        root.update()

    def download_and_install_test():


    root.mainloop()


