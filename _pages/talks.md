---
layout: page
title: 演讲
permalink: /talks/
description: 公开技术演讲、开发者大会、高校学术报告与实战工作坊。记录从校园极客到具身智能前沿的实战思考与工程总结，提供完整课件 PDF、演讲大纲与现场记录。
nav: true
nav_order: 3
---

### 🎙️ 精选公开演讲、技术研讨与实战工坊

> “论文里的机器人永远不会摔倒，摩擦力永远是线性的。但现实不是。算法可以在云端飘逸，但硬件必须在泥泞里打滚——请把手弄脏（Get your hands dirty），去感受物理世界的真实阻抗。”

---

#### 🤖 一、 具身智能与大模型软硬协同 (Embodied AI & VLA)

<div class="card mb-4 shadow-sm border-left-primary">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-primary">高校学术俱乐部分享</span>
      <span class="text-muted small">2026 · 清华大学</span>
    </div>
    <h4 class="card-title font-weight-bold">《代码的重量——如何用一行 Python 撬动物理世界》</h4>
    <h6 class="card-subtitle text-muted mb-3">副题：跨越“虚实鸿沟”——从 GitHub 开源到具身智能的工程着陆 | 主办：清华大学具身智能俱乐部 (THU Embodied AI Club)</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>面对高校顶尖机器人与 AI 开发者，深度剖析从纯数字世界（LLM / VLM）走向物理实体世界的阻抗匹配。开篇直面 2025 国际人形机器人技能大赛夺冠背后的“工程幸存者偏差”，讲述在决赛前一周为消除步态抖动连续熬夜调试、在焊锡焦味与电机过热中攻坚真机闭环的战壕经历；详解消费级单卡上优化 80 层 VLA 模型推理与 LeRobot 机械臂低延迟控制的软硬件协同方法。
    </p>
    <div class="bg-light p-3 rounded mb-3">
      <strong>🔥 核心观点与金句：</strong>
      <ul class="mb-0 mt-2 pl-3">
        <li><strong>第一性原理突破门槛</strong>：从在宿舍自制微米级无掩模光刻机被 CERN 关注，到具身智能开发——“昂贵的设备从来不是壁垒，对物理第一性原理的理解才是。”</li>
        <li><strong>先造好用的铲子</strong>：痛陈市售机器狗封闭黑盒与糟糕 SDK，逆向打造开源底层驱动 <code>dmcan</code> 与 <code>robodog</code>，“在这个赛道，造好用的铲子，有时候比挖金矿更有价值。”</li>
        <li><strong>做“缝合怪”而非“完美主义者”</strong>：不要苦等通用 AGI 降临才去动身，先用人类生物大脑借助 WebXR/VR 遥操作接管机器躯体，为未来大模型沉淀真实的 Ground Truth。</li>
        <li><strong>请把手弄脏 (Get your hands dirty)</strong>：鼓励学术开发者走出无摩擦力的仿真环境，下场听电机异响、解决电磁温漂，成为物理世界的开拓者。</li>
      </ul>
    </div>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/代码的重量——如何用一行%20Python%20撬动物理世界_compressed.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载完整演示课件 PDF</a>
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-success">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-success">顶尖创新答辩</span>
      <span class="text-muted small">2026.03 · 具身智能创新评审</span>
    </div>
    <h4 class="card-title font-weight-bold">《打通具身智能落地的最后一公里：基于单卡的 WALL-OSS 机械臂全栈部署闭环》</h4>
    <h6 class="card-subtitle text-muted mb-3">“具亮计划 2026” 答辩演讲 | 汇报人：张振尧（零零后科技）</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>针对具身智能动辄依赖 8 卡集群与高昂算力的痛点，系统汇报团队在<strong>单张 32GB 显存消费级显卡 (RTX 5090)</strong> 上实现 80 层 VLA 大模型端到端微调与 LeRobot SO-101 真机平滑闭环的极致工程突破。现场展示抓取腕带与溜溜球任务的丝滑操作。
    </p>
    <div class="bg-light p-3 rounded mb-3">
      <strong>🔥 硬核技术亮点：</strong>
      <ul class="mb-0 mt-2 pl-3">
        <li><strong>拒绝机械臂抖动的数学基石</strong>：抛弃易受噪声畸变的 Min-Max 归一化，采用 <strong>q1-q99 分位数归一化</strong>；引入 OpenPI RunningStats 架构与 5000 动态 bin 算法，实现在线流式分位数估计，彻底杜绝 OOM。</li>
        <li><strong>紧耦合 MoE 与 Flow Matching</strong>：基于 Qwen2.5-VL 语义底座，语言专家理解指令，动作专家通过 10 步 ODE 连续流匹配（Flow Matching）预测连续平滑流场，解决离散 Token 阶跃抖动。</li>
        <li><strong>算力极限压榨“四板斧”</strong>：8-bit AdamW 显存降 4 倍 + 梯度检查点 (Gradient Checkpointing) + 图像分辨率降至 224 + 单步 Batch=1 配合 <strong>256 步超长梯度累积</strong>，成功攻破单卡显存墙。</li>
        <li><strong>gRPC 毫秒级通信闭环</strong>：云端 Server 处理重推理，本地边缘端高频采集双目视频并执行 6-DOF 底层 PID，32 步长 Action Chunk 将端到端闭环延迟压至 33–100ms。</li>
      </ul>
    </div>
    <div class="d-flex flex-wrap gap-2">
      <a href="https://huggingface.co/datasets/00make/so100_teleoperation_dataset" class="btn btn-sm btn-outline-info" target="_blank" rel="noopener noreferrer">🌐 查看 HuggingFace 8199帧物理轨迹数据集</a>
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-info">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-info">社群技术公开课</span>
      <span class="text-muted small">2026 · 开发者社群</span>
    </div>
    <h4 class="card-title font-weight-bold">《Single GPU Full Stack Embodied AI：消费级硬件上的具身智能全栈探索》</h4>
    <h6 class="card-subtitle text-muted mb-3">单卡全栈具身智能实践分享</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>向开源社区开发者系统讲解如何用一台单卡消费级主机完成从机器人硬件搭设、数据遥操作采集（LeRobot / SO-100）、异构传感器 Key Mapping 统一、流式数据微调到轻量化真机部署的全流程，打消初学者“没有算力集群就无法做具身智能”的壁垒。
    </p>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/Single_GPU_Full_Stack_Embodied_AI.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载演示课件 PDF</a>
    </div>
  </div>
</div>

---

#### 🛠️ 二、 开源硬件、极限压榨与工程量产 (Hardware Engineering & Maker)

<div class="card mb-4 shadow-sm border-left-warning">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-warning text-dark font-weight-bold">开源硬件年度盛会特邀演讲</span>
      <span class="text-muted small">2026.09 · 深圳会展中心</span>
    </div>
    <h4 class="card-title font-weight-bold">《从原型到真实应用：跨学科硬件项目的落地实践》</h4>
    <h6 class="card-subtitle text-muted mb-3">第四届嘉立创开源硬件星火会主会场演讲 | 主讲人：张振尧（零零后科技 CEO）</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>在深圳会展中心 3.72:1 超宽屏主会场，面向数千名硬核硬件开发者、嵌入式工程师与创客同仁展开 15 分钟深度主题演讲。通过生动的“个人编年史”叙事，剖析一个跨学科硬件产品如何从学生时代的“玩具原型”一步步走向真实世界量产。
    </p>
    <div class="bg-light p-3 rounded mb-3">
      <strong>🔥 精彩故事与工程干货：</strong>
      <ul class="mb-0 mt-2 pl-3">
        <li><strong>极客起点</strong>：10 岁拆坏 DVD、16 岁用生活费在垃圾桶捡破损 iPhone 4 翻新成功；大学手搓步进电机写字机器人与 550W 高功率动力系统。</li>
        <li><strong>48小时黑客松的极限反转</strong>：首届小红书黑客松巅峰赛，“吹了么”七轴理容机械臂在赛前夜突发连线烧毁，团队通宵重构通信协议，最终在决赛舞台完成全场首次“机械臂全自主抓取并平稳吹干湿发”，斩获硬件赛道大奖。</li>
        <li><strong>跨学科技术融合</strong>：“YOLO 强开物理世界的‘数字领地’”，结合 PaliGemma 与 Pi0.5 轻量化模型，让边缘硬件拥有毫秒级视觉反馈。</li>
        <li><strong>避开量产的“万丈深坑”</strong>：从 1 台手搓 Demo 到 500+ 台规模交付，复盘 4G 射频噪声对音频电路的疯狂干扰、PCB 走线阻抗匹配、供应链元器件断货平替、以及通过自研自动化治具将生产测试成本压缩 70% 的工业级工程方法论。</li>
      </ul>
    </div>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/从原型到真实应用-张振尧-星火会.pptx" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📊 下载星火会超宽屏演示 PPTX</a>
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-danger">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-danger">企业技术分享与实战工坊</span>
      <span class="text-muted small">2025–2026 · 字节跳动</span>
    </div>
    <h4 class="card-title font-weight-bold">《用 Vibe Coding 与 Skill 打造具身智能 Agent：从“手搓”几千行 C++ 到一句话让机器人跳舞》</h4>
    <h6 class="card-subtitle text-muted mb-3">字节跳动 AI+ 主题演讲 / ADG 技术研讨与工作坊 | 主讲人：张振尧</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>传统机器人开发门槛极高，复杂的正逆运动学解算、ROS 环境配置、异构网络接口让大量富有创意的开发者和跨界设计师望而却步。张振尧现场展示如何借助以 Trae 为代表的现代 AI 编码助手开启 <strong>Vibe Coding</strong> 范式，通过自然语言编排 Agent Skill，将开发者从底层繁琐语法与环境报错中解放出来。
    </p>
    <div class="bg-light p-3 rounded mb-3">
      <strong>🔥 现场金句与实践展示：</strong>
      <ul class="mb-0 mt-2 pl-3">
        <li>“以前为了让机器人转个头，我们要面对密密麻麻的运动学方程和抓耳挠腮的编译报错；现在有了 Skill 模块与 AI Agent，<strong>我们不再是写底层的‘码农’，我们是‘导演’，机器人是听话的‘演员’</strong>。”</li>
        <li>现场演示仅用自然语言对话编排，在 10 分钟内完成多足机器人姿态控制与音乐节奏舞蹈编排。</li>
      </ul>
    </div>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/用%20Vibe%20Coding%20与%20Skill%20打造“具身智能”机器人%20Agent_compressed.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载 Vibe Coding 幻灯片 PDF</a>
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-secondary">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-secondary">生态开发者大会</span>
      <span class="text-muted small">2026 · 地瓜机器人</span>
    </div>
    <h4 class="card-title font-weight-bold">《RDK 机器人操作系统与算法演进：从算力芯片到通用运动大脑》</h4>
    <h6 class="card-subtitle text-muted mb-3">地瓜机器人开发者生态大会 | 特邀分享：地瓜生态资深开发者代表 张振尧</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>基于旭日/地瓜 RDK 系列嵌入式边缘算力套件，深入剖析国产端侧芯片在嵌入式 ROS2 桥接、多路 CSI 摄像头硬件编码、轻量化 Yolov8 目标追踪以及多传感器时间同步上的工程优化方案，助力开发者低成本打造高性能机器人系统。
    </p>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/RDK演讲稿_重构版.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载 RDK 演讲文稿 PDF</a>
    </div>
  </div>
</div>

---

#### 💡 三、 智能体变革与黑客松路演 (AI Engineering & Hackathon)

<div class="card mb-4 shadow-sm border-left-info">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-info">大模型工程架构路演</span>
      <span class="text-muted small">2026 · 扣子 AI 开发者大赛</span>
    </div>
    <h4 class="card-title font-weight-bold">《AI Engineering Revolution：智能体驱动的工程范式跃迁》</h4>
    <h6 class="card-subtitle text-muted mb-3">扣子 (Coze) 开发者路演分享</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>探讨大型语言模型从“Chat 对话助手”走向“自动化工程全流程”的变革。深度解析多智能体任务拆解、状态机路由、工具动态调用以及基于上下文记忆的长链路任务执行方案。
    </p>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/AI_Engineering_Revolution_compressed.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载 AI Engineering Revolution 课件 PDF</a>
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-primary">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-primary">NVIDIA 官方优秀案例项目路演</span>
      <span class="text-muted small">2025–2026 · 开发者大赛</span>
    </div>
    <h4 class="card-title font-weight-bold">《PCBTool AI：基于大模型微调的电路硬件设计专家智能体》</h4>
    <h6 class="card-subtitle text-muted mb-3">智能硬件设计与 EDA 自动化路演（该项目入选英伟达官方展台展示案例）</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>介绍利用 NVIDIA NIM 微服务架构与专用电路设计语料微调构建的 PCBTool AI 智能体系统。系统打通了从硬件原理图校验、元器件封装库推荐、阻抗走线建议到 Gerber 制造可行性分析的自动化全流程，将传统数天的硬件原理图初审缩短至数分钟。
    </p>
    <div class="d-flex flex-wrap gap-2">
      <a href="/assets/pdf/talks/1450-1500-PCBToolAI_compressed.pdf" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">📄 下载 PCBTool AI 演示文稿 PDF</a>
    </div>
  </div>
</div>

---

#### 🎓 四、 青年创新、高校巡讲与闭门对谈 (University, Media & Industry Talks)

<div class="card mb-4 shadow-sm border-left-success">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-success">高校官方特邀创新讲座</span>
      <span class="text-muted small">2025 · 北京化工大学</span>
    </div>
    <h4 class="card-title font-weight-bold">《从校园创客到技术创业者：一块碎屏引发的硬核探索》</h4>
    <h6 class="card-subtitle text-muted mb-3">北京化工大学机工系生产实习大会 & 巴黎居里工程师学院特邀主题讲座 | 主讲人：张振尧</h6>
    <p class="card-text">
      <strong>演讲背景与摘要：</strong>受母校邀请为机工系与工程师学院学弟学妹开展创新创业经验报告。张振尧以“一块摔碎的手机屏幕”为引子，坦诚分享如何从大一在宿舍里帮室友换屏、自学维修技术创立“新干线维修”服务 3000+ 订单、设立 100+ 勤工助学岗位，再到获得学校孵化基地支持创办零零后科技，研发“屋必安”物联网危房监测传感器助力脱贫攻坚防灾减灾，并最终跨入前沿具身智能赛道的真实蜕变历程。
    </p>
    <div class="bg-light p-3 rounded mb-3">
      <strong>💡 寄语青年学子：</strong>
      “动手是最好的老师。不要把年轻当成资本，而要把年轻当成试错的筹码。真正的技术创业不是站在聚光灯下讲概念，而是在宿舍台灯下、在实验室工作台前，用一行行代码和一块块电路板，去解决身边哪怕最微小的一个真实痛点。”
    </div>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-info">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-info">产业高端闭门沙龙</span>
      <span class="text-muted small">2026 · 清华科技园 Luma</span>
    </div>
    <h4 class="card-title font-weight-bold">《从玩家到开发者，我为什么要给机器狗写 SDK？》</h4>
    <h6 class="card-subtitle text-muted mb-3">清华科技园 Luma 具身智能闭门沙龙 | 对谈嘉宾：张振尧 × 维他动力赵哲伦 × 脑放电波 Nixon</h6>
    <p class="card-text">
      <strong>沙龙核心观点：</strong>与具身机器人创业一线核心创始人展开长达数小时的高浓度硬核对话。剖析当前四足机器人赛道“硬件堆料过剩但开发者体验极差”的现实矛盾；分享为什么坚持逆向通讯协议并开源易用 Python SDK；展望四足机器狗从“展示大玩具”向巡检、科研以及桌面级物理执行终端演进的破局点。
    </p>
  </div>
</div>

<div class="card mb-4 shadow-sm border-left-dark">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span class="badge badge-dark">腾讯科技产业专题研讨</span>
      <span class="text-muted small">2025.05 · 腾讯科技《具身之路》</span>
    </div>
    <h4 class="card-title font-weight-bold">《桌面机器人：下一代陪伴宠物，还是下一代智商税？》</h4>
    <h6 class="card-subtitle text-muted mb-3">腾讯科技《具身之路》系列专题直播与产业深度研讨</h6>
    <p class="card-text">
      <strong>研讨重点：</strong>
      <ul class="mb-0 mt-2 pl-3">
        <li><strong>产业兴衰镜鉴</strong>：复盘 Jibo、Vector 等早期桌面陪伴机器人商业折戟的核心原因（硬件成本高企、需求单一与高期待落差）。</li>
        <li><strong>动力与结构极限</strong>：在桌面级紧凑体积下塞入小型高精度伺服电机、微型传动机构与立体散热系统的工程取舍。</li>
        <li><strong>真伪需求之辩</strong>：在桌面终端接入端侧大模型，究竟是噱头套壳还是情感刚需？多模态音视频交互与动作流畅协同的延迟瓶颈何在。</li>
        <li><strong>商业变现模式</strong>：硬件一次性销售 vs 订阅制内容服务，如何跨越“买回家玩三天吃灰”的用户粘性挑战。</li>
      </ul>
    </p>
  </div>
</div>

---

### 📸 开发者大会现场与演讲掠影

<div class="row my-4">
  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/legacy/img/portfolio/191207-DevFEST.jpg" class="card-img-top img-fluid" alt="Google DevFest 现场">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">Google DevFest 开发者大会</h6>
        <small class="text-muted">参与 Google 开发者社区前沿技术分享与工作坊研讨</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/legacy/img/portfolio/gdg2020.jpg" class="card-img-top img-fluid" alt="2020 谷歌开发者大会">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">谷歌开发者大会 (GDG) PRE</h6>
        <small class="text-muted">开源开发工具、Web 前沿与端侧计算实践交流</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/legacy/img/portfolio/cxsqyj.jpg" class="card-img-top img-fluid" alt="创享商圈年会特邀演讲现场">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">创享商圈年会特邀演讲</h6>
        <small class="text-muted">汇报高校青年硬核科技创业、技术服务与社会价值实践</small>
      </div>
    </div>
  </div>
</div>

<div class="row my-2">
  <div class="col-md-6 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/awards/humanoid_robot_skills_champion.png" class="card-img-top img-fluid" alt="2025 国际人形机器人技能大赛（张江启动赛）人形机器人应用场景挑战赛张江记录第一名 荣誉证书">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">清华紫荆战队 · 张江启动赛纪录第一名证书</h6>
        <small class="text-muted">2025 国际人形机器人技能大赛（上海张江）荣誉证书，参赛成员含本人</small>
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/awards/nvidia_booth_showcase.jpg" class="card-img-top img-fluid" alt="英伟达展台现场案例展示">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">英伟达展台项目优秀案例展示</h6>
        <h6 class="card-subtitle text-muted mb-2 font-size-sm">NVIDIA 官方展台深度展示与官方签署授权案例</h6>
        <small class="text-muted">PCBTool AI 电路设计专家智能体入选官方展台展示案例</small>
      </div>
    </div>
  </div>
</div>

---

### 📅 公开演讲与技术布道年表 (2019–2026)

上表为本人在影像与文字档案中**逐条可核证的 18 场次**（2019—2026），并非完整全量；平台覆盖 Google、腾讯科技、智源研究院、地瓜机器人、嘉立创、火山引擎、NVIDIA 生态、清华 MBA 具身智能俱乐部与小红书科技。线下单场规模最大为嘉立创星火大会（现场 2,000+ 工程师开发者），单场报名最快满员为模力营公开课（400+ 人）。各场次人数为**独立现场数据，非累计去重**。

| 时间    | 场合                                                | 身份                          |
| ------- | --------------------------------------------------- | ----------------------------- |
| 2026-10 | 小红书科技 × 探月「具身智能 AMA」                   | 主讲                          |
| 2026-09 | 嘉立创星火大会（2000+ 工程师，深圳会展中心）        | 主讲                          |
| 2026-09 | S 创上海 2026 × 小红书 Showcase 专场                | 主讲                          |
| 2026-09 | 上海具身智能师资培训（职教师资班）                  | 主讲                          |
| 2026-08 | 探月黑客松 × HICOOL 全球创业者峰会专场              | 主持人                        |
| 2026-07 | 探月计划 Physical AI 黑客松开幕式                   | 致辞嘉宾                      |
| 2026-04 | 北京智源研究院「智源虾客行」                        | 讲师                          |
| 2026-03 | 地瓜机器人官方技术直播                              | 主讲                          |
| 2026-03 | 模力营 · 地瓜机器人（400+ 人，央视财经现场拍摄）    | 特邀嘉宾                      |
| 2026-01 | 火山引擎深圳社区 ADG 分享会（Intel 大湾区创新中心） | 讲师                          |
| 2025-12 | 探月 · 具身智能轻享 Talk（清华 MBA 具身智能俱乐部） | 主讲（线上 22,000+ 观看）     |
| 2025-11 | DDC2025 地瓜机器人开发者大会 · 小红书 AMA           | 圆桌嘉宾（获「年度星推官」）  |
| 2025-05 | 腾讯科技《具身之路》直播 · 桌面机器人专场           | 主持人                        |
| 2025-03 | 具身智能畅谈体验会（宇树 G1 + 机器狗）              | 圆桌嘉宾                      |
| 2024    | 大理 WaytoAGI 出海 Hacker House 技术分享            | 受邀开发者                    |
| 2023-03 | 中关村论坛 · 青年创新展区                           | 现场分享                      |
| 2020-11 | Google DevFest Shanghai 2020                        | 圆桌嘉宾（00 后代表性开发者） |
| 2019    | GDG Beijing / WTM 2019                              | 组织者 / 分享                 |

---

### 🎪 现场掠影与布道影像

<div class="row my-4">
  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/214-2026-robot_15014227296568480373-0.jpg" class="card-img-top img-fluid" alt="嘉立创第四届开源硬件星火会展馆现场，人群密集的蓝色展位">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">嘉立创开源硬件星火会 · 主会场演讲</h6>
        <small class="text-muted">2026.09 深圳会展中心，面向 2000+ 硬件工程师与创客，超宽屏主会场 15 分钟主题演讲。</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/282-2026-robot_14846461585053848190-0.jpg" class="card-img-top img-fluid" alt="智算启航 AI 融合实战活动海报">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">火山引擎深圳社区 ADG 分享会</h6>
        <small class="text-muted">2026.01 Intel 大湾区创新中心，主讲《用 Vibe Coding 打造机器人 Agent》。</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/142-2026-talk_15006050226552247034-0.jpg" class="card-img-top img-fluid" alt="展台前众人围观机器人演示">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">上海具身智能师资培训</h6>
        <small class="text-muted">2026.09 面向职教师资班讲授具身智能课程建设与真机实训，台下为未来的机器人专业教师。</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/018-2026-talk_14877951463515558508-0.jpg" class="card-img-top img-fluid" alt="白板前授课与听众">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">开源硬件项目实战授课</h6>
        <small class="text-muted">2026 社群公开课，白板推导 + 真机演示，讲解开源硬件从原型到可复现交付的全过程。</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/141-2026-robot_14992955533069587062-0.jpg" class="card-img-top img-fluid" alt="WRC 北京站地瓜精酿馆活动观众席坐满听众">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">世界机器人大会 · 生态专场交流</h6>
        <small class="text-muted">2026 亦庄机器人主题酒馆场，与机器人团队及产业链上下游伙伴同台交流。</small>
      </div>
    </div>
  </div>

  <div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/318-2024-talk_14359734704853553670-0.jpg" class="card-img-top img-fluid" alt="AI Hacker House 活动海报">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">黑客松方法论分享</h6>
        <small class="text-muted">2024 年起在多个 Hacker House 与开发者社区分享极限开发经验：作品 30%、演讲 30%、PPT 30%、运气 10%。</small>
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/171-2023-talk_14137199111566398198-0.jpg" class="card-img-top img-fluid" alt="中关村论坛众人参观圆形展项">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">中关村论坛 · 青年创新展区</h6>
        <small class="text-muted">2023 年受邀参与中关村论坛展区交流与现场讲解，是早期以在校创业者身份亮相的国家级科技平台。</small>
      </div>
    </div>
  </div>

  <div class="col-md-6 mb-4">
    <div class="card h-100 shadow-sm">
      <img src="/assets/img/journal/015-2025-talk_14613282929681175074-0.jpg" class="card-img-top img-fluid" alt="展台人形机器人立姿展示">
      <div class="card-body p-3">
        <h6 class="font-weight-bold mb-1">腾讯科技《具身之路》桌面机器人专场</h6>
        <small class="text-muted">2025.05 主持腾讯科技具身智能系列深度直播，围绕桌面陪伴机器人的真伪需求与商业化路径展开研讨。</small>
      </div>
    </div>
  </div>
</div>
