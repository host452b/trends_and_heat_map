"""Generate 50-year career prediction data (2026-2076) for 4 macro regions.

Produces data/csv/predictions_50yr.csv with 288 rows:
  4 regions x 12 major_categories x 6 decades.

Prediction model blends:
  1. Current composite_index as 2026 baseline
  2. AI impact decay based on ai_timeline distribution
  3. Trend extrapolation with dampening
  4. Structural shifts per region x category
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "csv" / "00_all_occupations.csv"
OUT_PATH = BASE_DIR / "data" / "csv" / "predictions_50yr.csv"

# ── time points ──────────────────────────────────────────────────────
DECADES = [2026, 2035, 2045, 2055, 2065, 2076]

# ── region definitions ───────────────────────────────────────────────
REGION_DEFS = {
    "CN": {
        "label_zh": "中国",
        "label_en": "China",
        "filter": lambda df: df[df["iso_code"] == "CN"],
    },
    "ASIA": {
        "label_zh": "亚洲",
        "label_en": "Asia (East+SE+South+Central-West)",
        "filter": lambda df: df[df["region"].isin(
            ["东亚", "东南亚", "南亚", "中亚/西亚"]
        )],
    },
    "EUR": {
        "label_zh": "欧洲",
        "label_en": "Europe (West+North+South+East)",
        "filter": lambda df: df[df["region"].isin(
            ["西欧", "北欧", "南欧", "东欧"]
        )],
    },
    "AFR": {
        "label_zh": "非洲",
        "label_en": "Africa (ZA+NG+KE+EG)",
        "filter": lambda df: df[df["iso_code"].isin(["ZA", "NG", "KE", "EG"])],
    },
}

CATEGORY_ORDER = [
    "TECH", "MED", "FIN", "EDU", "ENG", "GOV",
    "LAW", "ART", "TRA", "SKL", "SVC", "AGR",
]

CATEGORY_ZH = {
    "TECH": "信息技术与数字化", "MED": "医疗与健康", "FIN": "金融与商业",
    "EDU": "教育与学术", "ENG": "工程与制造", "GOV": "公共管理与公务员",
    "LAW": "法律与社会服务", "ART": "文化、艺术与传媒", "TRA": "交通运输与物流",
    "SKL": "技术工种与手工业", "SVC": "服务业与消费", "AGR": "农业、资源与环境",
}

# ── AI timeline mapping → midpoint year ──────────────────────────────
def _parse_ai_timeline(val):
    """Map ai_timeline string to a numeric midpoint year."""
    mapping = {
        "2025-2028": 2026.5,
        "2026-2030": 2028.0,
        "2028-2033": 2030.5,
        "2032-2038": 2035.0,
        "2035+": 2042.0,      # "beyond 2035" → assume ~2042
    }
    return mapping.get(str(val).strip(), 2050.0)  # default: far future


def _ai_impact_factor(ai_midpoint, ai_resistance, decade):
    """Calculate AI impact multiplier for a given decade.

    Returns a factor 0.0-1.0 that reduces recommendation_index.
    0.0 = no impact, 1.0 = maximum negative impact.
    """
    if decade <= 2026:
        return 0.0

    years_since_impact = decade - ai_midpoint
    if years_since_impact < 0:
        # AI hasn't impacted this category yet at this decade
        return 0.0

    # Base decay: steep in first decade after impact, then flattens
    # Higher ai_resistance → less impact
    vulnerability = max(0, (7.0 - ai_resistance) / 7.0)  # 0=immune, 1=fully vulnerable
    time_decay = min(1.0, years_since_impact / 15.0)  # saturates after 15 years

    return vulnerability * time_decay * 0.35  # max 35% reduction


def _trend_factor(trend_2000_2026, decade):
    """Extrapolate historical trend with dampening over time.

    Returns additive adjustment to recommendation_index.
    """
    if decade <= 2026:
        return 0.0

    years = decade - 2026
    # Trend continues but with exponential dampening
    # A trend of +3 over 26 years → ~+0.115/year
    annual_rate = trend_2000_2026 / 26.0
    # Dampening: halves every 20 years
    effective_years = 20.0 * (1.0 - np.exp(-years / 20.0))
    return annual_rate * effective_years * 0.5  # halved to avoid runaway


# ── Structural shift matrices ────────────────────────────────────────
# Per region × category × decade: additive adjustments
# Positive = structural tailwind, negative = headwind
# Values represent decade-specific cumulative adjustment from 2026

_STRUCT = {
    "CN": {
        # China: manufacturing→services→AI/biotech, aging boosts healthcare
        "TECH": {2026: 0, 2035: 0.8, 2045: 1.0, 2055: 0.6, 2065: 0.3, 2076: 0.1},
        "MED":  {2026: 0, 2035: 0.6, 2045: 1.2, 2055: 1.8, 2065: 2.2, 2076: 2.5},
        "FIN":  {2026: 0, 2035:-0.4, 2045:-0.8, 2055:-0.6, 2065:-0.4, 2076:-0.3},
        "EDU":  {2026: 0, 2035: 0.3, 2045: 0.5, 2055: 0.4, 2065: 0.3, 2076: 0.2},
        "ENG":  {2026: 0, 2035: 0.4, 2045: 0.3, 2055:-0.2, 2065:-0.5, 2076:-0.7},
        "GOV":  {2026: 0, 2035:-0.2, 2045:-0.5, 2055:-0.8, 2065:-1.0, 2076:-1.2},
        "LAW":  {2026: 0, 2035:-0.1, 2045:-0.3, 2055:-0.2, 2065: 0.0, 2076: 0.1},
        "ART":  {2026: 0, 2035: 0.3, 2045: 0.4, 2055: 0.2, 2065: 0.0, 2076:-0.1},
        "TRA":  {2026: 0, 2035:-0.5, 2045:-1.2, 2055:-1.5, 2065:-1.6, 2076:-1.5},
        "SKL":  {2026: 0, 2035: 0.5, 2045: 0.8, 2055: 1.0, 2065: 0.8, 2076: 0.6},
        "SVC":  {2026: 0, 2035: 0.4, 2045: 0.8, 2055: 1.2, 2065: 1.5, 2076: 1.7},
        "AGR":  {2026: 0, 2035: 0.1, 2045: 0.2, 2055: 0.1, 2065:-0.1, 2076:-0.2},
    },
    "ASIA": {
        # Asia: manufacturing hub continues, digital economy explodes, young population
        "TECH": {2026: 0, 2035: 1.0, 2045: 1.3, 2055: 1.0, 2065: 0.6, 2076: 0.3},
        "MED":  {2026: 0, 2035: 0.4, 2045: 0.8, 2055: 1.2, 2065: 1.6, 2076: 1.8},
        "FIN":  {2026: 0, 2035: 0.2, 2045:-0.2, 2055:-0.5, 2065:-0.4, 2076:-0.3},
        "EDU":  {2026: 0, 2035: 0.5, 2045: 0.8, 2055: 0.7, 2065: 0.5, 2076: 0.4},
        "ENG":  {2026: 0, 2035: 0.6, 2045: 0.5, 2055: 0.2, 2065:-0.2, 2076:-0.4},
        "GOV":  {2026: 0, 2035: 0.0, 2045:-0.3, 2055:-0.5, 2065:-0.7, 2076:-0.8},
        "LAW":  {2026: 0, 2035: 0.1, 2045: 0.0, 2055:-0.1, 2065: 0.0, 2076: 0.1},
        "ART":  {2026: 0, 2035: 0.4, 2045: 0.5, 2055: 0.3, 2065: 0.1, 2076: 0.0},
        "TRA":  {2026: 0, 2035:-0.3, 2045:-0.8, 2055:-1.2, 2065:-1.3, 2076:-1.2},
        "SKL":  {2026: 0, 2035: 0.4, 2045: 0.6, 2055: 0.7, 2065: 0.6, 2076: 0.5},
        "SVC":  {2026: 0, 2035: 0.5, 2045: 0.9, 2055: 1.3, 2065: 1.5, 2076: 1.6},
        "AGR":  {2026: 0, 2035: 0.2, 2045: 0.3, 2055: 0.2, 2065: 0.0, 2076:-0.1},
    },
    "EUR": {
        # Europe: green transition, aging crisis, AI regulation favors human jobs
        "TECH": {2026: 0, 2035: 0.6, 2045: 0.7, 2055: 0.4, 2065: 0.2, 2076: 0.0},
        "MED":  {2026: 0, 2035: 0.7, 2045: 1.3, 2055: 1.9, 2065: 2.3, 2076: 2.5},
        "FIN":  {2026: 0, 2035:-0.3, 2045:-0.7, 2055:-0.5, 2065:-0.3, 2076:-0.2},
        "EDU":  {2026: 0, 2035: 0.2, 2045: 0.4, 2055: 0.3, 2065: 0.2, 2076: 0.1},
        "ENG":  {2026: 0, 2035: 0.7, 2045: 0.9, 2055: 0.5, 2065: 0.1, 2076:-0.2},
        "GOV":  {2026: 0, 2035:-0.1, 2045:-0.4, 2055:-0.7, 2065:-0.9, 2076:-1.0},
        "LAW":  {2026: 0, 2035: 0.0, 2045:-0.2, 2055:-0.1, 2065: 0.1, 2076: 0.2},
        "ART":  {2026: 0, 2035: 0.2, 2045: 0.3, 2055: 0.1, 2065:-0.1, 2076:-0.2},
        "TRA":  {2026: 0, 2035:-0.4, 2045:-1.0, 2055:-1.4, 2065:-1.5, 2076:-1.4},
        "SKL":  {2026: 0, 2035: 0.6, 2045: 1.0, 2055: 1.3, 2065: 1.1, 2076: 0.9},
        "SVC":  {2026: 0, 2035: 0.4, 2045: 0.7, 2055: 1.1, 2065: 1.4, 2076: 1.6},
        "AGR":  {2026: 0, 2035: 0.3, 2045: 0.4, 2055: 0.3, 2065: 0.1, 2076: 0.0},
    },
    "AFR": {
        # Africa: massive youth population, digital leapfrog, infrastructure buildout
        "TECH": {2026: 0, 2035: 1.2, 2045: 1.8, 2055: 1.5, 2065: 1.0, 2076: 0.7},
        "MED":  {2026: 0, 2035: 0.5, 2045: 0.9, 2055: 1.3, 2065: 1.6, 2076: 1.8},
        "FIN":  {2026: 0, 2035: 0.5, 2045: 0.3, 2055: 0.0, 2065:-0.2, 2076:-0.3},
        "EDU":  {2026: 0, 2035: 0.8, 2045: 1.2, 2055: 1.0, 2065: 0.8, 2076: 0.6},
        "ENG":  {2026: 0, 2035: 0.9, 2045: 1.2, 2055: 1.0, 2065: 0.6, 2076: 0.3},
        "GOV":  {2026: 0, 2035: 0.1, 2045: 0.0, 2055:-0.2, 2065:-0.4, 2076:-0.5},
        "LAW":  {2026: 0, 2035: 0.2, 2045: 0.3, 2055: 0.2, 2065: 0.1, 2076: 0.1},
        "ART":  {2026: 0, 2035: 0.5, 2045: 0.7, 2055: 0.5, 2065: 0.3, 2076: 0.2},
        "TRA":  {2026: 0, 2035: 0.3, 2045: 0.0, 2055:-0.5, 2065:-0.8, 2076:-0.9},
        "SKL":  {2026: 0, 2035: 0.6, 2045: 0.9, 2055: 1.1, 2065: 1.0, 2076: 0.8},
        "SVC":  {2026: 0, 2035: 0.6, 2045: 1.0, 2055: 1.4, 2065: 1.7, 2076: 1.9},
        "AGR":  {2026: 0, 2035: 0.4, 2045: 0.6, 2055: 0.5, 2065: 0.3, 2076: 0.1},
    },
}


# ── Narratives ───────────────────────────────────────────────────────
NARRATIVES = {
    "CN": {
        "TECH": {
            2026: ("AI/半导体国产化热潮，高端人才极度稀缺", "AI/semiconductor localization boom, extreme talent shortage"),
            2035: ("AI基础编程岗被自动化取代，高端架构与AI安全需求激增", "Basic coding automated, surge in AI architecture and safety roles"),
            2045: ("技术全面渗透各行业，纯IT岗位收缩，跨界复合型人才主导", "Tech permeates all sectors, pure IT shrinks, cross-domain talent dominates"),
            2055: ("AI商品化完成，技术门槛降低，创新型与伦理治理岗成新蓝海", "AI commoditized, lower barriers, innovation and ethics governance as new blue ocean"),
            2065: ("量子计算/脑机接口催生新岗位，但整体技术就业趋于平稳", "Quantum/BCI creates new roles, but overall tech employment plateaus"),
            2076: ("技术完全融入社会基础设施，独立技术岗少但附加值极高", "Tech fully integrated into infrastructure, fewer standalone roles but very high value"),
        },
        "MED": {
            2026: ("老龄化初期+后疫情公卫投入，医疗人才需求上升", "Early aging + post-pandemic public health investment drives demand"),
            2035: ("65岁以上人口突破3亿，养老护理与慢病管理爆发式增长", "300M+ seniors, elderly care and chronic disease management explode"),
            2045: ("AI辅助诊疗普及，医生角色转向复杂决策与人文关怀", "AI-assisted diagnosis widespread, doctors shift to complex decisions and empathy"),
            2055: ("基因治疗/精准医学成熟，新型医学岗位大量涌现", "Gene therapy/precision medicine mature, new medical roles emerge en masse"),
            2065: ("超老龄社会，医疗健康成第一大就业领域", "Super-aged society, healthcare becomes #1 employment sector"),
            2076: ("人均寿命接近90，终身健康管理成为基础服务", "Life expectancy near 90, lifelong health management as basic service"),
        },
        "FIN": {
            2026: ("金融科技快速渗透，传统银行柜员大幅减少", "Fintech rapid penetration, traditional bank tellers decline sharply"),
            2035: ("AI量化交易主导，人工分析师仅限高端策略与合规", "AI quant trading dominates, human analysts only for strategy and compliance"),
            2045: ("数字人民币生态成熟，支付/清算岗位消失，风控复杂度升级", "Digital RMB ecosystem mature, payment roles vanish, risk control complexity rises"),
            2055: ("金融岗位大幅精简，但资产管理与跨境合规仍需人工", "Financial roles sharply reduced, but asset management and cross-border compliance need humans"),
            2065: ("AI监管沙盒全面运行，金融治理型人才需求回升", "AI regulatory sandboxes fully operational, financial governance talent demand recovers"),
            2076: ("金融与AI深度融合，人类角色聚焦信任/伦理/关系维护", "Finance-AI deep integration, human roles focus on trust/ethics/relationship"),
        },
        "EDU": {
            2026: ("双减政策调整后教培重组，在线教育高速发展", "Post-regulation restructuring, online education rapid growth"),
            2035: ("AI个性化教学普及，教师角色转向导师与情感支持", "AI personalized teaching widespread, teachers shift to mentoring and emotional support"),
            2045: ("终身学习成为刚需，企业培训与技能再造市场爆发", "Lifelong learning becomes essential, corporate training market explodes"),
            2055: ("教育内容AI自动生成，教育者聚焦创造力与批判思维培养", "AI auto-generates content, educators focus on creativity and critical thinking"),
            2065: ("教育与工作边界模糊，学习型组织成为主流", "Education-work boundaries blur, learning organizations become mainstream"),
            2076: ("脑机接口可能变革学习方式，传统教育模式根本转型", "BCI may transform learning, fundamental transformation of traditional education"),
        },
        "ENG": {
            2026: ("新能源/芯片/航空航天工程师极度紧缺", "Extreme shortage in new energy/chip/aerospace engineers"),
            2035: ("智能制造升级，传统产线工程师减少，绿色工程崛起", "Smart manufacturing upgrade, traditional line engineers decline, green engineering rises"),
            2045: ("碳中和目标推动大规模基础设施改造，工程需求阶段性高峰", "Carbon neutrality drives massive infrastructure renovation, engineering demand peaks"),
            2055: ("制造业自动化接近极限，工程师转向设计/创新/维护", "Manufacturing automation near limit, engineers shift to design/innovation/maintenance"),
            2065: ("传统工程岗持续萎缩，太空/深海/新材料成新前沿", "Traditional engineering shrinks, space/deep-sea/new materials as frontier"),
            2076: ("工程学高度跨学科化，纯机械/电气岗位稀少", "Engineering highly interdisciplinary, pure mechanical/electrical roles rare"),
        },
        "GOV": {
            2026: ("公务员稳定性高，竞争激烈但发展空间有限", "Civil service highly stable, competitive but limited growth"),
            2035: ("数字政务减少行政岗，政策分析与AI治理岗增加", "Digital government reduces admin, policy analysis and AI governance roles grow"),
            2045: ("AI行政审批普及，窗口服务岗位大幅压缩", "AI administrative approval widespread, service window roles sharply reduced"),
            2055: ("政府组织扁平化，公务员总量持续下降", "Government flattening, total civil servant numbers continue declining"),
            2065: ("公共治理复杂度升级，高端政策制定者不可替代", "Public governance complexity rises, senior policymakers irreplaceable"),
            2076: ("政府功能AI化程度极高，人类公务员精英化", "Government functions highly AI-driven, human civil servants become elite"),
        },
        "LAW": {
            2026: ("法律AI开始替代文书审查和合同审查初级岗位", "Legal AI begins replacing document review and junior contract roles"),
            2035: ("智能合约与AI仲裁兴起，诉讼律师需求下降", "Smart contracts and AI arbitration rise, litigation lawyer demand falls"),
            2045: ("AI法律顾问普及，人工律师聚焦复杂跨境和新型纠纷", "AI legal advisors widespread, human lawyers focus on complex cross-border disputes"),
            2055: ("法律服务平民化，高端法律创新与伦理咨询成增长点", "Legal services democratized, high-end legal innovation and ethics consulting grow"),
            2065: ("法律与科技深度融合，新型法律领域(太空法/AI法)兴起", "Law-tech deep integration, new legal fields (space law/AI law) emerge"),
            2076: ("法律框架需要根本性重构以适应后人类时代", "Legal frameworks need fundamental reconstruction for post-human era"),
        },
        "ART": {
            2026: ("短视频/直播经济带动内容创作就业", "Short video/live streaming drives content creation employment"),
            2035: ("AI生成内容泛滥，人类创意价值反而凸显", "AI-generated content floods market, human creativity value actually rises"),
            2045: ("虚拟现实/元宇宙催生新型艺术形态和大量岗位", "VR/metaverse creates new art forms and numerous positions"),
            2055: ("人工vs AI创作边界模糊，策展/审美/文化解读仍需人类", "Human vs AI creation boundaries blur, curation/aesthetics need humans"),
            2065: ("文化消费占GDP比重上升，但AI辅助大幅提升个人产出", "Cultural spending GDP share rises, but AI greatly boosts individual output"),
            2076: ("艺术成为人类身份认同核心，就业形态高度个体化", "Art becomes core of human identity, employment highly individualized"),
        },
        "TRA": {
            2026: ("网约车/即时配送支撑巨大就业，但自动驾驶开始测试", "Ride-hailing/instant delivery support massive employment, autonomous driving testing"),
            2035: ("L4自动驾驶商用化，出租车/货运司机大量失业", "L4 autonomous driving commercialized, massive taxi/truck driver unemployment"),
            2045: ("自动驾驶全面普及，驾驶类岗位接近消失，物流管理转型", "Autonomous driving ubiquitous, driving jobs near extinction, logistics management transforms"),
            2055: ("低空经济和无人配送成熟，交通系统全面智能化", "Low-altitude economy and drone delivery mature, transport fully intelligent"),
            2065: ("交通基础设施运维自动化，仅剩少量高端调度与应急岗位", "Transport infrastructure O&M automated, only senior dispatch and emergency roles remain"),
            2076: ("超级高铁/飞行汽车催生极小量新型运维岗", "Hyperloop/flying cars create very few new O&M roles"),
        },
        "SKL": {
            2026: ("技工荒持续，高级技师供不应求", "Skilled worker shortage continues, senior technicians in high demand"),
            2035: ("智能工具辅助提升技工效率，但核心手艺不可替代", "Smart tools boost skilled worker efficiency, but core craftsmanship irreplaceable"),
            2045: ("老龄化加剧技工荒，薪资水平显著上升", "Aging worsens skilled worker shortage, wages rise significantly"),
            2055: ("工业机器人承担重复性任务，高端维修/定制成为主流", "Industrial robots handle repetitive tasks, high-end repair/custom becomes mainstream"),
            2065: ("技工岗位精英化，收入接近工程师水平", "Skilled trades become elite, income approaches engineer level"),
            2076: ("传统手工艺成为文化遗产级稀缺技能", "Traditional craftsmanship becomes cultural heritage-level scarce skill"),
        },
        "SVC": {
            2026: ("平台经济重构服务业，灵活就业占比上升", "Platform economy restructures services, flexible employment share rises"),
            2035: ("养老/家政/护理需求激增，服务机器人初步辅助", "Elderly/domestic/care demand surges, service robots begin assisting"),
            2045: ("护理经济成为最大就业增长点之一", "Care economy becomes one of the largest employment growth areas"),
            2055: ("服务业AI辅助全面普及，人类聚焦情感与个性化服务", "Service AI assistance widespread, humans focus on emotional and personalized service"),
            2065: ("体验经济与情感经济主导消费，服务业高端化", "Experience and emotional economy dominate consumption, services go upscale"),
            2076: ("服务业是人类就业最大领域，深度个性化与心理疗愈为主", "Services largest human employment sector, deep personalization and mental healing dominate"),
        },
        "AGR": {
            2026: ("精准农业起步，传统农业仍占主导", "Precision agriculture starting, traditional farming still dominant"),
            2035: ("智慧农业技术推广，农业人口持续转移", "Smart agriculture tech adoption, rural-to-urban migration continues"),
            2045: ("垂直农场与基因编辑作物改变农业格局", "Vertical farms and gene-edited crops transform agriculture"),
            2055: ("农业高度自动化，就业人数极少但技术含量极高", "Agriculture highly automated, very few workers but very high tech"),
            2065: ("食品安全与生态治理成农业主要就业方向", "Food safety and ecological governance become main agricultural employment"),
            2076: ("合成生物学可能颠覆传统农业模式", "Synthetic biology may disrupt traditional agriculture models"),
        },
    },
}

# Copy and customize for other regions
NARRATIVES["ASIA"] = {
    "TECH": {
        2026: ("印度/东南亚IT外包高速增长，数字经济基础设施建设加速", "India/SE Asia IT outsourcing booming, digital infrastructure accelerating"),
        2035: ("亚洲成为全球AI研发第二极，软件工程师需求井喷", "Asia becomes global AI R&D second pole, software engineer demand surges"),
        2045: ("数字经济渗透率追平发达国家，基础IT岗位过剩", "Digital economy penetration catches up with developed nations, basic IT roles oversupplied"),
        2055: ("AI原生企业主导，技术岗位向创新与本地化方向演变", "AI-native companies dominate, tech roles evolve toward innovation and localization"),
        2065: ("技术人才跨境流动加剧，亚洲技术生态自成体系", "Tech talent cross-border mobility intensifies, Asia tech ecosystem self-contained"),
        2076: ("技术就业趋于稳定，人机协作成标准工作模式", "Tech employment stabilizes, human-AI collaboration becomes standard"),
    },
    "MED": {
        2026: ("南亚/东南亚医疗基础设施扩建，医护人才缺口巨大", "South/SE Asia healthcare infrastructure expansion, massive healthcare talent gap"),
        2035: ("远程医疗覆盖偏远地区，医学教育规模化", "Telemedicine reaches remote areas, medical education scales up"),
        2045: ("亚洲老龄化加速(日韩中)，医疗需求持续攀升", "Asian aging accelerates (JP/KR/CN), healthcare demand keeps climbing"),
        2055: ("医疗AI缩小城乡差距，但高端医疗人才仍集中在都市", "Medical AI narrows urban-rural gap, but top talent still concentrates in cities"),
        2065: ("亚洲成为全球医疗旅游中心，医疗出口带动就业", "Asia becomes global medical tourism hub, healthcare exports drive employment"),
        2076: ("基因编辑与再生医学重塑医疗体系", "Gene editing and regenerative medicine reshape healthcare systems"),
    },
    "FIN": {
        2026: ("亚洲金融科技领先全球，移动支付已普及", "Asian fintech leads globally, mobile payments already universal"),
        2035: ("数字银行取代传统网点，保险科技精简理赔", "Digital banks replace branches, insurtech streamlines claims"),
        2045: ("AI理财顾问普及，人工理财师仅服务超高净值客户", "AI financial advisors widespread, human advisors only for UHNW clients"),
        2055: ("跨境数字货币体系成熟，国际金融人才结构性转型", "Cross-border digital currency mature, international finance structural transformation"),
        2065: ("金融岗位回稳，新型风险管理与ESG合规持续增长", "Financial roles stabilize, new risk management and ESG compliance grow"),
        2076: ("金融服务完全嵌入日常生活，独立金融岗位缩减", "Financial services fully embedded in daily life, standalone roles shrink"),
    },
    "EDU": {
        2026: ("人口红利驱动教育投资，在线教育快速扩张", "Demographic dividend drives education investment, online education expands rapidly"),
        2035: ("AI教学工具普及到农村，教师需求从数量转向质量", "AI teaching tools reach rural areas, teacher demand shifts from quantity to quality"),
        2045: ("亚洲大学国际化程度大幅提升，跨境教育就业增长", "Asian university internationalization rises sharply, cross-border education employment grows"),
        2055: ("终身学习平台成熟，传统学校教师角色转型为学习设计师", "Lifelong learning platforms mature, traditional teachers transform to learning designers"),
        2065: ("教育科技成亚洲出口优势产业，相关就业增长", "Edtech becomes Asian export advantage, related employment grows"),
        2076: ("教育完全个性化，教育工作者聚焦社交情感学习", "Education fully personalized, educators focus on social-emotional learning"),
    },
    "ENG": {
        2026: ("亚洲制造业核心地位稳固，工程师需求旺盛", "Asia's manufacturing core position solid, strong engineer demand"),
        2035: ("智能工厂升级，传统产线工程师向自动化方向转型", "Smart factory upgrades, production line engineers shift to automation"),
        2045: ("亚洲主导新能源供应链，绿色工程师全球最稀缺", "Asia dominates new energy supply chains, green engineers globally scarce"),
        2055: ("制造业高端化完成，低端产线完全自动化", "Manufacturing upscaling complete, low-end lines fully automated"),
        2065: ("工程向太空/海洋/极端环境延伸，少量精英岗位", "Engineering extends to space/ocean/extreme environments, few elite roles"),
        2076: ("工程学与AI/生物融合，跨学科背景成为必备", "Engineering merges with AI/bio, interdisciplinary background essential"),
    },
    "GOV": {
        2026: ("各国政府数字化转型推进，公务员IT技能需求上升", "Government digital transformation advances, civil servant IT skills in demand"),
        2035: ("电子政务减少窗口岗位，但地区差异仍大", "E-government reduces counter positions, but regional disparities remain large"),
        2045: ("AI辅助决策进入政府体系，政策研究员需求增加", "AI-assisted decision-making enters government, policy researcher demand grows"),
        2055: ("政府规模普遍缩减，聚焦监管与公共服务设计", "Government size generally reduced, focusing on regulation and public service design"),
        2065: ("跨国治理议题增多，国际公务员需求微增", "Cross-national governance issues grow, international civil servant demand slightly rises"),
        2076: ("政府角色进一步精简，AI承担大部分行政功能", "Government role further streamlined, AI handles most administrative functions"),
    },
    "LAW": {
        2026: ("法律服务市场快速增长，合规需求带动律师就业", "Legal services market growing fast, compliance needs drive lawyer employment"),
        2035: ("AI法律助手普及，初级律师岗位竞争加剧", "AI legal assistants widespread, junior lawyer positions face intense competition"),
        2045: ("跨境电商纠纷处理AI化，知识产权法成增长点", "Cross-border e-commerce dispute AI-handled, IP law becomes growth area"),
        2055: ("法律AI处理90%标准案件，律师聚焦创新法律与调解", "Legal AI handles 90% standard cases, lawyers focus on innovative law and mediation"),
        2065: ("数据主权与AI伦理催生新型法律需求", "Data sovereignty and AI ethics create new legal demand"),
        2076: ("法律体系全面适应AI社会，法律哲学研究重要性上升", "Legal system fully adapted to AI society, legal philosophy research gains importance"),
    },
    "ART": {
        2026: ("K-pop/动漫/短视频推动亚洲文创产业全球化", "K-pop/anime/short video drive Asian cultural creative industry globalization"),
        2035: ("AI内容生成工具降低创作门槛，创意人才竞争加剧", "AI content tools lower creation barriers, creative talent competition intensifies"),
        2045: ("虚拟偶像与AI创作挑战传统艺人，但现场演出需求反增", "Virtual idols and AI creation challenge traditional artists, but live performance demand rises"),
        2055: ("沉浸式体验经济爆发，空间设计与叙事人才紧缺", "Immersive experience economy explodes, spatial design and narrative talent scarce"),
        2065: ("文化输出成为亚洲软实力核心，文创就业持续增长", "Cultural export becomes Asian soft power core, creative employment continues growing"),
        2076: ("人类艺术与AI艺术分化，手工艺/人类原创成奢侈品", "Human and AI art diverge, handcraft/human original becomes luxury"),
    },
    "TRA": {
        2026: ("电商物流带动配送员大军，网约车市场饱和", "E-commerce logistics drives delivery army, ride-hailing market saturated"),
        2035: ("自动驾驶在发达亚洲城市部署，东南亚仍以人力为主", "Autonomous driving deployed in developed Asian cities, SE Asia still labor-based"),
        2045: ("自动驾驶全面扩展，数百万驾驶岗位消失", "Autonomous driving fully expands, millions of driving jobs disappear"),
        2055: ("无人配送成为标准，物流管理平台化、算法化", "Unmanned delivery becomes standard, logistics management platform-based, algorithm-driven"),
        2065: ("交通系统全面自动化，仅少量应急与维护岗位", "Transport system fully automated, only few emergency and maintenance roles"),
        2076: ("新型交通工具(飞行器等)创造少量专业运维岗", "New transport modes (aircraft etc.) create few specialized O&M roles"),
    },
    "SKL": {
        2026: ("发达亚洲国家技工荒严重，薪资持续上涨", "Developed Asian countries face severe skilled worker shortage, wages keep rising"),
        2035: ("智能工具辅助施工，但建筑/维修技工需求依然旺盛", "Smart tools assist construction, but building/repair technician demand still strong"),
        2045: ("亚洲基础设施维护进入高峰期，技工需求稳定", "Asian infrastructure maintenance enters peak period, technician demand stable"),
        2055: ("3D打印/机器人替代部分技工，但精细作业仍需人工", "3D printing/robots replace some technicians, but fine work still needs humans"),
        2065: ("技工岗位高端化，跨技能复合型人才受追捧", "Skilled trades go upscale, cross-skill versatile talent in high demand"),
        2076: ("自动化覆盖大部分标准作业，手工技艺成为高端服务", "Automation covers most standard work, handcraft becomes premium service"),
    },
    "SVC": {
        2026: ("服务业吸纳亚洲最大就业，平台经济持续扩张", "Services absorb Asia's largest employment, platform economy keeps expanding"),
        2035: ("养老/护理服务需求暴增(日韩中)，年轻东南亚劳动力输出", "Elderly/care service demand surges (JP/KR/CN), young SE Asian labor exports"),
        2045: ("服务机器人进入家庭，但人类护理仍不可替代", "Service robots enter homes, but human care still irreplaceable"),
        2055: ("体验消费主导，服务从标准化转向极致个性化", "Experience consumption dominates, services shift from standardized to ultra-personalized"),
        2065: ("银发经济+情感经济成为服务业双引擎", "Silver economy + emotional economy become dual engines of services"),
        2076: ("服务业深度智能化但始终需要人的温度", "Services deeply intelligent but always need human warmth"),
    },
    "AGR": {
        2026: ("亚洲是全球农业劳动力最多的地区，现代化转型中", "Asia has world's most agricultural workers, modernization underway"),
        2035: ("精准农业技术扩散，小农经济开始整合", "Precision agriculture tech spreads, smallholder farming begins consolidating"),
        2045: ("农业科技缩小产量差距，农业人口转移加速", "Agtech narrows yield gaps, rural-to-urban migration accelerates"),
        2055: ("垂直农场在亚洲城市兴起，传统农业就业继续缩减", "Vertical farms rise in Asian cities, traditional agriculture employment keeps shrinking"),
        2065: ("农业高度工业化，但热带/亚热带作物仍需人工管理", "Agriculture highly industrialized, but tropical crops still need human management"),
        2076: ("合成蛋白/人造肉挑战传统畜牧，农业就业结构根本转型", "Synthetic protein/cultured meat challenge traditional livestock, agriculture employment fundamentally transforms"),
    },
}

NARRATIVES["EUR"] = {
    "TECH": {
        2026: ("AI监管(EU AI Act)塑造负责任AI生态，合规技术需求增长", "EU AI Act shapes responsible AI ecosystem, compliance tech demand grows"),
        2035: ("欧洲AI自主化推进，但人才竞争不敌美亚，远程+移民补缺", "European AI autonomy advances, but talent competition lags US/Asia, remote+immigration fills gaps"),
        2045: ("技术岗位稳定增长，绿色科技与隐私技术成欧洲优势", "Tech jobs stable growth, green tech and privacy tech become European advantages"),
        2055: ("AI监管经验成为全球标准，催生大量合规与治理岗位", "AI regulatory experience becomes global standard, creates many compliance and governance roles"),
        2065: ("技术就业趋于平稳，欧洲重视人本科技(human-centric tech)", "Tech employment plateaus, Europe emphasizes human-centric tech"),
        2076: ("技术完全服务化，少量维护岗+大量AI伦理/政策岗", "Tech fully service-oriented, few maintenance + many AI ethics/policy roles"),
    },
    "MED": {
        2026: ("老龄化最严重地区，医护人员严重短缺", "Most aging region globally, severe healthcare worker shortage"),
        2035: ("高龄护理危机加深，大量引进亚非医护移民", "Elderly care crisis deepens, massive healthcare worker immigration from Asia/Africa"),
        2045: ("AI诊疗提高效率但无法替代人力护理，护理岗持续增长", "AI diagnosis improves efficiency but cannot replace human care, nursing roles keep growing"),
        2055: ("欧洲成全球老龄化应对典范，医疗技术出口创造高端岗位", "Europe becomes global aging response model, medical tech exports create high-end roles"),
        2065: ("老龄化高峰到达，医疗健康占GDP 15%+，就业第一大类", "Aging peak arrives, healthcare 15%+ of GDP, #1 employment category"),
        2076: ("再生医学延长健康寿命，医疗重心从治疗转向增强", "Regenerative medicine extends healthy lifespan, healthcare shifts from treatment to enhancement"),
    },
    "FIN": {
        2026: ("欧洲银行整合加速，金融科技挑战传统机构", "European bank consolidation accelerates, fintech challenges traditional institutions"),
        2035: ("数字欧元落地，传统支付岗位消失，ESG金融快速增长", "Digital Euro launches, traditional payment roles disappear, ESG finance grows rapidly"),
        2045: ("AI风控全面替代人工审核，合规岗位仍需人类判断", "AI risk control fully replaces manual review, compliance roles still need human judgment"),
        2055: ("金融岗位缩减趋稳，可持续金融与碳交易成新增长点", "Financial role reduction stabilizes, sustainable finance and carbon trading as new growth"),
        2065: ("金融监管与技术深度融合，RegTech就业增长", "Financial regulation and tech deeply integrated, RegTech employment grows"),
        2076: ("金融高度自动化，人类聚焦关系型银行与价值观投资", "Finance highly automated, humans focus on relationship banking and values investing"),
    },
    "EDU": {
        2026: ("教育数字化转型加速，多语言AI教学工具兴起", "Education digital transformation accelerates, multilingual AI teaching tools emerge"),
        2035: ("终身学习政策制度化，成人再教育市场扩大", "Lifelong learning policies institutionalized, adult re-education market expands"),
        2045: ("欧洲大学吸引全球学生，国际教育成支柱产业", "European universities attract global students, international education becomes pillar industry"),
        2055: ("AI教师处理知识传授，人类教师聚焦苏格拉底式引导", "AI teachers handle knowledge transfer, human teachers focus on Socratic guidance"),
        2065: ("教育工作者数量减少但地位升高，成为高端专业", "Fewer educators but higher status, becomes elite profession"),
        2076: ("教育融入社会每个角落，教育者角色碎片化但不可或缺", "Education embedded everywhere in society, educator role fragmented but indispensable"),
    },
    "ENG": {
        2026: ("绿色转型推动风电/太阳能/氢能工程师需求猛增", "Green transition drives wind/solar/hydrogen engineer demand surge"),
        2035: ("碳中和工程全面展开，建筑翻新/电网升级创造大量工程岗", "Carbon neutrality engineering fully underway, building renovation/grid upgrade creates many roles"),
        2045: ("绿色基础设施建设高峰，工程就业黄金期", "Green infrastructure construction peak, engineering employment golden age"),
        2055: ("主要绿色改造完成，工程转向维护与优化", "Major green renovations complete, engineering shifts to maintenance and optimization"),
        2065: ("工程岗位回落，但核聚变/太空工程开辟新领域", "Engineering roles decline, but fusion/space engineering opens new fields"),
        2076: ("工程学高度专业化，广义工程岗位持续缩减", "Engineering highly specialized, general engineering roles keep shrinking"),
    },
    "GOV": {
        2026: ("欧洲政府规模庞大但效率改革压力增加", "European government large but efficiency reform pressure increases"),
        2035: ("AI行政减少公务员需求，但社会保障复杂度升高", "AI administration reduces civil servant needs, but social security complexity rises"),
        2045: ("跨国欧盟事务增多，国际公务员需求微增", "Cross-national EU affairs grow, international civil servant demand slightly rises"),
        2055: ("政府职能进一步精简，智能公共服务取代窗口岗", "Government functions further streamlined, smart public services replace counter positions"),
        2065: ("气候/移民/AI治理催生新型公共管理岗位", "Climate/migration/AI governance creates new public management roles"),
        2076: ("政府角色转向协调与仲裁，行政功能高度自动化", "Government role shifts to coordination and arbitration, admin highly automated"),
    },
    "LAW": {
        2026: ("GDPR/AI Act等法规创造大量合规律师需求", "GDPR/AI Act create massive compliance lawyer demand"),
        2035: ("法律科技普及，文档审核自动化，但隐私法持续创造岗位", "Legal tech widespread, document review automated, but privacy law keeps creating roles"),
        2045: ("AI法官实验试点，人类法律从业者向调解与策略转型", "AI judge experiments piloted, human legal practitioners shift to mediation and strategy"),
        2055: ("跨境法律纠纷AI处理，高端人权与国际法律仍需人类", "Cross-border legal disputes AI-handled, high-end human rights and international law still need humans"),
        2065: ("新型伦理与科技法律需求增长，法律哲学家受青睐", "New ethics and tech legal demand grows, legal philosophers in demand"),
        2076: ("法律体系面临后人类时代挑战，法律从业者极少但影响力大", "Legal system faces post-human era challenges, few practitioners but high influence"),
    },
    "ART": {
        2026: ("欧洲文化创意产业成熟，数字内容增长平稳", "European cultural creative industry mature, digital content steady growth"),
        2035: ("AI内容生成挑战欧洲创意传统，保护原创政策出台", "AI content generation challenges European creative tradition, originality protection policies emerge"),
        2045: ("沉浸式文化体验(VR博物馆/数字剧院)成为主流", "Immersive cultural experiences (VR museums/digital theaters) become mainstream"),
        2055: ("人类原创成为奢侈品，欧洲工匠传统溢价上升", "Human originals become luxury, European artisan tradition premium rises"),
        2065: ("文化遗产数字化保护创造新岗位，但总量有限", "Cultural heritage digital preservation creates new roles, but limited volume"),
        2076: ("艺术成为人类独特性最后堡垒，高度精英化", "Art becomes last bastion of human uniqueness, highly elitist"),
    },
    "TRA": {
        2026: ("欧洲铁路复兴+电动化，短途航空需求下降", "European rail revival + electrification, short-haul aviation demand drops"),
        2035: ("自动驾驶在高速公路普及，城市配送仍以人力为主", "Autonomous driving on highways widespread, urban delivery still labor-based"),
        2045: ("城市交通全面自动化，出租/公交司机岗位消失", "Urban transport fully automated, taxi/bus driver positions disappear"),
        2055: ("欧洲交通零排放目标达成，传统物流岗位大幅缩减", "Europe achieves zero-emission transport, traditional logistics roles sharply reduced"),
        2065: ("超级高铁连接主要城市，运输效率极高但就业极低", "Hyperloop connects major cities, transport efficiency very high but employment very low"),
        2076: ("交通成为公共基础设施服务，几乎无独立就业岗位", "Transport becomes public utility, almost no independent employment"),
    },
    "SKL": {
        2026: ("技工严重短缺，薪资快速上涨，移民技工增加", "Severe skilled worker shortage, wages rising fast, immigrant technicians increasing"),
        2035: ("绿色建筑改造创造海量技工需求，供不应求持续", "Green building renovation creates massive technician demand, shortage persists"),
        2045: ("技工成为中产核心职业，社会地位显著提升", "Skilled trades become core middle-class occupation, social status rises significantly"),
        2055: ("机器人替代部分标准作业，但装修/维修/安装仍需人工", "Robots replace some standard work, but renovation/repair/installation still need humans"),
        2065: ("技工岗位高端化并向服务化转型", "Skilled trades go upscale and shift toward service orientation"),
        2076: ("技工稀缺性达到历史峰值，成为高薪蓝领精英", "Skilled worker scarcity reaches historical peak, becomes high-paid blue-collar elite"),
    },
    "SVC": {
        2026: ("服务业是欧洲最大就业部门，数字化转型加速", "Services largest European employment sector, digital transformation accelerates"),
        2035: ("养老护理需求爆发，服务业就业增长核心来自护理经济", "Elderly care demand explodes, services employment growth core from care economy"),
        2045: ("服务机器人普及到餐饮/零售，人类转向高端服务", "Service robots widespread in dining/retail, humans shift to high-end services"),
        2055: ("体验经济与健康服务成为服务业两大支柱", "Experience economy and health services become two pillars of services"),
        2065: ("银发经济推动服务业持续增长，护理/陪伴岗最紧缺", "Silver economy drives continuous services growth, care/companion roles most scarce"),
        2076: ("服务业是人类就业绝对主体，AI辅助但无法取代温度", "Services absolute majority of human employment, AI assists but cannot replace warmth"),
    },
    "AGR": {
        2026: ("CAP改革推动可持续农业，有机农业增长", "CAP reform promotes sustainable agriculture, organic farming grows"),
        2035: ("精准农业全面推广，农业人口继续减少", "Precision agriculture fully adopted, agricultural population continues declining"),
        2045: ("欧洲农业高度机械化，但生态农业创造新岗位", "European agriculture highly mechanized, but ecological farming creates new roles"),
        2055: ("垂直农场与传统农场并存，农业科技人才需求增加", "Vertical and traditional farms coexist, agtech talent demand rises"),
        2065: ("气候变化影响南欧农业，北欧农业扩张", "Climate change impacts Southern European agriculture, Northern European agriculture expands"),
        2076: ("合成食品技术挑战传统农业，农业就业进一步缩减", "Synthetic food tech challenges traditional agriculture, agricultural employment further shrinks"),
    },
}

NARRATIVES["AFR"] = {
    "TECH": {
        2026: ("移动互联网和金融科技跨越式发展，IT人才极度短缺", "Mobile internet and fintech leapfrog development, extreme IT talent shortage"),
        2035: ("非洲科技创业生态爆发，本土独角兽涌现", "African tech startup ecosystem explodes, local unicorns emerge"),
        2045: ("数字经济成为GDP核心驱动力，IT岗位需求达到峰值", "Digital economy becomes GDP core driver, IT job demand peaks"),
        2055: ("AI工具降低技术门槛，IT就业从精英化转向大众化", "AI tools lower tech barriers, IT employment shifts from elite to mass"),
        2065: ("非洲成为全球科技外包新中心，技术就业规模庞大", "Africa becomes new global tech outsourcing center, massive tech employment"),
        2076: ("技术就业增长放缓但基数大，AI原生工作方式成主流", "Tech employment growth slows but large base, AI-native work becomes mainstream"),
    },
    "MED": {
        2026: ("医疗资源极度匮乏，基层医护缺口巨大", "Extreme medical resource shortage, massive primary healthcare gap"),
        2035: ("远程医疗+AI诊断大幅改善覆盖率，医护培训加速", "Telemedicine + AI diagnosis greatly improve coverage, healthcare training accelerates"),
        2045: ("非洲人口突破20亿，医疗需求增速全球最快", "Africa's population exceeds 2 billion, healthcare demand growth fastest globally"),
        2055: ("医疗基础设施改善，专科医生和护理人才持续增长", "Healthcare infrastructure improves, specialist and nursing talent continues growing"),
        2065: ("非洲成为全球传染病防控中心，公卫人才国际需求大", "Africa becomes global infectious disease control center, public health talent in international demand"),
        2076: ("医疗体系逐步追赶全球水平，健康管理意识普及", "Healthcare system gradually catches up to global level, health management awareness widespread"),
    },
    "FIN": {
        2026: ("移动支付(M-Pesa模式)推动金融普惠，银行渗透率上升", "Mobile payments (M-Pesa model) drive financial inclusion, banking penetration rises"),
        2035: ("非洲数字银行生态成熟，微型金融就业快速增长", "African digital banking ecosystem matures, microfinance employment grows rapidly"),
        2045: ("金融科技覆盖率达到中等收入国家水平，传统银行岗位开始缩减", "Fintech coverage reaches middle-income country level, traditional banking roles begin shrinking"),
        2055: ("金融岗位增长放缓，AI处理大部分标准交易", "Financial role growth slows, AI handles most standard transactions"),
        2065: ("金融监管复杂化催生合规岗位，但总量不再增长", "Financial regulation complexity creates compliance roles, but total no longer growing"),
        2076: ("金融完全数字化，人工岗位聚焦关系与信任建设", "Finance fully digital, human roles focus on relationships and trust building"),
    },
    "EDU": {
        2026: ("非洲教育投资加速，基础教育教师大量招聘", "African education investment accelerates, massive basic education teacher recruitment"),
        2035: ("EdTech平台覆盖偏远地区，教师角色从知识传授转向引导", "EdTech platforms reach remote areas, teacher role shifts from knowledge transfer to guidance"),
        2045: ("非洲青年人口全球最多，教育需求空前旺盛", "Africa has world's most youth, education demand unprecedentedly strong"),
        2055: ("职业教育体系成熟，技能培训师成为高需求岗位", "Vocational education system matures, skills trainers become high-demand roles"),
        2065: ("非洲大学国际影响力提升，学术就业增长", "African university international influence rises, academic employment grows"),
        2076: ("终身学习理念深入人心，教育工作者始终供不应求", "Lifelong learning deeply ingrained, educators always in short supply"),
    },
    "ENG": {
        2026: ("基础设施建设高潮，土木/电气工程师极度短缺", "Infrastructure construction boom, civil/electrical engineers in extreme shortage"),
        2035: ("非洲城市化加速，建筑/交通/水利工程大规模展开", "African urbanization accelerates, construction/transport/water engineering massive scale"),
        2045: ("可再生能源工程成为增长引擎，太阳能工程师需求爆发", "Renewable energy engineering becomes growth engine, solar engineer demand explodes"),
        2055: ("主要基础设施建设完成，工程转向维护与升级", "Major infrastructure construction complete, engineering shifts to maintenance and upgrades"),
        2065: ("工业化深化但自动化追赶，传统工程岗开始缩减", "Industrialization deepens but automation catches up, traditional engineering roles begin shrinking"),
        2076: ("工程学向可持续发展方向高度特化", "Engineering highly specialized toward sustainable development"),
    },
    "GOV": {
        2026: ("非洲政府治理能力提升，公务员队伍逐步专业化", "African governance capacity improves, civil service gradually professionalizes"),
        2035: ("数字政务在部分国家推广，但整体仍以传统行政为主", "Digital governance adopted in some countries, but overall still traditional administration"),
        2045: ("政府规模随经济增长扩大，但效率改革压力增加", "Government size grows with economy, but efficiency reform pressure increases"),
        2055: ("AI行政在城市试点，但农村地区仍需大量公务员", "AI administration piloted in cities, but rural areas still need many civil servants"),
        2065: ("治理现代化加速，公务员总量开始缩减", "Governance modernization accelerates, total civil servant numbers begin declining"),
        2076: ("政府功能逐步AI化，但非洲进度慢于全球平均", "Government functions gradually AI-driven, but Africa pace slower than global average"),
    },
    "LAW": {
        2026: ("法律服务需求随经济发展上升，合规意识增强", "Legal services demand rises with economic development, compliance awareness strengthens"),
        2035: ("法律科技初步引入，但大部分法律工作仍为人工", "Legal tech initially introduced, but most legal work still manual"),
        2045: ("商业法/投资法需求增长，国际律师事务所大量设立非洲分所", "Commercial/investment law demand grows, international law firms establish Africa offices"),
        2055: ("法律AI处理标准合同，但复杂法律和调解仍需人工", "Legal AI handles standard contracts, but complex law and mediation still need humans"),
        2065: ("非洲法律体系现代化基本完成，法治环境改善带动法律就业", "African legal system modernization largely complete, improved rule of law drives legal employment"),
        2076: ("法律服务普惠化，AI降低法律服务成本", "Legal services become inclusive, AI lowers legal service costs"),
    },
    "ART": {
        2026: ("Nollywood/Afrobeats全球走红，非洲文创产业崛起", "Nollywood/Afrobeats global success, African creative industry rises"),
        2035: ("非洲文化输出加速，数字内容创作就业增长最快", "African cultural exports accelerate, digital content creation employment grows fastest"),
        2045: ("AI创作工具普及，非洲创意人才聚焦本土文化叙事", "AI creation tools widespread, African creative talent focuses on local cultural narratives"),
        2055: ("非洲成为全球文化多样性供给中心", "Africa becomes global cultural diversity supply center"),
        2065: ("文化创意产业成为GDP重要组成部分", "Cultural creative industry becomes important GDP component"),
        2076: ("非洲文化全球影响力达到历史顶峰", "African culture reaches historical peak of global influence"),
    },
    "TRA": {
        2026: ("摩托车/小型货车配送主导最后一公里", "Motorcycle/minivan delivery dominates last mile"),
        2035: ("铁路/公路网扩建，传统运输就业增长强劲", "Rail/road network expansion, traditional transport employment grows strongly"),
        2045: ("部分城市引入自动驾驶，但大部分仍以人力运输为主", "Some cities introduce autonomous driving, but most still labor-based transport"),
        2055: ("自动驾驶逐步扩展，驾驶岗位开始缓慢缩减", "Autonomous driving gradually expands, driving positions begin slowly shrinking"),
        2065: ("物流自动化追赶全球水平，运输就业明显下降", "Logistics automation catches up to global level, transport employment notably declines"),
        2076: ("交通基础设施智能化完成，传统运输岗位大幅减少", "Transport infrastructure intelligent upgrade complete, traditional transport roles sharply reduced"),
    },
    "SKL": {
        2026: ("建筑/电工/管工等技工需求旺盛，培训体系不足", "Construction/electrical/plumbing technician demand strong, training system insufficient"),
        2035: ("城市化推动住房建设，技工需求持续增长", "Urbanization drives housing construction, technician demand keeps growing"),
        2045: ("技工培训体系逐步完善，供给改善但需求更大", "Technician training system gradually improves, supply improves but demand greater"),
        2055: ("工业化推动工厂技术工人需求，但自动化开始蚕食低端岗", "Industrialization drives factory technician demand, but automation begins eroding low-end roles"),
        2065: ("技工岗位向中高端升级，基础技工被机器替代", "Skilled trades upgrade to mid-high end, basic technicians replaced by machines"),
        2076: ("技工稀缺度随自动化推进先降后升", "Skilled worker scarcity first drops then rises with automation"),
    },
    "SVC": {
        2026: ("非正规服务业吸纳大量青年就业", "Informal services absorb massive youth employment"),
        2035: ("平台经济正规化，服务业从非正规转向数字平台", "Platform economy formalization, services shift from informal to digital platforms"),
        2045: ("非洲中产崛起推动消费服务需求暴增", "African middle class rise drives consumer service demand surge"),
        2055: ("医疗/教育/养老服务需求持续扩大", "Healthcare/education/elderly service demand keeps expanding"),
        2065: ("服务业成为非洲第一大就业领域", "Services become Africa's #1 employment sector"),
        2076: ("服务经济全面成熟，但AI替代效应开始显现", "Service economy fully mature, but AI substitution effects begin appearing"),
    },
    "AGR": {
        2026: ("农业仍是非洲第一大就业，现代化程度低", "Agriculture still Africa's #1 employment, low modernization"),
        2035: ("农业科技引入改善产量，但就业人口仍庞大", "Agtech introduction improves yields, but employment population still massive"),
        2045: ("机械化加速，农业就业人口开始缩减", "Mechanization accelerates, agricultural employment population begins declining"),
        2055: ("食品加工与农业服务创造新型就业机会", "Food processing and agricultural services create new employment opportunities"),
        2065: ("非洲成为全球粮食安全关键供给方", "Africa becomes critical global food security supplier"),
        2076: ("农业就业大幅缩减但产出倍增，农业科技就业增长", "Agricultural employment sharply reduced but output doubles, agtech employment grows"),
    },
}


def compute_predictions(df):
    """Main prediction engine. Returns a DataFrame with 288 rows."""
    rows = []

    for region_key, rdef in REGION_DEFS.items():
        subset = rdef["filter"](df)
        label_zh = rdef["label_zh"]
        label_en = rdef["label_en"]

        for cat_code in CATEGORY_ORDER:
            cat_data = subset[subset["major_code"] == cat_code]
            if cat_data.empty:
                continue

            # Baseline metrics
            baseline_composite = cat_data["composite_index"].mean()
            mean_ai_resistance = cat_data["ai_resistance"].mean()
            mean_trend = cat_data["trend_2000_2026"].mean()

            # AI timeline: compute average midpoint year for this category×region
            ai_midpoints = cat_data["ai_timeline"].apply(_parse_ai_timeline)
            mean_ai_midpoint = ai_midpoints.mean()

            cat_zh = CATEGORY_ZH.get(cat_code, cat_code)

            for decade in DECADES:
                # 1. Start with baseline
                idx = baseline_composite

                # 2. AI impact decay
                ai_factor = _ai_impact_factor(mean_ai_midpoint, mean_ai_resistance, decade)
                idx -= ai_factor * baseline_composite

                # 3. Trend extrapolation
                t_factor = _trend_factor(mean_trend, decade)
                idx += t_factor

                # 4. Structural shifts
                struct_key = region_key
                s_factor = _STRUCT.get(struct_key, {}).get(cat_code, {}).get(decade, 0)
                idx += s_factor

                # Clamp to reasonable bounds [1.0, 10.0]
                idx = max(1.0, min(10.0, idx))

                rows.append({
                    "region": label_zh,
                    "region_en": label_en,
                    "major_code": cat_code,
                    "major_category": cat_zh,
                    "decade": decade,
                    "recommendation_index": round(idx, 2),
                    "ai_impact_factor": round(ai_factor, 4),
                    "trend_factor": round(t_factor, 4),
                    "structural_factor": round(s_factor, 2),
                })

    result = pd.DataFrame(rows)

    # Compute recommendation_share per region×decade
    result["recommendation_share"] = 0.0
    for (rgn, dec), grp in result.groupby(["region", "decade"]):
        total = grp["recommendation_index"].sum()
        if total > 0:
            shares = (grp["recommendation_index"] / total * 100).round(2)
            result.loc[grp.index, "recommendation_share"] = shares

    # Compute change_vs_2026
    baseline_map = {}
    for _, row in result[result["decade"] == 2026].iterrows():
        key = (row["region"], row["major_code"])
        baseline_map[key] = row["recommendation_index"]

    result["change_vs_2026"] = result.apply(
        lambda r: round(r["recommendation_index"] - baseline_map.get(
            (r["region"], r["major_code"]), r["recommendation_index"]
        ), 2),
        axis=1,
    )

    # Add narratives
    region_key_map = {"中国": "CN", "亚洲": "ASIA", "欧洲": "EUR", "非洲": "AFR"}

    def _get_narrative(row, lang):
        rk = region_key_map.get(row["region"], "")
        narr = NARRATIVES.get(rk, {}).get(row["major_code"], {}).get(row["decade"], ("", ""))
        return narr[0] if lang == "zh" else narr[1]

    result["narrative_zh"] = result.apply(lambda r: _get_narrative(r, "zh"), axis=1)
    result["narrative_en"] = result.apply(lambda r: _get_narrative(r, "en"), axis=1)

    # Reorder columns
    col_order = [
        "region", "region_en", "major_code", "major_category", "decade",
        "recommendation_index", "recommendation_share", "change_vs_2026",
        "ai_impact_factor", "trend_factor", "structural_factor",
        "narrative_zh", "narrative_en",
    ]
    result = result[col_order]

    # Sort by region, decade, recommendation_index descending
    result = result.sort_values(
        ["region", "decade", "recommendation_index"],
        ascending=[True, True, False],
    ).reset_index(drop=True)

    return result


def main():
    print("Loading source data...")
    df = pd.read_csv(CSV_PATH)
    print(f"  Loaded {len(df)} rows from {CSV_PATH}")

    print("Computing 50-year predictions...")
    predictions = compute_predictions(df)
    print(f"  Generated {len(predictions)} prediction rows")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
    print(f"  Saved to {OUT_PATH}")

    # Quick summary
    for region in predictions["region"].unique():
        print(f"\n  [{region}]")
        for decade in DECADES:
            subset = predictions[(predictions["region"] == region) & (predictions["decade"] == decade)]
            top = subset.nlargest(3, "recommendation_index")
            cats = ", ".join(f"{r['major_code']}({r['recommendation_index']:.1f})" for _, r in top.iterrows())
            print(f"    {decade}: top3 = {cats}")


if __name__ == "__main__":
    main()
