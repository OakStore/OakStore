import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import "../components"

FluentPage {
    title: qsTr("主页")

    Column {
        width: parent.width
        spacing: 12 // 间距

        Text {
            typography: Typography.BodyStrong
            text: qsTr("优质应用")
            font.pixelSize: 20
        }

        Grid {
            width: parent.width
            // 列数自动计算
            columns: Math.floor(width / (340 + 6))
            rowSpacing: 12
            columnSpacing: 12
            layoutDirection: GridLayout.LeftToRight

            // 使用 Repeater 动态生成卡片
            Repeater {
                model: appStoreProvider.appList

                delegate: InfoClip {
                    modelData: model.modelData
                }
            }
        }

        Text {
            typography: Typography.BodyStrong
            text: qsTr("新应用")
        }

        Text {
            typography: Typography.BodyStrong
            text: qsTr("类型3")
        }
    }
}