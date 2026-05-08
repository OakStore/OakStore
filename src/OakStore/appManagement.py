
import os
import shutil
import json
from loguru import logger
from . import configFile


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
        if data is None:
            return list(app_list.keys())
        else:
            if data in app_list:
                return configFile.jsonFile.readJson(app_list, f"/{data}")
            else:
                logger.info(f"应用 {data} 不存在")
                return False

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
    # 1. 获取应用信息
    app_info = app_list_operation("get", app)
    if not app_info:
        logger.error(f"卸载失败，应用 {app} 不存在")
        return False

    # 2. 获取安装路径
    install_path = app_info.get("path")
    if not install_path:
        logger.error(f"卸载失败，应用 {app} 的路径无效")
        return False

    # 3. 删除应用文件夹
    try:
        if os.path.exists(install_path):
            shutil.rmtree(install_path)
            logger.info(f"已删除应用文件夹：{install_path}")
        else:
            logger.warning(f"应用文件夹不存在：{install_path}")
    except Exception as e:
        logger.error(f"卸载失败，无法删除文件夹 {install_path}，错误：{e}")
        return False

    # 4. 从 AppList.json 移除应用
    removed = app_list_operation("remove", app)
    if not removed:
        logger.error(f"卸载失败，无法从列表移除 {app}")
        return False

    logger.info(f"已卸载 {app}")
    return True


# print(app_list_operation("remove", data = "oakstore.store1"))