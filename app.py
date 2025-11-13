import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class AutoResizingPlainTextEdit(QPlainTextEdit):
    MIN_HEIGHT = 40
    MAX_HEIGHT = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(self.MIN_HEIGHT)
        self.setMaximumHeight(self.MAX_HEIGHT)
        self.setPlaceholderText("输入您的问题...")
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.document().blockCountChanged.connect(self._adjust_height)
        self.textChanged.connect(self._adjust_height)
        self._adjust_height()

    def setPlainText(self, text):  # noqa: D401
        super().setPlainText(text)
        self._adjust_height()

    def _adjust_height(self):
        blocks = max(1, self.document().blockCount())
        line_height = self.fontMetrics().lineSpacing()
        calculated = self.MIN_HEIGHT + (blocks - 1) * line_height
        new_height = max(self.MIN_HEIGHT, min(calculated, self.MAX_HEIGHT))
        self.setFixedHeight(int(new_height))


class FullscreenInputDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑信息")
        self.setModal(True)
        self.resize(420, 360)
        main_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()
        title_label = QLabel("编辑信息")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.reject)
        header_layout.addWidget(close_button)
        main_layout.addLayout(header_layout)
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setPlainText(text)
        self.text_edit.setPlaceholderText("输入您的信息...")
        main_layout.addWidget(self.text_edit, 1)
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        footer_layout.addWidget(cancel_button)
        submit_button = QPushButton("完成")
        submit_button.clicked.connect(self.accept)
        footer_layout.addWidget(submit_button)
        main_layout.addLayout(footer_layout)

    def get_text(self):
        return self.text_edit.toPlainText()


class DigitalHumanApp(QMainWindow):
    SUGGESTIONS = [
        "想查询一下社保的缴纳情况和相关的信息",
        "查询当地医保办理需要哪些手续？",
        "公积金提取步骤以及相关的信息",
        "其他热点问题",
    ]

    MEDICAL_SUGGESTIONS = [
        "办理医保需要哪些材料？",
        "医保查询",
        "医保报销",
    ]

    def __init__(self):
        super().__init__()
        self.voice_active = False
        self.sound_enabled = True
        self.setWindowTitle("政务服务数字人 - 桌面版示例")
        self.resize(480, 860)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet("background-color: #e0e0e0;")
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central)
        device_frame = QFrame()
        device_frame.setObjectName("deviceFrame")
        device_frame.setStyleSheet(
            "#deviceFrame {"
            " background-color: #ffffff;"
            " border: 3px solid #333333;"
            " border-radius: 36px;"
            " padding: 14px;"
            "}"
        )
        device_frame.setFixedSize(400, 780)
        layout.addWidget(device_frame)
        device_layout = QVBoxLayout(device_frame)
        device_layout.setContentsMargins(0, 0, 0, 0)
        device_layout.setSpacing(0)
        screen = QFrame()
        screen.setObjectName("screen")
        screen.setStyleSheet(
            "#screen {"
            " background-color: #ffffff;"
            " border: 2px solid #b0b0b0;"
            " border-radius: 28px;"
            "}"
        )
        device_layout.addWidget(screen)
        screen_layout = QVBoxLayout(screen)
        screen_layout.setContentsMargins(0, 0, 0, 12)
        screen_layout.setSpacing(12)
        self._add_status_bar(screen_layout)
        self._add_back_button(screen_layout)
        self._add_avatar_row(screen_layout)
        self._add_conversation_area(screen_layout)
        self._add_info_modules(screen_layout)
        self._add_input_area(screen_layout)

    def _add_status_bar(self, parent_layout):
        bar = QFrame()
        bar.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #f0f0f0;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 6, 16, 6)
        layout.setSpacing(8)
        time_label = QLabel("9:41")
        time_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(time_label)
        layout.addStretch()
        layout.addWidget(QLabel("热点"))
        layout.addWidget(QLabel("热点"))
        battery = QLabel("电量 85%")
        layout.addWidget(battery)
        parent_layout.addWidget(bar)

    def _add_back_button(self, parent_layout):
        frame = QFrame()
        frame.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 0, 16, 0)
        back_button = QPushButton("←")
        back_button.setFixedSize(40, 40)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setStyleSheet(
            "QPushButton {"
            " background-color: #ffffff;"
            " border: 2px solid #999999;"
            " border-radius: 20px;"
            " font-size: 20px;"
            "}"
            "QPushButton:hover {"
            " background-color: #f3f3f3;"
            "}"
        )
        back_button.clicked.connect(self._on_back)
        layout.addWidget(back_button)
        layout.addStretch()
        parent_layout.addWidget(frame)

    def _add_avatar_row(self, parent_layout):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.addStretch()
        history_button = self._pill_button("历史")
        history_button.clicked.connect(lambda: self._notify("历史记录功能待接入"))
        layout.addWidget(history_button)
        profile_button = self._pill_button("我的")
        profile_button.clicked.connect(lambda: self._notify("个人中心功能待接入"))
        layout.addWidget(profile_button)
        self.sound_button = self._pill_button("声音:开")
        self.sound_button.clicked.connect(self._toggle_sound)
        layout.addWidget(self.sound_button)
        notify_button = self._pill_button("消息")
        notify_button.clicked.connect(lambda: self._notify("暂无新的消息"))
        layout.addWidget(notify_button)
        parent_layout.addWidget(frame)

    def _pill_button(self, text):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedHeight(36)
        button.setStyleSheet(
            "QPushButton {"
            " background-color: #ffffff;"
            " border: 2px solid #999999;"
            " border-radius: 18px;"
            " padding: 6px 16px;"
            " color: #000000;"
            "}"
            "QPushButton:hover {"
            " background-color: #f5f5f5;"
            "}"
        )
        return button

    def _add_conversation_area(self, parent_layout):
        # 尝试加载本地 index.html 用于 UE5 Pixel Streaming
        html_path = Path(__file__).with_name('index.html')
        if html_path.exists():
            webview = QWebEngineView()
            webview.load(QUrl.fromLocalFile(str(html_path)))
            parent_layout.addWidget(webview, 1)
        else:
            # 如果 index.html 不存在，显示占位符
            frame = QFrame()
            frame.setStyleSheet(
                "background-color: #fdfdfd;"
                "border: none;"
            )
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(24, 12, 24, 12)
            layout.setSpacing(12)
            layout.addStretch()
            portrait = QLabel("数字人图像占位")
            portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
            portrait.setStyleSheet(
                "background-color: #f3f3f3;"
                "border: 2px dashed #cccccc;"
                "border-radius: 20px;"
                "padding: 24px;"
                "color: #666666;"
            )
            layout.addWidget(portrait)
            video = QLabel("视频流区域（已配置 UE5 Pixel Streaming - 等待 index.html）")
            video.setAlignment(Qt.AlignmentFlag.AlignCenter)
            video.setWordWrap(True)
            video.setStyleSheet(
                "background-color: #f8f8f8;"
                "border: 2px solid #dddddd;"
                "border-radius: 16px;"
                "padding: 24px;"
                "color: #555555;"
            )
            layout.addWidget(video)
            layout.addStretch()
            parent_layout.addWidget(frame, 1)

    def _add_info_modules(self, parent_layout):
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)
        layout.addWidget(self._info_module("政务服务推荐", "根据您的历史记录，已为您准备常用事项。"))
        layout.addWidget(self._info_module("便民服务", "天气、出行、医疗等信息一站式查看。"))
        parent_layout.addWidget(container)

    def _info_module(self, title, description):
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: #fafafa;"
            "border: 2px solid #e0e0e0;"
            "border-radius: 16px;"
        )
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #555555;")
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        return frame

    def _add_input_area(self, parent_layout):
        container = QFrame()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)
        self._build_suggestions(layout)
        self._build_medical_overlay(layout)
        self._build_input_controls(layout)
        parent_layout.addWidget(container)

    def _build_suggestions(self, parent_layout):
        self.suggestions_frame = QFrame()
        self.suggestions_frame.setStyleSheet(
            "background-color: #ffffff;"
            "border: 1px solid #dddddd;"
            "border-radius: 16px;"
        )
        layout = QVBoxLayout(self.suggestions_frame)
        layout.setContentsMargins(16, 12, 16, 12)
        header_layout = QHBoxLayout()
        header_label = QLabel("猜你想问")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        self.suggestions_close = QPushButton("收起")
        self.suggestions_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.suggestions_close.setFixedHeight(28)
        self.suggestions_close.setStyleSheet(
            "QPushButton {"
            " border: none;"
            " color: #1E3A8A;"
            " padding: 4px 8px;"
            "}"
            "QPushButton:hover {"
            " color: #102a66;"
            "}"
        )
        self.suggestions_close.clicked.connect(self._toggle_suggestions)
        header_layout.addWidget(self.suggestions_close)
        layout.addLayout(header_layout)
        self.suggestions_list = QListWidget()
        self.suggestions_list.setStyleSheet(
            "QListWidget {"
            " border: none;"
            " outline: none;"
            "}"
            "QListWidget::item {"
            " padding: 10px 8px;"
            " border-radius: 12px;"
            "}"
            "QListWidget::item:selected {"
            " background-color: #e8f1ff;"
            " color: #1E3A8A;"
            "}"
        )
        for item_text in self.SUGGESTIONS:
            QListWidgetItem(item_text, self.suggestions_list)
        self.suggestions_list.itemClicked.connect(self._on_suggestion_clicked)
        layout.addWidget(self.suggestions_list)
        parent_layout.addWidget(self.suggestions_frame)

    def _build_medical_overlay(self, parent_layout):
        self.medical_frame = QFrame()
        self.medical_frame.setVisible(False)
        self.medical_frame.setStyleSheet(
            "background-color: #fafafa;"
            "border: 1px solid #e0e0e0;"
            "border-radius: 12px;"
        )
        layout = QVBoxLayout(self.medical_frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)
        for text in self.MEDICAL_SUGGESTIONS:
            button = QPushButton(text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet(
                "QPushButton {"
                " background-color: #ffffff;"
                " border: 1px solid #d0d0d0;"
                " border-radius: 10px;"
                " padding: 6px 12px;"
                " text-align: left;"
                "}"
                "QPushButton:hover {"
                " background-color: #f1f5ff;"
                "}"
            )
            button.clicked.connect(lambda _, value=text: self._set_input_text(value))
            layout.addWidget(button)
        parent_layout.addWidget(self.medical_frame)

    def _build_input_controls(self, parent_layout):
        frame = QFrame()
        frame.setStyleSheet(
            "QFrame {"
            " background-color: #f5f5f5;"
            " border: 1px solid #dddddd;"
            " border-radius: 18px;"
            "}"
        )
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        self.input_field = AutoResizingPlainTextEdit()
        layout.addWidget(self.input_field, 1)
        button_column = QVBoxLayout()
        button_column.setContentsMargins(0, 0, 0, 0)
        button_column.setSpacing(6)
        self.expand_button = QPushButton("全屏")
        self.expand_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.expand_button.setFixedWidth(70)
        self.expand_button.clicked.connect(self._open_fullscreen_editor)
        button_column.addWidget(self.expand_button)
        self.voice_button = QPushButton("点击说话")
        self.voice_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.voice_button.setFixedWidth(70)
        self.voice_button.clicked.connect(self._toggle_voice)
        button_column.addWidget(self.voice_button)
        self.keyboard_button = QPushButton("猜你想问")
        self.keyboard_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.keyboard_button.setFixedWidth(70)
        self.keyboard_button.clicked.connect(self._toggle_suggestions)
        button_column.addWidget(self.keyboard_button)
        button_column.addItem(QSpacerItem(20, 10))
        layout.addLayout(button_column)
        parent_layout.addWidget(frame)

    def _on_back(self):
        self._notify("返回操作已触发，当前示例未接入上一页。")

    def _toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        state = "开" if self.sound_enabled else "关"
        self.sound_button.setText(f"声音:{state}")
        self._notify(f"声音已切换为{state}")

    def _toggle_voice(self):
        self.voice_active = not self.voice_active
        text = "停止说话" if self.voice_active else "点击说话"
        self.voice_button.setText(text)
        if self.voice_active:
            self._notify("开始录音（示例状态）")
        else:
            self._notify("结束录音（示例状态）")

    def _toggle_suggestions(self):
        visible = self.suggestions_frame.isVisible()
        self.suggestions_frame.setVisible(not visible)
        self.suggestions_close.setText("收起" if not visible else "展开")
        label = "猜你想问" if visible else "收起建议"
        self.keyboard_button.setText(label)

    def _on_suggestion_clicked(self, item):
        text = item.text()
        self._set_input_text(text)
        self._maybe_toggle_medical_overlay(text)

    def _maybe_toggle_medical_overlay(self, text):
        if "医保" in text:
            self.medical_frame.setVisible(True)
        else:
            self.medical_frame.setVisible(False)

    def _set_input_text(self, text):
        self.input_field.setPlainText(text)
        self.input_field.setFocus()
        self.input_field.moveCursor(self.input_field.textCursor().End)

    def _open_fullscreen_editor(self):
        dialog = FullscreenInputDialog(self.input_field.toPlainText(), self)
        if dialog.exec():
            self.input_field.setPlainText(dialog.get_text())

    def _notify(self, message):
        QMessageBox.information(self, "提示", message)


def main():
    app = QApplication(sys.argv)
    window = DigitalHumanApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
