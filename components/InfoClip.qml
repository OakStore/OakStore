import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI



Clip {
    id: root
    width: 340
    height: 88
    radius: 12

    // 属性
    property var modelData
    property bool isInstalled: false
    property bool isDownloading: false
    property int downloadProgress: 0

    Component {
        id: successNotif
        InfoBar {
            severity: Severity.Success
            title: qsTr("下载成功")
            text: qsTr("%1 已成功下载到/download中").arg(modelData.name)
            timeout: 5000
            customContent: [
                Hyperlink {
                    text: qsTr("查看下载目录")
                    onClicked: Qt.openUrlExternally("file:./download")
                }
            ]
        }
    }

    // 下载进度监听
    Connections {
        target: appStoreProvider

        function onProgressChanged(app_id, p) {
            if (modelData && app_id === modelData.app_id) {
                if (!isDownloading) isDownloading = true

                downloadProgress = p

                if (p >= 100) {
                    isDownloading = false
                    isInstalled = true
                    downloadProgress = 0
                }
            }
        }
    }

    onIsInstalledChanged: {
        if (isInstalled) {
            floatLayer.createCustom(successNotif)
        }
    }

    // 布局
    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 22
        anchors.rightMargin: 22
        spacing: 16

        Image {
            Layout.alignment: Qt.AlignVCenter
            source: modelData ? modelData.icon : ""
            fillMode: Image.PreserveAspectFit
            Layout.preferredWidth: 40
            Layout.preferredHeight: 40
        }

        Column {
            Layout.fillWidth: true // 占据中间空间
            Layout.alignment: Qt.AlignVCenter
            spacing: 3

            RowLayout {
                // 标题占中，按钮靠右
                width: parent.width
                Layout.fillWidth: true
                spacing: 8

                Text {
                    typography: Typography.BodyStrong
                    font.pixelSize: 16
                    text: modelData ? modelData.name : ""
                    // 标题占位
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                }

                // 按钮区
                Item {
                    Layout.preferredWidth: 80
                    Layout.preferredHeight: 32
                    Layout.alignment: Qt.AlignVCenter

                    Button {
                        anchors.fill: parent
                        visible: !isDownloading

                        // 图标与文本随安装状态切换
                        icon.name: isInstalled ? "ic_fluent_folder_open_20_filled" : "ic_fluent_arrow_download_20_filled"
                        highlighted: isInstalled ? false : true
                        text: isInstalled ? qsTr("打开") : qsTr("下载")

                        onClicked: {
                            if (isInstalled) {
                                console.log("执行打开:", modelData.name)
                                Qt.openUrlExternally("file:./download")
                            } else {
                                isDownloading = true
                                appStoreProvider.startDownload(modelData.app_id)
                            }
                        }
                    }

                    ProgressBar {
                        anchors.centerIn: parent
                        width: parent.width
                        visible: isDownloading
                        from: 0
                        to: 100
                        value: downloadProgress
                    }
                }
            }

            Text {
                Layout.fillWidth: true
                // 长描述截断到 10 字
                text: {
                    if (!modelData || !modelData.desc) return "";
                    return modelData.desc.length > 10
                        ? modelData.desc.substring(0, 10) + "..."
                        : modelData.desc
                }

                elide: Text.ElideRight
                maximumLineCount: 1
                typography: Typography.Caption
                color: Theme.currentTheme.colors.textSecondaryColor
            }
        }
    }

    onClicked: dialog.open()

    Dialog {
        id: dialog
        modal: true
        title: qsTr("应用信息")
        implicitWidth: 800

        standardButtons: Dialog.None | Dialog.Close

        ColumnLayout {
            anchors.fill: parent
            spacing: 12

            RowLayout {
                spacing: 12
                Image {
                    Layout.alignment: Qt.AlignVCenter
                    source: modelData ? modelData.icon : ""
                    fillMode: Image.PreserveAspectFit
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 40
                }
                Column {
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    spacing: 6

                    Text {
                        width: parent.width
                        typography: Typography.BodyStrong
                        font.pixelSize: 16
                        text: modelData ? modelData.name : ""
                    }

                    Text {
                        Layout.fillWidth: true
                        color: "gray"
                        font.pixelSize: 12
                        text: modelData ? (modelData.developer + " | v" + modelData.version) : ""
                    }
                }
            }

            Text {
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                text: modelData ? modelData.desc : ""
            }
        }
    }
}