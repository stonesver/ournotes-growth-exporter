# v0.1.0-alpha.1 — 本地养成导出预览版

在自己的电脑读取台港澳服 BHK 账号养成，导出 JSON 后导入 Our Notes 配卡工具。密码与会话不经过资料站。

## 下载与使用

- Windows 10/11 x64：`ournotes-growth-windows-x64.zip`，19.6 MB，完整解压后运行 `Start.cmd`。
- Mac Apple Silicon：`ournotes-growth-macos-arm64.zip`，19.6 MB，完整解压后运行 `Start.command`；不支持 Intel Mac。
- 源码：使用本 Release 下的 Source code，或者直接浏览仓库。
- 文件摘要：下载 `SHA256SUMS` 核对。

**本公开包不包含有效 SDK 配置，需自行提供有权使用的最小 SDK XML。模板不能直接用于登录。** 首次在本机页面选择 XML，或将有效配置命名为 `sdk.xml` 放到工具根目录。

Mac 候选从最终 ZIP 解压后通过离线启动自检；未完成 Developer ID 签名与 Apple 公证，不建议关闭系统保护来运行。Windows 发布前未有本机 Windows 验收，后续 GitHub Actions 仅验证无凭据离线启动，不等同于真实游戏登录通过。

本工具不属于官方客户端，开源许可不代表官方接口授权。登录可能使原游戏会话失效，额外验证不支持、不自动重试。导出仅覆盖五类已支持养成，回忆加成等未知项目不补全。
