# FastAPI WebRTC Video Chat

FastAPI WebRTC Video Chat 是一个使用 FastAPI 和 WebRTC 技术构建的实时视频聊天应用程序。该项目特别实现了一个有趣的功能，即在视频聊天中将用户的头像替换为吴彦祖的头像。

## 功能

- **实时视频传输**：实现端到端的实时视频通信。
- **头像替换**：在视频流中将用户头像替换为指定图片（如吴彦祖的头像）。
- **P2P 连接**：使用 WebRTC 技术建立点对点连接。

## 技术栈

- **FastAPI**：用于构建 API 的现代、快速的 Web 框架。
- **WebRTC**：支持网页浏览器进行实时语音对话或视频对话的技术。
- **aiortc**：AsyncIO 的 WebRTC 库。
- **Python**：编程语言。

## 安装

1. 克隆项目到本地：

```bash
git clone https://github.com/yourusername/FastAPI-WebRTC-Video-Chat.git
cd FastAPI-WebRTC-Video-Chat
````

2. 创建虚拟环境并激活：

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 运行

```bash
uvicorn main:app --reload
```
应用程序将在 http://127.0.0.1:8000 启动。

使用
打开浏览器，访问应用程序的地址。
允许浏览器访问摄像头和麦克风。
点击“start”按钮以启动。
在下方的框中你的头像将自动替换为吴彦祖的头像。
注意事项
确保在部署应用程序之前配置好所有必要的环境变量和安全设置。
由于使用了 WebRTC，确保您的服务器可以处理实时的网络连接。
贡献
欢迎任何形式的贡献。如果你发现一个 bug 或者想要添加一个新的功能，请创建一个 issue 或者发起一个 pull request。