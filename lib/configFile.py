import json
import pathlib
from loguru import logger


class Initialization:
    """
    初始化配置目录与默认配置文件
    """

    def __init__(self, workDir=None, configSubdir='config'):
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

    def initConfig(self):
        """
        初始化主配置文件
        :return: bool
        """
        try:
            self.configDir.mkdir(parents=True, exist_ok=True)
            configPath = self.configDir / "config.json"

            data = {
                "path": {
                    "cachePath": "./cache",
                    "appInstallPath": "./APP"
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
    def readJson(self, file_path, keyPath):
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
