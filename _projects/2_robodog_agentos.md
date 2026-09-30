---
layout: page
title: robodog 与 AgentOS 机器人实时操作系统
description: 机器狗高自由度运动控制库，结合 6 轴机械臂与 WebXR 空间交互，支持姿态估计、UWB 定位、自主避障与手势抓取。
img: assets/img/projects/placeholder.png
importance: 2
category: 具身智能
related_publications: false
---

### 🐾 项目架构

四足机器狗作为复合移动作业载体，不仅需要稳定的步态规划，还需要与高层智能代理（Agent）及感知系统顺畅通讯。**robodog** 与 **AgentOS** 提供了一套软硬协同的实时系统解决方案。

---

### 🚀 核心技术与功能

* **运动学与步态规划**：
  * 支持对角步态、爬行步态等多种动态步态自适应调节
  * 融合 IMU 与多路编码器进行高频扩展卡尔曼滤波（EKF）位姿估计
* **移动作业（Mobile Manipulation）**：
  * 在四足机身上挂载 6 轴轻量化机械臂
  * 通过 WebXR 与 Three.js 搭建沉浸式手势映射遥操作界面，实现隔空视觉引导抓取
* **高精度空间定位**：
  * 深度集成超宽带（UWB）微基站定位系统，提供厘米级室内绝对坐标反馈
* **ROS/ROS2 通信中间件**：
  * 设计轻量级节点通信协议，保障高频运控环路（1kHz）与低频感知推理环路的解耦隔离
