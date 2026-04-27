// SPDX-License-Identifier: LGPL-3-or-later
// Copyright (C) 2026 Lyang1273 & Orlyn

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    title: qsTr("设置")

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: qsTr("About")
        }

        SettingCard {
            width: parent.width
            title: qsTr("窗口背景效果")
            description: qsTr("更改窗口背景效果，部分效果仅支持 Windows11。")
            icon.name: "ic_fluent_square_hint_sparkles_20_regular"

            ComboBox {
                property var data: ["mica", "acrylic", "none"]
                model: ListModel {
                    ListElement { text: qsTr("云母") }
                    ListElement { text: qsTr("亚克力") }
                    ListElement { text: qsTr("无") }
                }
                currentIndex: data.indexOf(Theme.getBackdropEffect())
                onCurrentIndexChanged: {
                    Theme.setBackdropEffect(data[currentIndex])
                }
            }
        }

        SettingExpander {
            width: parent.width
            title: qsTr("OakStore")
            description: qsTr("© 2026 Lyang & Orlyn. All rights reserved.")

            SettingItem {
                id: repo
                title: qsTr("To clone this repository")

                TextInput {
                    id: repoUrl
                    readOnly: true
                    text: "git clone https://github.com/OakStore/OakStore.git"
                    wrapMode: TextInput.Wrap
                }
                ToolButton {
                    flat: true
                    icon.name: "ic_fluent_copy_20_regular"
                    onClicked: {
                        Backend.copyToClipboard(repoUrl.text)
                    }
                }
            }
            SettingItem {
                title: qsTr("File a bug or request new sample")

                Hyperlink {
                    text: qsTr("Create an issue on GitHub")
                    openUrl: "https://github.com/OakStore/OakStore/issues/new/choose"
                }
            }
            SettingItem {
                title: qsTr("License")
                description: qsTr("This project is licensed under the GNU LGPL v3 license")

                Hyperlink {
                    text: qsTr("MIT License")
                    openUrl: "https://github.com/OakStore/OakStore/blob/main/LICENSE"
                }
            }
        }
    }
}