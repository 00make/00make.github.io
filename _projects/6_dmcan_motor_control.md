---
layout: page
title: dmcan 电机控制库与 ROS 动力学集成
description: 封装达妙（DM）无刷电机 CAN 总线力矩与阻抗控制算法，构建基于 ROS/ROS2 的分布式实时驱动框架。
img: assets/img/projects/writer2.jpg
importance: 6
category: 边缘智能与嵌入式
related_publications: false
---

### ⚙️ 项目背景

在四足机器人、双足步行机器人以及高动态机械臂的研发中，高频力控伺服（Impedance/Torque Control）是决定运控柔顺性与抗扰动能力的核心基础。

**dmcan** 针对达妙系列一体化无刷关节电机，提供了一套轻量、鲁棒且跨平台的 C++/Python 控制接口与 ROS 驱动包。

---

### 🛠️ 技术特点

* **完整协议封装**：
  * 支持 MIT 模式（位置-速度-前馈力矩-Kp-Kd）、位置速度模式与直接力矩模式
  * 毫秒级 CAN 总线丢包检测与状态自动恢复机制
* **动力学与仿真兼容**：
  * 输出标准 ROS `sensor_msgs/JointState` 与 `trajectory_msgs` 接口
  * 便于无缝接入 MoveIt、Isaac Gym 与 Pinocchio 动力学计算库
* **开发者友好**：
  * 开源命令行调试工具，支持单关节示教与图形化阶跃响应分析
