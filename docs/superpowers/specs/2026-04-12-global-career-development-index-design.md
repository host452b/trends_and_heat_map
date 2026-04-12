# Global Career Development Index — Design Spec

全球职业发展指数数据库设计文档。

**项目代号**: trends_and_heat_map
**参考仓库**: host452b/travel_with_family（全球景区多维评分数据库，1072条记录·34列）
**目标**: 构建全球最全面的职业多维量化评分数据库，覆盖1300+职业×45国/地区，34维评分+趋势列，支持人类浏览和AI Agent程序化消费。

---

## 1. 核心决策摘要

| 决策项 | 选定方案 |
|--------|---------|
| 数据行粒度 | 一行 = 一个职业 × 一个国家/地区 |
| 时间维度 | 2026年快照 + 趋势列（trend_2000_2026, trend_5yr, demand_direction, ai_timeline） |
| 国家覆盖 | 45国/地区，按区域代表选取 |
| 职业颗粒度 | 极致细分 ~1,300 细类（ISCO-08扩展 + 新兴职业） |
| 评价维度 | 34个维度，全部纳入加权综合分 |
| CSV分文件 | 按职业大类分（12个CSV） |
| Notebook结构 | A(1:1数据)+B(45国全景)+C(趋势专题)+排行榜+新兴职业专题 = 75个 |
| 数据方法论 | 权威数据源主导 + AI校准微调 |
| 雇主类型 | 新增 employer_type 列区分国有垄断/一般国企/民企/创业/自由职业 |
| 一个中国原则 | 中国台湾地区、中国香港地区标记为 type=region |

---

## 2. 职业分类体系（12大类）

| # | 大类 | 代码 | CSV文件名 | 覆盖范围 |
|---|------|------|----------|---------|
| 1 | 信息技术与数字化 | TECH | tech_digital.csv | 软件、硬件、AI、数据、网络安全、游戏、区块链等 |
| 2 | 医疗与健康 | MED | medical_health.csv | 临床、护理、药学、康复、公卫、中医、传统医学等 |
| 3 | 金融与商业 | FIN | finance_business.csv | 银行、证券、保险、会计、咨询、投资、房地产等 |
| 4 | 教育与学术 | EDU | education_academia.csv | K12、高等教育、培训、学术研究等 |
| 5 | 工程与制造 | ENG | engineering_manufacturing.csv | 机械、电气、化工、建筑、汽车、航空等 |
| 6 | 公共管理与公务员 | GOV | gov_public.csv | 各国公务员体系、事业编、军警消防、情报、国际组织等 |
| 7 | 法律与社会服务 | LAW | legal_social.csv | 律师、法官、社工、NGO、宗教等 |
| 8 | 文化、艺术与传媒 | ART | culture_arts_media.csv | 影视、音乐、出版、设计、动画游戏、体育、广告公关、自媒体、网红、主播等 |
| 9 | 交通运输与物流 | TRA | transport_logistics.csv | 飞行员、船员、司机、快递、航空管制、物流管理等 |
| 10 | 技术工种与手工业 | SKL | skilled_trades.csv | 电工、焊工、水管工、CNC技师、传统手工艺等 |
| 11 | 服务业与消费 | SVC | service_consumer.csv | 餐饮、零售、旅游、美容、家政、照护、平台零工、特殊合法职业等 |
| 12 | 农业、资源与环境 | AGR | agriculture_resources.csv | 农牧渔、采矿、能源、环保、林业等 |

### 2.1 完整分类树示例（TECH）

```
信息技术与数字化 (TECH)
├── 软件开发
│   ├── 前端工程师
│   ├── 后端工程师
│   ├── 全栈工程师
│   ├── 移动端工程师(iOS)
│   ├── 移动端工程师(Android)
│   ├── 嵌入式软件工程师
│   ├── 游戏开发工程师
│   ├── DevOps工程师
│   └── QA/测试工程师
├── 人工智能与数据
│   ├── 机器学习工程师
│   ├── 数据科学家
│   ├── 数据分析师
│   ├── 数据工程师
│   ├── NLP工程师
│   ├── 计算机视觉工程师
│   ├── AI研究员
│   ├── 数据标注员
│   ├── AI Trainer/RLHF标注师
│   ├── AI产品经理
│   └── Prompt Engineer
├── 网络与安全
│   ├── 网络安全工程师
│   ├── 渗透测试工程师
│   ├── 网络架构师
│   ├── 系统管理员
│   ├── 云计算工程师
│   └── 漏洞赏金猎人(Bug Bounty Hunter)
├── 产品与设计
│   ├── 产品经理
│   ├── UI设计师
│   ├── UX研究员
│   └── 交互设计师
└── 新兴数字职业
    ├── 区块链开发者
    ├── Web3工程师
    ├── 无人机软件工程师
    ├── AR/VR开发者
    └── 量化交易开发者
```

### 2.2 完整分类树示例（ART — 文化产业展开）

```
文化、艺术与传媒 (ART)
├── 影视制作
│   ├── 电影导演
│   ├── 电视剧导演
│   ├── 编剧/剧本作家
│   ├── 制片人
│   ├── 演员/表演艺术家
│   ├── 特技演员
│   ├── 选角导演
│   ├── 摄影指导
│   ├── 剪辑师
│   ├── 灯光师
│   ├── 美术指导/场景设计
│   ├── 服装造型师
│   ├── 特效师(实体)
│   ├── 视觉特效(VFX)艺术家
│   └── 综艺节目编导
├── 音乐产业
│   ├── 歌手/音乐人
│   ├── 作曲家
│   ├── 作词人
│   ├── 音乐制作人
│   ├── 录音工程师/混音师
│   ├── A&R(艺人发掘)
│   ├── 乐器演奏家
│   ├── 指挥家
│   ├── DJ
│   └── 音乐治疗师
├── 出版与写作
│   ├── 小说家/作家
│   ├── 编辑(图书)
│   ├── 编辑(期刊/杂志)
│   ├── 文学经纪人
│   ├── 翻译/译者
│   ├── 本地化经理
│   ├── 校对员
│   └── 技术文档写作
├── 舞台与表演
│   ├── 舞台剧演员
│   ├── 舞蹈家/编舞
│   ├── 脱口秀演员
│   ├── 相声/曲艺演员
│   ├── 魔术师
│   ├── 马戏/杂技演员
│   ├── 舞台监督
│   └── 舞台灯光/音响设计
├── 博物馆与文化遗产
│   ├── 策展人
│   ├── 文物修复师
│   ├── 考古学家
│   ├── 博物馆管理员
│   ├── 美术馆运营
│   ├── 非遗传承人
│   └── 文化遗产保护专家
├── 设计与创意
│   ├── 平面设计师
│   ├── 工业设计师
│   ├── 时装设计师
│   ├── 室内设计师
│   ├── 珠宝设计师
│   ├── 文创产品设计师
│   ├── 国潮/文化IP设计师
│   └── 品牌设计师
├── 动画与游戏
│   ├── 动画师(2D)
│   ├── 动画师(3D)
│   ├── 分镜/故事板艺术家
│   ├── 游戏策划
│   ├── 游戏美术
│   ├── 关卡设计师
│   └── 游戏音效设计
├── 广告与公关
│   ├── 文案/Copywriter
│   ├── 创意总监
│   ├── 美术总监(广告)
│   ├── 公关专员
│   ├── 危机公关
│   ├── 品牌经理
│   └── 活动策划/执行
├── 新闻与传媒
│   ├── 记者(文字)
│   ├── 记者(视频)
│   ├── 主持人/主播(新闻)
│   ├── 摄影记者
│   └── 新闻编辑
├── 新媒体与内容
│   ├── YouTuber/视频创作者
│   ├── 短视频创作者
│   ├── 播客主播
│   ├── Newsletter/Substack写手
│   ├── 公众号/博客作者
│   ├── VTuber/虚拟主播
│   ├── 直播带货主播
│   ├── 才艺直播主播
│   ├── 游戏直播主播
│   ├── KOL/网红
│   ├── MCN运营
│   ├── 短视频导演
│   └── 内容审核员
├── 体育与竞技
│   ├── 足球运动员
│   ├── 篮球运动员
│   ├── 网球运动员
│   ├── 游泳运动员
│   ├── 田径运动员
│   ├── 格斗运动员
│   ├── 高尔夫球手
│   ├── 赛车手
│   ├── 电竞选手
│   ├── 教练
│   ├── 裁判员
│   ├── 体育经纪人
│   └── 体育解说员
├── 会展与策展
│   ├── 会展设计师
│   ├── 会议组织者
│   ├── 展览运营
│   └── 拍卖师
├── 图书馆与信息
│   ├── 图书馆员
│   ├── 档案管理员
│   └── 信息科学家
└── 文化产业管理
    ├── IP运营/授权
    ├── 文化产业投资
    ├── 经纪人(艺人)
    ├── 经纪人(体育)
    └── 版权管理/律师
```

### 2.3 完整分类树示例（GOV — 公共管理展开）

```
公共管理与公务员 (GOV)
├── 中央/联邦公务员
│   ├── 行政管理官员
│   ├── 政策分析师
│   ├── 税务官员
│   ├── 海关关员
│   ├── 外交官
│   ├── 审计官员
│   ├── 监察/反腐官员
│   ├── 统计官员
│   ├── 气象官员
│   └── 国会/议会工作人员
├── 地方公务员
│   ├── 地方行政官员
│   ├── 城市规划师(政府)
│   ├── 社区干部/基层治理
│   └── 城管执法人员
├── 司法行政
│   ├── 法院书记员
│   ├── 法警
│   └── 司法行政人员
├── 事业单位/公共机构（中国及类似体系）
│   ├── 公立学校教师(事业编)
│   ├── 公立医院医生(事业编)
│   ├── 科研院所研究员
│   └── 公共图书馆/博物馆(事业编)
├── 国际组织
│   ├── 联合国职员
│   ├── WHO/世卫职员
│   ├── 世界银行/IMF职员
│   └── 其他国际组织(OECD/WTO/ILO等)
├── 军事
│   ├── 陆军军官/士兵
│   ├── 海军军官/士兵
│   ├── 空军军官/士兵
│   ├── 特种部队
│   └── 军事工程师/技术军官
├── 警察与执法
│   ├── 警察(正式编制)
│   ├── 辅警/协警
│   ├── 刑事侦查员
│   ├── 交通警察
│   ├── 网络警察
│   └── 私人侦探(民间)
├── 消防与应急
│   ├── 消防员
│   ├── 急救医护(EMT/Paramedic)
│   ├── 灾害应急管理员
│   └── 海岸警卫队
├── 情报与安全
│   ├── 情报分析员
│   ├── 安全官员
│   └── 安保人员(民间)
└── 国有垄断企业（通过employer_type=state_monopoly区分）
    ├── 电力/电网(如国家电网)
    ├── 烟草(如中国烟草)
    ├── 石油天然气(如中石油/Saudi Aramco/Gazprom)
    ├── 铁路(如中国铁路/JR/SNCF)
    ├── 电信(如三大运营商/NTT)
    └── 国有银行
```

> 注：其余9个大类（MED/FIN/EDU/ENG/LAW/TRA/SKL/SVC/AGR）的完整分类树将在实施阶段逐一展开，结构与上述示例一致：大类→中类→细类。

---

## 3. 国家/地区清单（45个）

坚持一个中国原则：中国台湾地区、中国香港地区标记为 `type=region`。

| 区域 | 国家/地区 | ISO码 | 数量 |
|------|----------|-------|------|
| 东亚 | 中国 | CN | |
| | 日本 | JP | |
| | 韩国 | KR | |
| | 中国台湾地区 | TW (type=region) | |
| | 中国香港地区 | HK (type=region) | |
| | | | 3国+2地区 |
| 东南亚 | 新加坡 | SG | |
| | 泰国 | TH | |
| | 越南 | VN | |
| | 印度尼西亚 | ID | |
| | 马来西亚 | MY | |
| | 菲律宾 | PH | |
| | | | 6 |
| 南亚 | 印度 | IN | |
| | 巴基斯坦 | PK | |
| | 孟加拉国 | BD | |
| | | | 3 |
| 中亚/西亚 | 阿联酋 | AE | |
| | 以色列 | IL | |
| | 沙特阿拉伯 | SA | |
| | 土耳其 | TR | |
| | | | 4 |
| 西欧 | 英国 | GB | |
| | 法国 | FR | |
| | 德国 | DE | |
| | 荷兰 | NL | |
| | 瑞士 | CH | |
| | | | 5 |
| 北欧 | 瑞典 | SE | |
| | 丹麦 | DK | |
| | 芬兰 | FI | |
| | | | 3 |
| 南欧 | 意大利 | IT | |
| | 西班牙 | ES | |
| | 葡萄牙 | PT | |
| | | | 3 |
| 东欧 | 波兰 | PL | |
| | 捷克 | CZ | |
| | 俄罗斯 | RU | |
| | | | 3 |
| 北美 | 美国 | US | |
| | 加拿大 | CA | |
| | 墨西哥 | MX | |
| | | | 3 |
| 南美 | 巴西 | BR | |
| | 阿根廷 | AR | |
| | 智利 | CL | |
| | 哥伦比亚 | CO | |
| | | | 4 |
| 大洋洲 | 澳大利亚 | AU | |
| | 新西兰 | NZ | |
| | | | 2 |
| 非洲 | 南非 | ZA | |
| | 尼日利亚 | NG | |
| | 肯尼亚 | KE | |
| | 埃及 | EG | |
| | | | 4 |
| **合计** | | | **43国 + 2地区 = 45** |

选国逻辑：G20全覆盖、每区域至少2-3代表、含不同发展阶段、含劳动力市场特色国。

---

## 4. 评价维度体系（34维度·全部加权）

所有维度统一 **0-10分制**。

### 4.1 入门门槛（6%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 前置学习成本 | learning_cost | 无需培训即可上岗 | 10年+专业训练 | 3% | O*NET Education/Training, 各国职业资格框架 |
| 学历要求 | education_req | 无学历要求 | 博士/博士后必需 | 3% | O*NET, ILO ISCED映射, 各国教育部 |

### 4.2 发展空间（10%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 职业成长系数 | growth_coeff | 无晋升空间 | 天花板极高/指数成长 | 4% | LinkedIn Career Path, Glassdoor Career Trajectories |
| 职业寿命 | career_lifespan | <5年即淘汰 | 可干到退休且越老越值钱 | 3% | ILO年龄段就业统计, OECD Aging & Employment |
| 职业机遇 | opportunity | 夕阳行业无机会 | 风口爆发/红利期 | 3% | WEF Future of Jobs, McKinsey MGI, CB Insights |

### 4.3 市场面（10%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 职业市场大小 | market_size | 极小众(<万人) | 全球数千万从业者 | 2% | ILO ILOSTAT就业统计, 各国劳动统计局 |
| 供需关系 | supply_demand | 严重过剩 | 严重供不应求 | 4% | Indeed/LinkedIn人才洞察, OECD Skills for Jobs |
| 发达国家稀缺度 | developed_scarcity | 完全不缺 | 极度紧缺/移民快通道 | 4% | OECD Shortage Lists, 各国移民局紧缺职业清单 |

### 4.4 收入与回报（9%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 职业附加值水平 | value_added | 最低工资/无隐性收入 | 顶薪+股权+社会资源丰厚 | 5% | ILO Global Wage Report, Glassdoor/PayScale, 各国统计局 |
| 性价比 | cost_performance | 高投入低回报 | 低投入高回报 | 4% | 综合计算：附加值/(学习成本+学历要求+入行年限) |

### 4.5 稳定与风险（15%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 职业稳定性 | stability | 极不稳定/随时裁员 | 铁饭碗/终身雇佣 | 4% | OECD Employment Protection, ILO就业形态统计 |
| 安全危险系数 | safety | 致命高危 | 零风险 | 3% | ILO Safety & Health, OSHA/EU-OSHA工伤统计 |
| 职业病系数 | occupational_disease | 高发职业病 | 几乎无职业病 | 2% | WHO Occupational Health, 各国职业病报告 |
| 加班程度 | overtime | 极端996/007 | 严格准时下班 | 3% | OECD Hours Worked, ILO Working Time, Glassdoor |
| 职业倦怠水平 | burnout | 极度倦怠/高离职率 | 身心愉悦/高留存 | 3% | Gallup State of Global Workplace, WHO Burnout研究 |

### 4.6 口碑与转型（9%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 技能通用性 | skill_versatility | 极度专精/不可迁移 | 万能技能/处处通用 | 3% | O*NET Skills Transferability, LinkedIn Skills Genome |
| 转行容易度 | career_switch | 几乎无法转行 | 随时可切换赛道 | 3% | LinkedIn Career Transitions, 各行业调研 |
| 口碑方差 | reputation_variance | 两极严重分化 | 评价高度一致 | 3% | Glassdoor/知乎/Reddit/Quora舆情AI汇总 |

> **注意**：口碑方差为反向指标。原始数据范围0-5（0=稳定，5=分化），在加权计算前需归一化为0-10分且反转方向（10=稳定可信=好，0=两极分化=差），以便与其他"越高越好"的维度统一参与加权。Notebook中该列仍显示原始0-5值并反色（绿=稳定，红=分化）。

### 4.7 未来（6%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| AI替代风险 | ai_resistance | 即将完全替代 | AI完全无法替代 | 6% | Oxford Frey-Osborne, WEF Future of Jobs 2025, McKinsey MGI |

### 4.8 生活质量（15%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 社会地位/尊重度 | social_status | 社会底层/受歧视 | 极高社会地位/受人尊敬 | 3% | 各国职业声望调查(SIOPS/ISEI), Gallup |
| 远程工作友好度 | remote_friendly | 必须现场 | 100%远程/数字游民 | 3% | McKinsey Remote Work Survey, FlexJobs |
| 自由度/自主性 | autonomy | 完全受控/流水线 | 完全自主决策 | 3% | O*NET Work Context: Autonomy, Gallup |
| 家庭友好度 | family_friendly | 极不兼容家庭 | 完美兼顾 | 3% | OECD Better Life Index, UNICEF Family-Friendly |
| 成就感/意义感 | fulfillment | 无意义感 | 极高使命感/社会贡献 | 3% | Gallup Employee Engagement, 各国职业满意度调查 |

### 4.9 结构性与灵活性（20%）

| 维度 | 字段名 | 0分 | 10分 | 权重 | 主要数据源 |
|------|--------|-----|------|------|-----------|
| 创业转化率 | entrepreneurship | 几乎无人创业 | 大量成功创业案例 | 2% | GEM全球创业观察, Crunchbase |
| 性别平等度 | gender_equality | 极端性别失衡 | 完全均衡 | 2% | ILO Gender Statistics, WEF Gender Gap |
| 入行年龄弹性 | age_flexibility | 只收应届/年轻人 | 任何年龄都能入行 | 2% | OECD Aging Worker, 行业调研 |
| 社交属性 | social_interaction | 完全独立工作 | 高强度人际互动 | 2% | O*NET Work Context: Social |
| 体力要求 | physical_demand | 纯脑力 | 重体力劳动 | 1% | O*NET Physical Demands |
| 政策/执照壁垒 | license_barrier | 无门槛 | 需国家级执照/严格准入 | 2% | 各国职业准入法规 |
| 周期敏感度 | cycle_sensitivity | 完全抗周期 | 随经济剧烈波动 | 2% | 各国GDP-就业弹性统计 |
| 副业兼容性 | side_job_compat | 合同/法规禁止 | 自由兼职/斜杠友好 | 2% | 各国劳动法+行业惯例 |
| 国际流动性 | intl_mobility | 资质不互认/无法跨国 | 全球通用/随时外派 | 3% | 各国职业资质互认协议 |
| 行业垄断度 | industry_monopoly | 完全自由竞争 | 头部垄断/个体无空间 | 2% | 各行业集中度(HHI), 反垄断报告 |

### 4.10 权重汇总

| 类别 | 维度数 | 小计 |
|------|--------|------|
| 入门门槛 | 2 | 6% |
| 发展空间 | 3 | 10% |
| 市场面 | 3 | 10% |
| 收入与回报 | 2 | 9% |
| 稳定与风险 | 5 | 15% |
| 口碑与转型 | 3 | 9% |
| 未来 | 1 | 6% |
| 生活质量 | 5 | 15% |
| 结构性与灵活性 | 10 | 20% |
| **总计** | **34** | **100%** |

**综合加权发展指数** = Σ(各维度分数 × 权重) ，范围0-10。

### 4.11 评分方向说明

所有维度在综合加权计算中统一为"**越高越好**"方向。部分维度的原始含义需要反向理解：

| 维度 | 原始语义 | 评分方向（用于加权） | 说明 |
|------|---------|-------------------|------|
| 前置学习成本 | 成本高=门槛高 | 10=低成本易入门=好 | 对求职者而言低门槛更友好 |
| 学历要求 | 要求高=门槛高 | 10=低学历可入=好 | 同上 |
| 口碑方差 | 方差大=分化严重 | 10=稳定一致=好 | 原始0-5范围需归一化并反转 |
| 体力要求 | 体力消耗大 | 10=纯脑力轻松=好 | 体力劳动不利于职业寿命 |
| 政策/执照壁垒 | 壁垒高=准入难 | 10=无壁垒自由进入=好 | 对求职者而言低壁垒更友好 |
| 周期敏感度 | 敏感=波动大 | 10=完全抗周期=好 | 稳定优于波动 |
| 行业垄断度 | 垄断高=个体空间小 | 10=自由竞争=好 | 开放市场对个体更友好 |

其余27个维度天然为"越高越好"方向（如成长系数高=好、稳定性高=好、远程友好高=好）。

### 4.12 口碑方差解读（对标参考仓库）

- **0-1.5 (绿)** = 评价稳定，该职业在该国的体验可预期
- **1.5-2.5 (黄)** = 多数认可，少数不同看法
- **2.5-5 (红)** = 两极分化，体验取决于具体雇主/城市/个人

---

## 5. CSV完整列定义（57列）

### 5.1 基础信息列（15列）

| # | 列名 | 字段名 | 类型 | 示例 |
|---|------|--------|------|------|
| 1 | ID | id | string | TECH-0101-CN-general |
| 2 | 大类 | major_category | string | 信息技术与数字化 |
| 3 | 大类代码 | major_code | string | TECH |
| 4 | 中类 | mid_category | string | 软件开发 |
| 5 | 细类 | sub_category | string | 前端工程师 |
| 6 | 细类(英) | sub_category_en | string | Front-end Engineer |
| 7 | ISCO编码 | isco_code | string | 2514 |
| 8 | O*NET编码 | onet_code | string | 15-1254.00 |
| 9 | 区域 | region | string | 东亚 |
| 10 | 国家/地区 | country_or_region | string | 中国 |
| 11 | ISO码 | iso_code | string | CN |
| 12 | 类型 | type | string | country / region |
| 13 | 雇主类型 | employer_type | string | general / state_monopoly / ... |
| 14 | 典型学历 | typical_education | string | 本科/硕士 |
| 15 | 典型入行年龄 | typical_entry_age | string | 22-26岁 |

### 5.2 地区特有标签（1列）

| # | 列名 | 字段名 | 类型 | 说明 |
|---|------|--------|------|------|
| 16 | 地区性 | locality | string | global / regional / country_specific |

### 5.3 34个评分列（#17-#50，float 0-10）

按第4节顺序排列：learning_cost → education_req → growth_coeff → career_lifespan → opportunity → market_size → supply_demand → developed_scarcity → value_added → cost_performance → stability → safety → occupational_disease → overtime → burnout → skill_versatility → career_switch → reputation_variance → ai_resistance → social_status → remote_friendly → autonomy → family_friendly → fulfillment → entrepreneurship → gender_equality → age_flexibility → social_interaction → physical_demand → license_barrier → cycle_sensitivity → side_job_compat → intl_mobility → industry_monopoly

### 5.4 趋势与汇总列（8列，#51-#58）

| # | 列名 | 字段名 | 类型 | 说明 |
|---|------|--------|------|------|
| 51 | 2000-2026趋势 | trend_2000_2026 | int(-5~+5) | 整体发展趋势 |
| 52 | 近5年趋势 | trend_5yr | int(-5~+5) | 近5年方向 |
| 53 | 需求方向 | demand_direction | string | ↑↑ / ↑ / → / ↓ / ↓↓ |
| 54 | AI影响时间线 | ai_timeline | string | 如"2028-2032"、"不受影响" |
| 55 | 综合加权发展指数 | composite_index | float | 0-10加权计算 |
| 56 | 中文摘要 | summary_zh | string | 一句话 |
| 57 | 英文摘要 | summary_en | string | 一句话 |
| 58 | 数据来源 | data_source | string | 来源标注 |

**共58列。**

### 5.5 ID编码规则

格式：`{大类代码}-{中类序号}{细类序号}-{ISO码}-{雇主类型}`

示例：
- `TECH-0101-CN-general` = 信息技术·软件开发·前端工程师·中国·通用
- `ENG-0201-CN-state_monopoly` = 工程·电气·电气工程师·中国·国有垄断(国家电网)
- `MED-0301-US-general` = 医疗·药学·药剂师·美国·通用
- `GOV-0101-JP-state_owned` = 公共管理·中央公务员·行政官员·日本·国有

employer_type为general时可省略：`TECH-0101-CN` 等同于 `TECH-0101-CN-general`

---

## 6. Notebook架构（75个）

所有notebook统一视觉语言：
- 评分列：红-绿色阶（0红→5黄→10绿）
- 口碑方差列：反色（0绿=稳定→5红=分化）
- 趋势列：红-绿色阶（-5红→0白→+5绿）

### 6.1 第一层：数据总览（1个）

| # | 文件名 | 内容 |
|---|--------|------|
| 00 | 00_数据总览.ipynb | 项目说明 · 1300+职业分类树 · 34维度定义 · 权重体系 · 数据来源 · 方法论 |

### 6.2 第二层：1:1完整数据表（12个）

| # | 文件名 | 大类 |
|---|--------|------|
| 01 | 01_tech_digital.ipynb | TECH |
| 02 | 02_medical_health.ipynb | MED |
| 03 | 03_finance_business.ipynb | FIN |
| 04 | 04_education_academia.ipynb | EDU |
| 05 | 05_engineering_manufacturing.ipynb | ENG |
| 06 | 06_gov_public.ipynb | GOV |
| 07 | 07_legal_social.ipynb | LAW |
| 08 | 08_culture_arts_media.ipynb | ART |
| 09 | 09_transport_logistics.ipynb | TRA |
| 10 | 10_skilled_trades.ipynb | SKL |
| 11 | 11_service_consumer.ipynb | SVC |
| 12 | 12_agriculture_resources.ipynb | AGR |

### 6.3 第三层：排行榜汇总（5个）

| # | 文件名 | 内容 |
|---|--------|------|
| 13 | 13_综合发展指数Top100.ipynb | 全球综合排行 · 各大类Top10 · 各区域Top10 |
| 14 | 14_AI抗性排行.ipynb | AI最难替代Top50 · 最易替代Top50 · AI时间线分布 |
| 15 | 15_性价比排行.ipynb | 投入产出比最高 · 各学历段最佳 · 各国最佳 |
| 16 | 16_稀缺度与移民价值.ipynb | 发达国家最紧缺 · 国际流动性最高 · 移民快通道 |
| 17 | 17_生活质量排行.ipynb | 远程友好 · 家庭友好 · 低倦怠 · 高自由 · 高成就感 |

### 6.4 第四层：趋势专题（4个）

| # | 文件名 | 内容 |
|---|--------|------|
| 18 | 18_2000-2026赢家与输家.ipynb | trend排序 · 崛起最快vs衰落最快 · 行业迁移图 |
| 19 | 19_AI冲击波分析.ipynb | AI替代时间线 · 各大类受冲击比例 · 各国AI就业风险热力图 |
| 20 | 20_各国职业结构演变.ipynb | 产业结构变迁 · 一二三产占比趋势 · 新兴职业崛起速度 |
| 21 | 21_供需失衡预警.ipynb | 全球最过剩vs最短缺 · 各国用工荒地图 · 未来5年供需预测 |

### 6.5 第五层：国家全景（45个）

命名：`{序号}_{ISO码}_{中文名}职业全景.ipynb`

| # | 文件名 |
|---|--------|
| 22 | 22_CN_中国职业全景.ipynb |
| 23 | 23_US_美国职业全景.ipynb |
| 24 | 24_JP_日本职业全景.ipynb |
| 25 | 25_KR_韩国职业全景.ipynb |
| 26 | 26_TW_中国台湾地区职业全景.ipynb |
| 27 | 27_HK_中国香港地区职业全景.ipynb |
| 28 | 28_SG_新加坡职业全景.ipynb |
| 29 | 29_TH_泰国职业全景.ipynb |
| 30 | 30_VN_越南职业全景.ipynb |
| 31 | 31_ID_印度尼西亚职业全景.ipynb |
| 32 | 32_MY_马来西亚职业全景.ipynb |
| 33 | 33_PH_菲律宾职业全景.ipynb |
| 34 | 34_IN_印度职业全景.ipynb |
| 35 | 35_PK_巴基斯坦职业全景.ipynb |
| 36 | 36_BD_孟加拉国职业全景.ipynb |
| 37 | 37_AE_阿联酋职业全景.ipynb |
| 38 | 38_IL_以色列职业全景.ipynb |
| 39 | 39_SA_沙特阿拉伯职业全景.ipynb |
| 40 | 40_TR_土耳其职业全景.ipynb |
| 41 | 41_GB_英国职业全景.ipynb |
| 42 | 42_FR_法国职业全景.ipynb |
| 43 | 43_DE_德国职业全景.ipynb |
| 44 | 44_NL_荷兰职业全景.ipynb |
| 45 | 45_CH_瑞士职业全景.ipynb |
| 46 | 46_SE_瑞典职业全景.ipynb |
| 47 | 47_DK_丹麦职业全景.ipynb |
| 48 | 48_FI_芬兰职业全景.ipynb |
| 49 | 49_IT_意大利职业全景.ipynb |
| 50 | 50_ES_西班牙职业全景.ipynb |
| 51 | 51_PT_葡萄牙职业全景.ipynb |
| 52 | 52_PL_波兰职业全景.ipynb |
| 53 | 53_CZ_捷克职业全景.ipynb |
| 54 | 54_RU_俄罗斯职业全景.ipynb |
| 55 | 55_CA_加拿大职业全景.ipynb |
| 56 | 56_MX_墨西哥职业全景.ipynb |
| 57 | 57_BR_巴西职业全景.ipynb |
| 58 | 58_AR_阿根廷职业全景.ipynb |
| 59 | 59_CL_智利职业全景.ipynb |
| 60 | 60_CO_哥伦比亚职业全景.ipynb |
| 61 | 61_AU_澳大利亚职业全景.ipynb |
| 62 | 62_NZ_新西兰职业全景.ipynb |
| 63 | 63_ZA_南非职业全景.ipynb |
| 64 | 64_NG_尼日利亚职业全景.ipynb |
| 65 | 65_KE_肯尼亚职业全景.ipynb |
| 66 | 66_EG_埃及职业全景.ipynb |

### 6.6 第六层：新兴职业形态专题（7个）

| # | 文件名 | 内容 |
|---|--------|------|
| 67 | 67_自媒体与内容创作者生态.ipynb | YouTuber·博客·播客·Newsletter·各平台各国对比 |
| 68 | 68_一人公司与自由职业.ipynb | 独立开发者·自由咨询·Indie Hacker·各国政策 |
| 69 | 69_网红与影响力经济.ipynb | KOL·带货·各平台生态·各国网红经济规模 |
| 70 | 70_直播产业全景.ipynb | 游戏直播·带货·教育·虚拟主播·头部vs长尾 |
| 71 | 71_运动员与体育产业.ipynb | 各运动项目·电竞·教练·经纪·职业寿命对比 |
| 72 | 72_平台零工与新型雇佣.ipynb | 网约车·外卖·Fiverr·各国零工经济·劳动保障 |
| 73 | 73_文化产业生态.ipynb | 影视·音乐·出版·文创·各国文化GDP·产业链对比 |

### 6.7 第七层：查询工具（1个）

| # | 文件名 | 内容 |
|---|--------|------|
| 74 | 74_query_tool.ipynb | 交互式查询函数库 |

核心函数：
```python
find_jobs(country="CN", ai_resistance=">7", remote_friendly=">8")
compare("前端工程师", ["CN", "US", "DE", "JP"])
top_n(category="TECH", metric="cost_performance", n=20)
country_overview("CN", sort_by="composite_index")
transition_path("会计师", target_field="TECH")
trend_leaders(metric="trend_2000_2026", direction="up", n=30)
employer_compare("电气工程师", "CN", ["state_monopoly", "private_large"])
```

### 6.8 汇总

| 层级 | 数量 |
|------|------|
| 数据总览 | 1 |
| 1:1完整数据 | 12 |
| 排行榜汇总 | 5 |
| 趋势专题 | 4 |
| 国家全景 | 45 |
| 新兴职业专题 | 7 |
| 查询工具 | 1 |
| **总计** | **75** |

---

## 7. 数据方法论

### 7.1 方法：权威数据源主导 + AI校准微调

| 层级 | 数据来源 | 覆盖 |
|------|---------|------|
| 第一层（锚点） | 权威机构硬数据 | 有数据的维度×国家组合 |
| 第二层（补全） | Claude + GPT交叉评估取均值 | 无硬数据的组合 |
| 第三层（校准） | 用第一层锚点约束第二层AI评分的合理范围 | 全部 |

### 7.2 权威数据源清单

| 来源 | 覆盖维度 |
|------|---------|
| ILO ILOSTAT | 就业统计、工时、安全、性别、工资 |
| OECD Employment Outlook | 就业保护、技能供需、工时、老龄化 |
| O*NET (美国) | 教育要求、技能迁移性、工作环境、体力需求 |
| WEF Future of Jobs Report | AI替代、新兴技能、行业趋势 |
| McKinsey Global Institute | 自动化潜力、远程工作、生产率 |
| Oxford/Frey & Osborne | AI替代概率（702个职业） |
| Glassdoor / Indeed | 口碑、薪资、满意度、倦怠 |
| LinkedIn Economic Graph | 职业路径、技能基因组、人才流动 |
| GEM全球创业观察 | 创业转化率 |
| WEF Gender Gap Report | 性别平等 |
| Gallup World Poll | 工作满意度、倦怠、社会地位 |
| PayScale / Numbeo | 薪资购买力校准 |
| 各国劳动统计局 | 国别细分数据 |
| 各国移民局紧缺职业清单 | 发达国家稀缺度 |

### 7.3 数据来源标注

每行 `data_source` 列标注：
- 纯权威数据：`ILO+OECD+O*NET 综合`
- AI校准：`AI综合评估 + ILO/OECD锚点校准`
- 纯AI（无对应硬数据）：`Claude+GPT加权平均（无锚点）`

---

## 8. 机器可读性层

### 8.1 SCHEMA.yaml

定义每列的类型、取值范围、权重、单位、含义（中英双语）。AI agent读此文件即可理解整个数据集。

### 8.2 跨分类映射

| 文件 | 内容 |
|------|------|
| mapping_isco.csv | 本项目ID ↔ ISCO-08 |
| mapping_onet.csv | 本项目ID ↔ O*NET SOC |
| mapping_isced.csv | 学历字段 ↔ ISCED等级 |
| country_meta.csv | ISO码·区域·发展阶段·GDP·人口·劳动力规模 |

### 8.3 JSON镜像

`data/json/` 下为每个CSV生成JSON版本，含 `meta` 对象和 `records` 数组。`data/json/meta/` 下存 schema.json、categories.json、countries.json、weights.json。

### 8.4 双语README

README.md（中文）+ README_EN.md（英文），降低国际AI agent使用门槛。

### 8.5 CHANGELOG.md

结构化变更日志，记录每次数据更新。

---

## 9. 项目完整文件结构

```
trends_and_heat_map/
├── README.md
├── README_EN.md
├── FLOW.md
├── CHANGELOG.md
├── schema/
│   ├── SCHEMA.yaml
│   ├── categories.yaml
│   └── weights.yaml
├── mapping/
│   ├── mapping_isco.csv
│   ├── mapping_onet.csv
│   ├── mapping_isced.csv
│   └── country_meta.csv
├── data/
│   ├── csv/                          (12个CSV)
│   └── json/                         (12个JSON + meta/)
├── notebooks/                        (75个notebook)
└── archive/
```

---

## 10. 终极汇总

| 指标 | 数值 |
|------|------|
| 职业大类 | 12 |
| 职业细类 | ~1,300 |
| 国家/地区 | 45 (43国+2地区) |
| 评分维度 | 34（全部加权，合计100%） |
| CSV列数 | 58 |
| 预估总行数 | ~43,000-45,000 |
| CSV文件 | 12 |
| Notebook | 75 |
| 映射文件 | 4 |
| Schema文件 | 3 |
| 数据方法论 | 权威数据源主导 + AI校准微调 |
