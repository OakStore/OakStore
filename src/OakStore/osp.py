# SPDX-License-Identifier: LGPL-3-or-later
# Copyright (C) 2026 Lyang1273 & Orlyn
import os
from loguru import logger
import zipfile
import traceback
import json
import shutil
from . import appManagement
from . import configFile


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

def installAPP(packagePath):
    """
    安装应用
    :param packagePath: 应用包位置
    :param installPath: 安装位置
    :return: bool
    """
    logger.info(f"安装位于{packagePath}的应用包")
    cache_path = configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/cachePath")

    logger.info("正在清理安装缓存")
    try:
        shutil.rmtree(f"{cache_path}/install")
    except Exception:
        pass

    logger.info("开始安装")
    if unzip(packagePath, cache_path+"/install"):
        # 解析应用信息
        info = APPInfo(cache_path+"/install")
        logger.info(f"所安装应用的信息\n{info}")
        logger.info("复制程序文件")
        os.makedirs(configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/appInstallPath")+"/"+configFile.jsonFile.readJson(info, "/BasicInfo/AppPackageName"), exist_ok=True)
        shutil.copytree(configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/cachePath")+"/install/APP", configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/appInstallPath")+"/"+configFile.jsonFile.readJson(info, "/BasicInfo/AppPackageName"), dirs_exist_ok=True)
        shutil.copy2(configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/cachePath")+"/install/AppInfo.json", configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/appInstallPath")+"/"+configFile.jsonFile.readJson(info, "/BasicInfo/AppPackageName"))
        logger.info("复制完成")
        appManagement.app_list_operation("add", data = {
            configFile.jsonFile.readJson(info, "/BasicInfo/AppPackageName"): {
                "name": configFile.jsonFile.readJson(info, "/BasicInfo/AppName"),
                "version": configFile.jsonFile.readJson(info, "/BasicInfo/AppVersion"),
                "version_code": configFile.jsonFile.readJson(info, "/BasicInfo/AppVersionCode"),
                "path": configFile.jsonFile.readJsonFile(f"{os.path.expanduser('~')}/AppData/Local/OakStore/config/config.json", "/path/appInstallPath")+"/"+configFile.jsonFile.readJson(info, "/BasicInfo/AppPackageName"),
                "executable_file": configFile.jsonFile.readJson(info, "/BasicInfo/ExecutableFile")
            }
        })
        logger.info("已将应用添加至已安装列表")
        logger.info("安装完成")
        return True

