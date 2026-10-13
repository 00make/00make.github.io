---
layout: page
title: treehollow 校园匿名社交平台与开源社区
description: 发起并主开发的校园匿名社区 bucthole.com，多子域名架构 + WebSocket 实时推送 + reCAPTCHA 风控，2021 年 Web 与 iOS 双端上线，成为校内热议社区，仓库已开源并被开发者社区使用。
img: assets/img/projects/treehollow.png
importance: 7
category: 开源生态与创业
related_publications: false
---

### 🌐 项目历程

**2019-10 ~ 2021-09** 在大学期间发起并主导开发校园匿名社区 **北化树洞（bucthole.com）**，为高校学生提供安全、纯粹的交流与互助空间。本人独立建立并运营域名与 `bucthole` GitHub 组织，负责架构选型、开发与社区运营，并指导协作者完成部署。

---

### 📈 架构与运营亮点

- **多子域名服务化架构**：

  - `bucthole.com` —— 主页与社区入口
  - `tapi` —— API 服务层
  - `ws` —— Android 端 WebSocket 实时推送通道
  - `re` —— reCAPTCHA 人机验证服务
  - `i` —— 图片资源服务
  - `web` —— 网页版客户端
  - `terms` —— 用户协议与合规文本

- **技术栈**：`treehollow` / React / WebSocket / reCAPTCHA / iOS · Android · Web 三端；网页版基于 P 大树洞开源 web 版（`xmcp`）、React 与 IcoMoon 等开源项目二次构建，而非从零造轮子。

- **隐私与风控设计**：在树洞内以「开发人员」身份公开说明后台无法看到真实身份，把匿名性做成产品契约而不是口头承诺；配套敏感信息过滤与社区自治规范，保障校园社区健康运营。

- **上线与影响**：2021-08-09 `bucthole.com` 正式上线，2021-08-13 iOS 版本接入 App Store（`treehollow` 客户端），上线即成为校内热议社区，用户主动讨论其隐私机制。

- **开源**：完整仓库开源 [`github.com/bucthole/bucthole`](https://github.com/bucthole/bucthole)，已开源并被开发者社区使用。

---

### 🔗 这段经历留下了什么

第一次独立完成「架构拆分 → 安全与隐私设计 → 多端交付 → 社区自治」的完整闭环。后来做开发者生态与机器人开源 SDK 时反复用到的思路——把复杂系统拆成职责单一的服务、把用户信任写进产品设计、用开源社区承接自己照顾不过来的需求——起点都在这里。
