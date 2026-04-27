# SPDX-License-Identifier: LGPL-3-or-later
# Copyright (C) 2026 Lyang1273 & Orlyn

from loguru import logger
import zipfile
import traceback
import json
import configFile


def unzip(path, outputPath):
    """
    解压缩文件
    :param path: 压缩文件位置
    :param outputPath: 输出目录
    :return: bool: True：成功；False：失败
    """
    logger.info(f"解压文件 {path} 到 {outputPath}")

    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            logger.info("正在解压")
            zip_ref.extractall(outputPath)
            logger.info("解压成功")
            return True
    except FileNotFoundError:
        logger.error(f"解压失败：位于 {path} 的压缩文件不存在\n{traceback.format_exc()}")
        return False
    except zipfile.BadZipFile:
        logger.error(f"解压失败：压缩文件损坏或不是有效的ZIP文件 - {path}\n{traceback.format_exc()}")
        return False
    except Exception:
        logger.error(f"解压失败：未知错误\n{traceback.format_exc()}")
        return False

def APPInfo(path):
    """
    读取 APPInfo.json 中的内容
    :param path: APPInfo.json 文件目录
    :return: 读取成功时返回 data，失败时返回 None；返回示例：{'BasicInfo': {'AppPackageName': 'rinlit.classwidgets', 'AppName': 'ClassWidgets', 'AppIntroduction': '课表软件', 'AppVersionSN': 1, 'AppVersion': 2.0, 'AppVersionCode': None, 'AppDeveloper': 'RinLit'}, 'DevelopInfo': {'ProgrammingLanguage': 'Python', 'OpenSource': True, 'License': 'MIT'}, 'CompatibilityInfo': {'MinVersion': '10.0.10240', 'Bit': '64bit'}, 'SupportInfo': {'Link': 'classwidgets.rinlit.cn', 'Email': None}, 'UserExperienceTip': {'TouchSupport': True, 'LowMemoryUsage': True, 'i18n': True}, 'Permission': {'Camera': False, 'Microphone': False, 'ModifySystemRegistry': False, 'Internet': True, 'Administrator': False, 'location': True, 'MonitorUserOperations': False, 'DeviceInformation': False, 'RunInTheBackground': False}}
    """
    try:
        with open(f"{path}/APPInfo.json", 'r', encoding='utf-8') as file:
            data = json.load(file)

        logger.info(f"成功读取 {path}/APPInfo.json \n{data}")
        return data

    except FileNotFoundError:
        logger.error(f"找不到位于{path}的JSON文件")
        return None
    except json.JSONDecodeError:
        logger.error(f"JSON解析错误")
        return None
    except Exception as e:
        logger.error(f"读取文件时出错，因为 {e}")
        return None

def installAPP(packagePath, installPath):
    """
    安装应用
    :param packagePath: 应用包位置
    :param installPath: 安装位置
    :return: bool
    """
    json_file = configFile.jsonFile()
    cache_path = "."+json_file.readJsonFile("../config/config.json", "/path/cachePath")

    if unzip(packagePath, cache_path):
        # 解析应用信息
        info = APPInfo(cache_path + "APPInfo.json")
        


# unzip("../core1.py", "../cache")
APPInfo("../data")
installAPP("D:\\Python\\OSP-File\\260401.osp", 0)
