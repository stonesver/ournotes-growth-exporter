# v0.2.0-alpha.2 — 三服养成导出，恢复解压即用

Windows、Mac 和源码发行 ZIP 内置旧版使用的 SDK 应用配置。完整解压后启动即可选择港澳台、EN 或韩服并输入 BHK 邮箱密码，无需自行获取或填写 SDK 配置。配置不包含玩家账号、密码或登录令牌。

- Windows x64 打开 `Start.cmd`；Mac Apple Silicon 打开 `Start.command`，均无需另装 Python。
- 支持已有角色的角色卡、留影、乐器、角色评级和 TGW。导出的 JSON 须在网站同一区服导入。
- v0.2.0-alpha.1 用户请更新并完整解压；v0.1.0-alpha.3 及更早版本仅支持港澳台。Google 游戏授权尚未接通。

验证：最终 Mac ZIP 解压后直接使用内置配置，通过离线自检和三服真实养成读取，全程未手动载入配置。三个 ZIP 均验证完整文件摘要及内置配置一致性。Windows 离线自检由发行工作流单独验证；真实 Windows 桌面登录、游戏内逐项人工对账、Mac Developer ID 签名、公证和互联网下载后的 Gatekeeper 验收仍未完成。

下载文件摘要见 `SHA256SUMS`。使用说明见 [README](https://github.com/stonesver/ournotes-growth-exporter/blob/v0.2.0-alpha.2/README.md)。Git 源码仓库只保留配置模板，维护者通过显式打包参数提供发行用配置。
