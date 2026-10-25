# v0.2.0-alpha.1 — 港澳台、EN、韩服养成导出

本机登录页可选择港澳台、EN 或韩服。支持 BHK 邮箱密码账号，读取已有角色的角色卡、留影、乐器、角色评级和 TGW，并在 JSON 中记录所属区服。网站导入时请选择同一区服；未读取的数据保持未知，不补成满级。

- 自动协商官方要求的客户端版本；遇到维护、额外验证或账号错误时停止。
- 公开包仅包含 SDK 配置模板，不包含有效 SDK 应用配置、玩家凭据或账号快照。首次运行需载入已有有效配置；没有配置时可使用网站邮箱登录入口。旧版 v0.1.0-alpha.3 仅支持港澳台。
- Windows x64 解压后打开 `Start.cmd`；Mac Apple Silicon 打开 `Start.command`。无需另装 Python。Google 游戏授权尚未接通。

验证：最终 Mac 可执行程序通过离线自检，并用同一探测账号完成三服实际养成读取；源码与 Windows 包的共享模块一致。此验证不代表游戏内逐项人工对账。Windows 桌面真实登录、Mac Developer ID 签名、公证和互联网下载后的 Gatekeeper 验收仍未完成。

三个 ZIP 的摘要见 `SHA256SUMS`。完整使用步骤见 [README](https://github.com/stonesver/ournotes-growth-exporter/blob/v0.2.0-alpha.1/README.md)。
