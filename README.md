# Digital Human UI - Python Desktop Application

将 HTML 政务服务数字人 UI 转换成 Python 桌面应用，集成 UE5 Pixel Streaming 实时视频流。

## 功能特性

- ✅ **PyQt6 原生桌面应用**：完全用 Python 实现跨平台 UI
- ✅ **UE5 Pixel Streaming 集成**：嵌入 WebEngine 加载原始 HTML，自动连接 UE5 实时渲染
- ✅ **政务服务场景**：社保、医保、公积金等查询建议
- ✅ **自适应输入框**：支持全屏编辑、语音按钮、联想问答
- ✅ **响应式布局**：模拟手机设备外观（375×812）

## 项目结构

```
.
├── app.py                 # PyQt6 主应用程序
├── index.html             # UE5 Pixel Streaming 客户端页面
├── index1.html            # 备用页面
├── Images01.png           # 数字人形象图片
├── bj.jpg                 # 背景图片
└── README.md              # 本文件
```

## 安装依赖

```bash
# 使用清华镜像加快安装（推荐）
pip install PyQt6 PyQt6-WebEngine -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=120

# 或使用默认源
pip install PyQt6 PyQt6-WebEngine
```

## 运行应用

```bash
python app.py
```

应用启动后会：
1. 加载本地 `index.html`
2. 自动初始化 Pixel Streaming 客户端
3. 连接到 UE5 信令服务器（默认 `ws://localhost:80`）
4. 显示实时视频流和交互界面

## UE5 Pixel Streaming 配置

### 前置要求

1. **UE5 项目**：启用 Pixel Streaming 插件
2. **信令服务器**：运行 Epic Games 提供的 signalling server
3. **网络**：确保信令服务器地址可访问

### 启动步骤

#### 1. UE5 编辑器中运行

```
Cmd: C:\ue5project\Binaries\Win64\UE4Editor.exe -game -WINDOWED -ResX=1920 -ResY=1080 -PixelStreamingIP=127.0.0.1 -PixelStreamingPort=8888 -RenderOffScreen
```

#### 2. 启动信令服务器

```bash
cd SignallingWebServer
node server.js --httpPort=80 --StreamerPort=8888
```

#### 3. 修改连接地址（如需）

编辑 `index.html` 中的 `psConfig`：

```javascript
const psConfig = {
    initialSettings: {
        AutoConnect: true,
        AutoPlayVideo: true,
        StartVideoMuted: true,
    },
    signallingUrl: 'ws://localhost:80'  // 改为你的服务器地址
};
```

## 主要代码组件

### `app.py` - PyQt6 应用

| 类 | 功能 |
|---|---|
| `AutoResizingPlainTextEdit` | 自适应高度文本编辑框 |
| `FullscreenInputDialog` | 全屏输入对话框 |
| `DigitalHumanApp` | 主应用窗口 |

### 核心交互

- **返回按钮**：返回上一页
- **头像行**：历史、个人中心、声音开关、消息
- **猜你想问**：联想建议列表
- **医保弹窗**：医保相关建议细分
- **输入区**：自动高度、全屏编辑、语音模式
- **WebView**：嵌入 Pixel Streaming 客户端

## 常见问题

### 1. ModuleNotFoundError: No module named 'PyQt6'

确保使用正确的 Python 环境安装依赖，或明确指定 Python 路径：

```bash
C:\Python313\python.exe -m pip install PyQt6 PyQt6-WebEngine
```

### 2. QUrl 类型错误

已修复，使用 `QUrl.fromLocalFile()` 正确转换文件路径。

### 3. PixelStreaming 连接失败

检查：
- 信令服务器是否运行
- UE5 Pixel Streaming 是否启用
- 网络连接是否正常
- 地址是否正确（默认 `ws://localhost:80`）

## 后续开发计划

- [ ] 接入真实后端服务（社保、医保数据查询）
- [ ] 添加语音识别和合成（TTS）
- [ ] 支持更多政务场景
- [ ] 打包成 .exe 可执行文件
- [ ] 多语言支持
- [ ] 性能优化和错误处理完善

## 技术栈

- **UI 框架**：PyQt6 + PyQt6-WebEngine
- **渲染引擎**：UE5 Pixel Streaming
- **前端**：HTML5 + JavaScript + Tailwind CSS
- **通信**：WebRTC + WebSocket
- **平台**：Windows / macOS / Linux

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提 Issue 或 PR。
