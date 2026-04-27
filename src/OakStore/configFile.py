# SPDX-License-Identifier: LGPL-3-or-later
# Copyright (C) 2026 Lyang1273 & Orlyn

import json
import pathlib
import os
from loguru import logger


class Initialization:
    """
    初始化配置目录与默认配置文件
    """

    def __init__(self, workDir=f"{os.path.expanduser('~')}/AppData/Local/OakStore", configSubdir='config'):
        """
        初始化配置类
        :param workDir: 工作目录，默认为当前目录
        :param configSubdir: 配置文件的子目录名称，默认 config
        """
        # 工作目录，默认当前目录
        if workDir is None:
            self.workDir = pathlib.Path.cwd()
        else:
            self.workDir = pathlib.Path(workDir)

        self.workDir.mkdir(parents=True, exist_ok=True)
        self.configDir = self.workDir / configSubdir

        logger.info(f"工作目录: {self.workDir.absolute()}")
        logger.info(f"配置目录: {self.configDir}")

    @staticmethod
    def initConfig(workDir=None, configSubdir='config'):
        """
        初始化主配置文件
        :param workDir: 工作目录，默认为用户目录下的 OakStore/config
        :param configSubdir: 配置文件的子目录名称，默认 config
        :return: bool
        """
        if workDir is None:
            workDir = f"{os.path.expanduser('~')}/AppData/Local/OakStore/"
        configDir = pathlib.Path(workDir) / configSubdir
        try:
            configDir.mkdir(parents=True, exist_ok=True)
            configPath = configDir / "config.json"

            """
            path: 路径
                cachePath: 缓存
                appInstallPath: 应用安装
                installPath: 应用安装？（忘了）
            url: 顾名思义
                cloudConfig: 云端配置
            """

            data = {
                "path": {
                    "cachePath": f"{os.path.expanduser('~')}/AppData/Local/OakStore/cache",
                    "appInstallPath": f"{os.path.expanduser('~')}/AppData/Local/OakStoreInstall/APP",
                    "installPath": f"{os.path.expanduser('~')}/AppData/Local/OakStoreInstall/APP"
                },
                "url": {
                    "cloudConfig": "https://github.com/OakStore/OakStore/raw/refs/heads/cloudConfig/cloud.json"
                }
            }

            with configPath.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logger.info(f"已初始化配置文件: {configPath}")
            return True

        except PermissionError:
            logger.error("初始化配置文件失败：写入权限不足")
            return False
        except OSError as e:
            logger.error(f"初始化配置文件失败: {e}")
            return False


class jsonFile:
    @staticmethod
    def readJson(json_obj, keyPath):
        """
        读取json内容
        Args:
            json_obj: json对象
            keyPath: 要读取的键

        Returns:

        """
        data = json.load(json_obj)

        parts = keyPath.lstrip('/').split('/')    # 解析 keyPath

        for part in parts:
            if part == '':
                continue
            if isinstance(data, dict):
                if part not in data:
                    raise KeyError(f"键 '{part}' 不存在")
                data = data[part]
            elif isinstance(data, list):
                try:
                    idx = int(part)
                    data = data[idx]
                except ValueError:
                    raise KeyError(f"列表索引必须是整数，得到 '{part}'")
                except IndexError:
                    raise IndexError(f"列表索引 {idx} 超出范围")
            else:
                raise TypeError(f"无法在类型 {type(data).__name__} 上访问 '{part}'")

        return data

    @staticmethod
    def readJsonFile(file_path, keyPath):
        """
        从JSON文件读取指定路径的值
        路径格式：类似 '/data/value/main'，以 '/' 分隔
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        parts = keyPath.lstrip('/').split('/')    # 解析 keyPath

        for part in parts:
            if part == '':
                continue
            if isinstance(data, dict):
                if part not in data:
                    raise KeyError(f"键 '{part}' 不存在")
                data = data[part]
            elif isinstance(data, list):
                try:
                    idx = int(part)
                    data = data[idx]
                except ValueError:
                    raise KeyError(f"列表索引必须是整数，得到 '{part}'")
                except IndexError:
                    raise IndexError(f"列表索引 {idx} 超出范围")
            else:
                raise TypeError(f"无法在类型 {type(data).__name__} 上访问 '{part}'")

        return data

if __name__ == "__main__":
    Initialization.initConfig()
