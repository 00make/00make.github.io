---
layout: page
title: 单卡极限部署：80层 VLA 模型真机闭环
description: 在单张 32GB RTX 5090 消费级显卡上跑通 80 层 Decoder 架构 VLA 模型（WALL-OSS）全链路微调 + LeRobot SO-101 机械臂真机闭环，端到端延迟低至 33–100ms。
img: assets/img/projects/vslam1.jpg
importance: 1
category: 具身智能
related_publications: false
---

### 🌟 项目背景与核心痛点

高校实验室与个人开发者在具身智能（Embodied AI）研究中，往往面临严重的算力瓶颈——缺乏 8 卡高端服务器，无法对大规模 Vision-Language-Action (VLA) 模型进行本地微调与真实机械臂部署。

本项目直击这一核心痛点，探索**单张消费级显卡下的极端工程性能优化**，成功在单张 32GB 显存显卡上跑通超大参数量模型微调与真机交互闭环。

---

### ⚡ 核心技术方案与突破

* **极限显存优化**：
  * 引入 8-bit AdamW 优化器，显存占用直降 50%
  * 深度启用 Activation Checkpointing（梯度检查点）技术
  * 设计 256 步梯度累积策略，在有限显存下模拟超大 Batch Size 稳定收敛
* **端到端真机超低延迟闭环**：
  * 对接 LeRobot SO-101 机械臂低成本硬件
  * 视觉输入到动作输出全链路工程重构，将模型推理与真机动作响应延迟压至 **33–100ms**
* **开源高质量数据集**：
  * 自主采集 30 条 / 8,199 帧高质量机械臂遥操作轨迹，涵盖多物体分拣与复杂空间动作
  * 完整数据集与评估权重已同步开源至 HuggingFace

---

### 🔗 开源与相关资源

* **开源代码**：[GitHub - 00make](https://github.com/00make)
* **数据集**：HuggingFace 机械臂轨迹数据集
* **课件报告**：[清华大学具身智能俱乐部专题分享](/talks/)
