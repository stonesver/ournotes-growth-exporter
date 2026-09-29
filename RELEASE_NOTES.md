# v0.1.0-alpha.2 — 解压即可使用

已内置台港澳服 BHK 应用配置，无需自行配置。配置用于标识游戏和渠道，不包含任何玩家账号、密码或会话。

1. 下载对应 ZIP 并完整解压：Windows x64 打开 `Start.cmd`；Mac Apple Silicon 打开 `Start.command`。两个包均约 19.6 MB，无需安装 Python。
2. 在本机页面用 BHK 邮箱密码登录，读取后下载养成 JSON。
3. 回到 [Our Notes 配卡工具](https://ournotes.stonebg.cn/global/zh-CN/tools/deck-builder/)，在「我的卡库 → 从游戏导入我的养成」选择 JSON，核对后应用。

登录请求从本机发送到官方服务，不经过资料站服务器。非官方工具存在账号限制风险；登录可能使游戏会话失效，额外验证不支持、不自动重试。回忆加成需自行设置。

Mac 仅支持 Apple Silicon，尚未完成 Apple 公证；不要关闭系统安全保护。源码许可不代表官方接口授权。

验证：43 项回归测试通过；Mac 最终 ZIP 解压后通过包含应用配置的离线自检；官方 SDK 初始化成功（未使用玩家凭据）。Windows 新版离线验证结果见本仓库 Actions，离线检查不代表 Windows 真实账号登录验收。

下载 `SHA256SUMS` 可核对两个 ZIP 的 SHA-256。
