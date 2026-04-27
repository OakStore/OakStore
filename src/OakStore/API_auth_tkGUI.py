# SPDX-License-Identifier: LGPL-3-or-later
# Copyright (C) 2026 Lyang1273 & Orlyn

import API_auth
import tkinter
from tkinter import messagebox

def GUI_TFAuth(text: str="要继续吗？"):
    """
    带用户界面的是或否对话框
    Args:
        text: 提示文本，默认“要继续吗？”

    Returns: bool
    """

    result = messagebox.askyesno("", text)
    return result




if __name__ == "__main__":
    print(GUI_TFAuth("要获取该应用吗？将会下载并安装到你的设备上。"))