import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml
import RinUI

FluentWindow {
    id: window
    width: 1100
    height: 700
    minimumWidth: 600
    minimumHeight: 400
    maximumWidth: 16777215
    maximumHeight: 16777215
    visible: true
    title: "AppStore"
    defaultPage: Qt.resolvedUrl("pages/Home.qml")

    // 搜索框
    titleBarArea: AutoSuggestBox {
        id: searchField
        width: 325
        anchors.centerIn: parent
        placeholderText: qsTr("Search controls and samples...")
        model: ItemData.allControls
        textRole: "title"

        onAccepted: {
            var selected = ItemData.allControls.find(c => c.title === searchField.text)
            if (selected && selected.page) {
                navigationView.push(selected.page)
            } else {
                // 未命中则跳转搜索页
                console.log("Search for: " + searchField.text)
                navigationView.push(Qt.resolvedUrl("pages/Search.qml"), { query: searchField.text || "" })
            }
        }
    }

    navigationItems: [
        {
            title: qsTr("主页"),
            page: Qt.resolvedUrl("pages/Home.qml"),
            icon: "ic_fluent_home_20_regular",
        },
        {
            title: qsTr("所有应用"),
            page: Qt.resolvedUrl("pages/AllAPP.qml"),
            icon: "ic_fluent_apps_list_20_regular",
        },
        {
            title: qsTr("应用库"),
            page: Qt.resolvedUrl("pages/AppManagement.qml"),
            icon: "ic_fluent_apps_20_regular",
            position: Position.Bottom
        },
        {
            title: qsTr("设置"),
            page: Qt.resolvedUrl("pages/Settings.qml"), 
            icon: "ic_fluent_settings_20_regular",
            position: Position.Bottom
        }
    ]
}
