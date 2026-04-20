import sys
import json
from loguru import logger
import threading
from lib.internet import download
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot, Signal, Property
from RinUI.core import RinUIWindow


class AppInfo(QObject):
    # 信号：应用ID 与下载进度
    progressChanged = Signal(str, int)
    # 信号：应用列表已加载
    appsLoaded = Signal()

    def __init__(self):
        super().__init__()
        self._apps = []
        self.load_local_data()

    @Property(list, notify=appsLoaded)
    def appList(self):
        return self._apps

    @Slot()
    def loadApps_local(self):
        self.load_local_data()

    def load_local_data(self):
        # 从 data/app_info.json 加载应用列表
        base_dir = Path(__file__).parent
        json_path = base_dir / "data" / "app_info.json"

        try:
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._apps = data.get("apps", [])
                    logger.info(f"成功从 {json_path} 加载 {len(self._apps)} 条应用")
                    self.appsLoaded.emit()
            else:
                logger.error(f"找不到数据文件: {json_path.absolute()}")
        except Exception as e:
            logger.error(f"解析 JSON 出错: {e}")

    def get_app_by_id(self, app_id):
        for app in self._apps:
            if str(app.get("app_id")) == str(app_id):
                return app
        return None

    @Slot(str)
    def startDownload(self, app_id):
        app_data = self.get_app_by_id(app_id)
        if not app_data:
            logger.warning(f"找不到 ID 为 {app_id} 的应用")
            return

        url = app_data.get("download_url")
        if not url:
            logger.error(f"应用 {app_id} 缺少 download_url")
            return

        threading.Thread(
            target=self._run_download_thread,
            args=(app_id, url),
            daemon=True
        ).start()

    def _run_download_thread(self, app_id, url):
        # 使用 lib.internet.download 下载并通过信号上报进度
        success = download(
            url=url,
            savePath="./Download",
            progress_callback=lambda p: self.progressChanged.emit(str(app_id), p)
        )

        if success:
            logger.success(f"应用 {app_id} 下载完成")
        else:
            logger.error(f"应用 {app_id} 下载失败")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    store_provider = AppInfo()
    store_provider.loadApps_local()

    qml_path = Path(__file__).resolve().parent / "main.qml"
    window = RinUIWindow(str(qml_path))

    # 安全设置上下文属性：优先使用 engine，否则尝试 rootContext
    engine = getattr(window, 'engine', None)
    if engine:
        engine.rootContext().setContextProperty("appStoreProvider", store_provider)
    else:
        # 备用：若 window 提供 rootContext 接口
        root_ctx = getattr(window, 'rootContext', None)
        if root_ctx:
            root_ctx().setContextProperty("appStoreProvider", store_provider)

    sys.exit(app.exec())