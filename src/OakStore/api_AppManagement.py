
from . import appManagement
from . import osp


def install_app(packagePath, format="osp"):
    if format == "osp":
        if osp.installAPP(packagePath):
            return True
        else:
            return False
    else:
        return False

def uninstall_app(name):
    appManagement.uninstall(name)

def get_app_list():
    appManagement.app_list_operation("get")
    return True

def get_installed_app_info(name):
    appManagement.app_list_operation("get", name)
    return True

def add_app(*, data, auth=False):
    if auth:
        appManagement.app_list_operation("add", data)
        return True
    else:
        return False

def remove_app(*, name, auth=False):
    if auth:
        if appManagement.app_list_operation("remove", name):
            return True
        else:
            return False
    else:
        return False
