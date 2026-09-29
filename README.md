# Our Notes 本地养成导出工具

已内置台港澳服 BHK 应用配置，下载解压即可使用，无需自行配置。

- [下载 Mac / Windows 预览包](https://github.com/stonesver/ournotes-growth-exporter/releases/tag/v0.1.0-alpha.2)，每个约 19.6 MB。
- [打开 Our Notes 配卡工具](https://ournotes.stonebg.cn/global/zh-CN/tools/deck-builder/)。

请勿在 Issues 中提交账号、密码、令牌、个人导出或原始抓包。

台港澳服 BHK 邮箱密码账号。电脑直接连接官方服务，不需要 ADB；读取角色卡、留影、乐器、角色评级和 TGW，导出 JSON 后可导入 Our Notes 配卡工具。

## Windows 便携版

1. 完整解压 ZIP，不要在压缩包中直接运行。
2. 双击 `Start.cmd`，浏览器会打开本机页面。无需额外安装 Python，也无需管理员权限。
3. 工具自动载入内置的台港澳服应用配置，无需自行配置。
4. 在本机页面输入邮箱和密码，读取后点击「下载养成 JSON」。
5. 到网站配卡工具的「选卡库 → 我的卡库 → 从游戏导入我的养成」选择 JSON，核对后应用。

关闭终端或按 Ctrl+C 退出。默认不自动写文件，结果仅在进程内存保留到退出；下载后的 JSON 由你自行保管。每次读取会清除上一次内存结果；需要保留时先下载备份。登录可能使官方游戏中的会话失效，验证码等额外验证不支持、不自动重试。

目标系统为 Windows 10/11 x64。Windows 便携包会通过 GitHub Windows 运行器进行离线启动检查；该检查不代表真实账号登录验收。它不是手机应用，也不是浏览器直接运行的程序。

## Mac 便携版（Apple Silicon）

完整解压后双击 `Start.command`。工具自带运行环境，无需安装 Python，会打开终端和本机浏览器页面；后续登录和 JSON 导入流程与 Windows 相同，无需自行配置。关闭终端或按 Ctrl+C 退出。

当前包仅适用于 Apple Silicon（M 系列芯片），不适用于 Intel Mac。当前为开发验证候选，未完成 Apple Developer ID 签名和公证；本机运行通过不代表从互联网下载后的 Gatekeeper 验收通过。不要通过关闭系统安全保护来运行。正式发布前还需完成平台分发验收。

## 从源码运行（Windows / macOS / Linux）

Python 3.9 或更新版本：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python launcher.py
```

Windows 将 `.venv/bin/python` 换成 `.venv\Scripts\python.exe`。

`python launcher.py --self-test` 检查依赖、RSA 运算和本机 HTTP 服务，不连接官方服务器，不使用真实账号。

## SDK 配置

已内置 `sdk.bhk.xml`，包含游戏/渠道标识及应用签名 key，与玩家账号无关。源码版和便携版启动时均自动载入。它不是个人登录令牌，仍需玩家自行输入邮箱和密码。

需要更换配置时，可在浏览器选择不超过 6 KB 的最小 XML，只在本次运行生效；或将自定义配置保存为工具根目录的 `sdk.xml`，优先于内置配置载入。`sdk.example.xml` 仅是结构模板。不要在配置里填写账号或密码。

分发包含上述共享应用配置，不包含个人快照、邮箱、密码或登录令牌。源码许可只覆盖本工具代码，官方 SDK、游戏资源和第三方依赖保留各自权利及许可。

本工具为非官方项目。源码许可不覆盖第三方应用配置及游戏资源，也不代表官方认可第三方客户端或接口用途。

## 可审查边界

- 仅监听 `127.0.0.1` 的随机端口，校验 Host、Origin 和本次启动 nonce。
- 官方服务器与读取方法在源码中固定，不允许配置任意目标地址。
- 密码输入在提交后清空；不写凭据日志、状态文件或导出文件。
- 默认仅内存保存最近一次养成结果。显式传入 `--output 新文件.json` 才自动保存，且不会覆盖旧文件。
- 不保存设备绑定或账号会话；退出后再次读取需要重新输入。
- JSON 只导出支持的养成字段。未知字段不补全；网站按当前资料重新换算等级，回忆加成等未读取项目保持原设置。

网页不能直接执行本工具。完全免安装请使用网站的网页登录；本地工具的目的在于让登录请求从自己的电脑发送。
