
import os
import json
from loguru import logger


def init_app_list():
    try:
        os.makedirs(f"{os.path.expanduser('~')}/AppData/Local/OakStore/data", exist_ok=True)

        """
        [AppPackageName]: 包名
            name: 名称
            version: 版本
            version_code: 版本号
            path: 位置
            executable_file: 可执行文件名 
        """

        data = {
            "oakstore.store": {
                "name": "OakStore",
                "version": "0.0.0.0",
                "version_code": 0,
                "path": ".",
                "executable_file": "store.exe"
            }
        }

        with open(f"{os.path.expanduser('~')}/AppData/Local/OakStore/data/AppList.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"已初始化应用列表")
        return True

    except PermissionError:
        logger.error("初始化应用列表失败：写入权限不足")
        return False
    except OSError as e:
        logger.error(f"初始化应用列表失败: {e}")
        return False

def app_list_operation(operation="get", data=None):
    with open(f"{os.path.expanduser('~')}/AppData/Local/OakStore/data/AppList.json", "r", encoding="utf-8") as f:
        app_list = json.load(f)

    if operation == "get":
        return list(app_list.keys())

    elif operation == "add":
        for key, value in data.items():
            app_list[key] = value
        with open(f"{os.path.expanduser('~')}/AppData/Local/OakStore/data/AppList.json", "w", encoding="utf-8") as f:   # 写回
            json.dump(app_list, f, indent=4, ensure_ascii=False)
        logger.info(f"已添加应用：{list(data.keys())}")
        return True

    elif operation == "remove":
        if data in app_list:
            del app_list[data]
        else:
            logger.info(f"要移除的应用 {data} 不存在")
            return False
        with open(f"{os.path.expanduser('~')}/AppData/Local/OakStore/data/AppList.json", "w", encoding="utf-8") as f:   # 写回
            json.dump(app_list, f, indent=4, ensure_ascii=False)
        logger.info(f"已移除应用：{data}")
        return True

def uninstall(app):
    pass

# print(app_list_operation("remove", data = "oakstore.store1"))