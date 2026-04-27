import tkinter as tk
from tkinter import ttk


class EditableTable:
    def __init__(self, parent):
        self.parent = parent

        # 创建表格
        columns = ("姓名", "年龄", "部门", "电话")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)

        # 设置列标题和宽度
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_double_click)

        # 添加示例数据
        sample_data = [
            ("张三", "28", "技术部", "13800138001"),
            ("李四", "32", "市场部", "13800138002"),
            ("王五", "25", "人事部", "13800138003"),
        ]
        for row in sample_data:
            self.tree.insert("", tk.END, values=row)

        self.edit_entry = None  # 当前编辑框

    def on_double_click(self, event):
        """双击编辑单元格"""
        # 获取点击的行和列
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            item = self.tree.identify_row(event.y)

        if not item:
            return

        column = self.tree.identify_column(event.x)  # 返回如 "#1" "#2"
        col_index = int(column.replace("#", "")) - 1

        # 获取单元格位置和大小
        x, y, width, height = self.tree.bbox(item, column)
        if not all([x, y, width, height]):
            return

        # 获取当前值
        current_value = self.tree.item(item, "values")[col_index]

        # 创建输入框
        self.edit_entry = tk.Entry(self.tree)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, current_value)
        self.edit_entry.focus_set()

        # 绑定保存事件
        self.edit_entry.bind("<Return>", lambda e: self.save_edit(item, col_index))
        self.edit_entry.bind("<FocusOut>", lambda e: self.cancel_edit())
        self.edit_entry.bind("<Escape>", lambda e: self.cancel_edit())

    def save_edit(self, item, col_index):
        """保存编辑"""
        new_value = self.edit_entry.get()
        if new_value:
            # 获取当前行的所有值
            values = list(self.tree.item(item, "values"))
            values[col_index] = new_value
            # 更新表格
            self.tree.item(item, values=values)
        self.edit_entry.destroy()
        self.edit_entry = None

    def cancel_edit(self):
        """取消编辑"""
        if self.edit_entry:
            self.edit_entry.destroy()
            self.edit_entry = None


# 使用示例
root = tk.Tk()
root.title("可编辑表格")
root.geometry("500x300")
app = EditableTable(root)
root.mainloop()