#!/usr/bin/env python3
"""Generate tech_digital.csv — TECH pilot data for Global Career Development Index.

Creates scored data for all TECH occupations across all 45 countries/regions.
Uses realistic, country-differentiated scoring based on global labor market knowledge.
"""

import csv
import sys
import random
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.score_calculator import load_weights, calculate_composite

# ---------------------------------------------------------------------------
# OCCUPATION DEFINITIONS (from categories.yaml TECH section)
# ---------------------------------------------------------------------------

OCCUPATIONS = [
    # software_dev
    {"id": "0101", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "前端工程师", "en": "Front-end Engineer", "isco": "2514", "onet": "15-1254.00", "locality": "global"},
    {"id": "0102", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "后端工程师", "en": "Back-end Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0103", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "全栈工程师", "en": "Full-stack Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0104", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "移动应用开发工程师", "en": "Mobile App Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0105", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "嵌入式软件工程师", "en": "Embedded Software Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0106", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "DevOps工程师", "en": "DevOps Engineer", "isco": "2522", "onet": "15-1244.00", "locality": "global"},
    {"id": "0107", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "软件测试工程师", "en": "Software QA Engineer", "isco": "2519", "onet": "15-1253.00", "locality": "global"},
    {"id": "0108", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "软件架构师", "en": "Software Architect", "isco": "2512", "onet": "15-1251.00", "locality": "global"},
    {"id": "0109", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "站点可靠性工程师(SRE)", "en": "Site Reliability Engineer (SRE)", "isco": "2522", "onet": "15-1244.00", "locality": "global"},
    {"id": "0110", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "低代码/无代码开发者", "en": "Low-Code/No-Code Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0111", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "游戏服务器工程师", "en": "Game Server Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0112", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "数据库管理员", "en": "Database Administrator", "isco": "2521", "onet": "15-1242.00", "locality": "global"},
    {"id": "0113", "mid": "software_dev", "mid_zh": "软件开发", "mid_en": "Software Development",
     "zh": "技术支持工程师", "en": "Technical Support Engineer", "isco": "2519", "onet": "15-1232.00", "locality": "global"},
    # ai_data
    {"id": "0201", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "机器学习工程师", "en": "Machine Learning Engineer", "isco": "2511", "onet": "15-2051.00", "locality": "global"},
    {"id": "0202", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "数据科学家", "en": "Data Scientist", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "0203", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "数据分析师", "en": "Data Analyst", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "0204", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "数据工程师", "en": "Data Engineer", "isco": "2523", "onet": "15-1243.00", "locality": "global"},
    {"id": "0205", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "NLP工程师", "en": "NLP Engineer", "isco": "2511", "onet": "15-2051.00", "locality": "global"},
    {"id": "0206", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "计算机视觉工程师", "en": "Computer Vision Engineer", "isco": "2511", "onet": "15-2051.00", "locality": "global"},
    {"id": "0207", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "AI研究科学家", "en": "AI Research Scientist", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "0208", "mid": "ai_data", "mid_zh": "人工智能与数据", "mid_en": "Artificial Intelligence & Data",
     "zh": "大数据架构师", "en": "Big Data Architect", "isco": "2523", "onet": "15-1243.00", "locality": "global"},
    # network_security
    {"id": "0301", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "网络工程师", "en": "Network Engineer", "isco": "2523", "onet": "15-1241.00", "locality": "global"},
    {"id": "0302", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "信息安全工程师", "en": "Cybersecurity Engineer", "isco": "2529", "onet": "15-1212.00", "locality": "global"},
    {"id": "0303", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "渗透测试工程师", "en": "Penetration Tester", "isco": "2529", "onet": "15-1212.00", "locality": "global"},
    {"id": "0304", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "安全运维工程师", "en": "Security Operations Engineer", "isco": "2529", "onet": "15-1212.00", "locality": "global"},
    {"id": "0305", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "云计算工程师", "en": "Cloud Engineer", "isco": "2523", "onet": "15-1244.00", "locality": "global"},
    {"id": "0306", "mid": "network_security", "mid_zh": "网络与安全", "mid_en": "Network & Cybersecurity",
     "zh": "系统管理员", "en": "System Administrator", "isco": "2522", "onet": "15-1244.00", "locality": "global"},
    # product_design
    {"id": "0401", "mid": "product_design", "mid_zh": "产品与设计", "mid_en": "Product & Design",
     "zh": "产品经理", "en": "Product Manager", "isco": "2511", "onet": "15-1299.09", "locality": "global"},
    {"id": "0402", "mid": "product_design", "mid_zh": "产品与设计", "mid_en": "Product & Design",
     "zh": "UI设计师", "en": "UI Designer", "isco": "2166", "onet": "15-1255.00", "locality": "global"},
    {"id": "0403", "mid": "product_design", "mid_zh": "产品与设计", "mid_en": "Product & Design",
     "zh": "UX设计师", "en": "UX Designer", "isco": "2166", "onet": "15-1255.00", "locality": "global"},
    {"id": "0404", "mid": "product_design", "mid_zh": "产品与设计", "mid_en": "Product & Design",
     "zh": "交互设计师", "en": "Interaction Designer", "isco": "2166", "onet": "15-1255.00", "locality": "global"},
    {"id": "0405", "mid": "product_design", "mid_zh": "产品与设计", "mid_en": "Product & Design",
     "zh": "技术项目经理", "en": "Technical Project Manager", "isco": "1330", "onet": "15-1299.09", "locality": "global"},
    # emerging_digital
    {"id": "0501", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "区块链开发工程师", "en": "Blockchain Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0502", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "物联网工程师", "en": "IoT Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0503", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "机器人流程自动化工程师", "en": "RPA Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0504", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "增强现实/虚拟现实开发工程师", "en": "AR/VR Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0505", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "量子计算研究员", "en": "Quantum Computing Researcher", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "0506", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "AI提示工程师", "en": "AI Prompt Engineer", "isco": "2511", "onet": "15-1299.09", "locality": "global"},
    {"id": "0507", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "数据标注师", "en": "Data Annotator", "isco": "4132", "onet": "43-9021.00", "locality": "global"},
    {"id": "0508", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "数字孪生工程师", "en": "Digital Twin Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0509", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "边缘计算工程师", "en": "Edge Computing Engineer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0510", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "Web3开发工程师", "en": "Web3 Developer", "isco": "2514", "onet": "15-1252.00", "locality": "global"},
    {"id": "0511", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "AI安全研究员", "en": "AI Safety Researcher", "isco": "2511", "onet": "15-2051.00", "locality": "global"},
    {"id": "0512", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "MLOps工程师", "en": "MLOps Engineer", "isco": "2522", "onet": "15-1244.00", "locality": "global"},
    {"id": "0513", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "合成数据工程师", "en": "Synthetic Data Engineer", "isco": "2511", "onet": "15-2051.00", "locality": "global"},
    {"id": "0514", "mid": "emerging_digital", "mid_zh": "新兴数字职业", "mid_en": "Emerging Digital Occupations",
     "zh": "数字无障碍专家", "en": "Digital Accessibility Specialist", "isco": "2514", "onet": "15-1255.00", "locality": "global"},
]

# ---------------------------------------------------------------------------
# COUNTRY METADATA (from mapping/country_meta.csv)
# ---------------------------------------------------------------------------

COUNTRIES = [
    {"iso": "CN", "name_zh": "中国", "name_en": "China", "region": "东亚", "type": "country", "dev": "emerging"},
    {"iso": "JP", "name_zh": "日本", "name_en": "Japan", "region": "东亚", "type": "country", "dev": "developed"},
    {"iso": "KR", "name_zh": "韩国", "name_en": "South Korea", "region": "东亚", "type": "country", "dev": "developed"},
    {"iso": "TW", "name_zh": "中国台湾地区", "name_en": "Taiwan (China)", "region": "东亚", "type": "region", "dev": "developed"},
    {"iso": "HK", "name_zh": "中国香港地区", "name_en": "Hong Kong (China)", "region": "东亚", "type": "region", "dev": "developed"},
    {"iso": "SG", "name_zh": "新加坡", "name_en": "Singapore", "region": "东南亚", "type": "country", "dev": "developed"},
    {"iso": "TH", "name_zh": "泰国", "name_en": "Thailand", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "VN", "name_zh": "越南", "name_en": "Vietnam", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "ID", "name_zh": "印度尼西亚", "name_en": "Indonesia", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "MY", "name_zh": "马来西亚", "name_en": "Malaysia", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "PH", "name_zh": "菲律宾", "name_en": "Philippines", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "IN", "name_zh": "印度", "name_en": "India", "region": "南亚", "type": "country", "dev": "emerging"},
    {"iso": "PK", "name_zh": "巴基斯坦", "name_en": "Pakistan", "region": "南亚", "type": "country", "dev": "developing"},
    {"iso": "BD", "name_zh": "孟加拉国", "name_en": "Bangladesh", "region": "南亚", "type": "country", "dev": "developing"},
    {"iso": "AE", "name_zh": "阿联酋", "name_en": "United Arab Emirates", "region": "中亚/西亚", "type": "country", "dev": "developed"},
    {"iso": "IL", "name_zh": "以色列", "name_en": "Israel", "region": "中亚/西亚", "type": "country", "dev": "developed"},
    {"iso": "SA", "name_zh": "沙特阿拉伯", "name_en": "Saudi Arabia", "region": "中亚/西亚", "type": "country", "dev": "emerging"},
    {"iso": "TR", "name_zh": "土耳其", "name_en": "Turkey", "region": "中亚/西亚", "type": "country", "dev": "emerging"},
    {"iso": "GB", "name_zh": "英国", "name_en": "United Kingdom", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "FR", "name_zh": "法国", "name_en": "France", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "DE", "name_zh": "德国", "name_en": "Germany", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "NL", "name_zh": "荷兰", "name_en": "Netherlands", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "CH", "name_zh": "瑞士", "name_en": "Switzerland", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "SE", "name_zh": "瑞典", "name_en": "Sweden", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "DK", "name_zh": "丹麦", "name_en": "Denmark", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "FI", "name_zh": "芬兰", "name_en": "Finland", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "IT", "name_zh": "意大利", "name_en": "Italy", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "ES", "name_zh": "西班牙", "name_en": "Spain", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "PT", "name_zh": "葡萄牙", "name_en": "Portugal", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "PL", "name_zh": "波兰", "name_en": "Poland", "region": "东欧", "type": "country", "dev": "emerging"},
    {"iso": "CZ", "name_zh": "捷克", "name_en": "Czech Republic", "region": "东欧", "type": "country", "dev": "developed"},
    {"iso": "RU", "name_zh": "俄罗斯", "name_en": "Russia", "region": "东欧", "type": "country", "dev": "emerging"},
    {"iso": "US", "name_zh": "美国", "name_en": "United States", "region": "北美", "type": "country", "dev": "developed"},
    {"iso": "CA", "name_zh": "加拿大", "name_en": "Canada", "region": "北美", "type": "country", "dev": "developed"},
    {"iso": "MX", "name_zh": "墨西哥", "name_en": "Mexico", "region": "北美", "type": "country", "dev": "emerging"},
    {"iso": "BR", "name_zh": "巴西", "name_en": "Brazil", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "AR", "name_zh": "阿根廷", "name_en": "Argentina", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "CL", "name_zh": "智利", "name_en": "Chile", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "CO", "name_zh": "哥伦比亚", "name_en": "Colombia", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "AU", "name_zh": "澳大利亚", "name_en": "Australia", "region": "大洋洲", "type": "country", "dev": "developed"},
    {"iso": "NZ", "name_zh": "新西兰", "name_en": "New Zealand", "region": "大洋洲", "type": "country", "dev": "developed"},
    {"iso": "ZA", "name_zh": "南非", "name_en": "South Africa", "region": "非洲", "type": "country", "dev": "emerging"},
    {"iso": "NG", "name_zh": "尼日利亚", "name_en": "Nigeria", "region": "非洲", "type": "country", "dev": "developing"},
    {"iso": "KE", "name_zh": "肯尼亚", "name_en": "Kenya", "region": "非洲", "type": "country", "dev": "developing"},
    {"iso": "EG", "name_zh": "埃及", "name_en": "Egypt", "region": "非洲", "type": "country", "dev": "developing"},
]

# ---------------------------------------------------------------------------
# COUNTRY PROFILES — modifiers that shape scores by country characteristics
# Each country has a profile dict that shifts various score dimensions.
# ---------------------------------------------------------------------------

# Country tech-ecosystem profiles: (tech_maturity, compensation, work_life_balance,
#   remote_culture, stability_env, ai_adoption, market_dynamism, gender_eq,
#   education_quality, international_openness, regulatory_env, overtime_culture)
# All on 0-10 scale representing relative standing.

COUNTRY_PROFILES = {
    # TECH POWERHOUSES
    "US": {"tech": 9.5, "comp": 9.5, "wlb": 5.5, "remote": 9.0, "stab": 5.5, "ai": 9.5, "market": 9.5, "gender": 7.5, "edu": 9.0, "intl": 8.5, "reg": 6.0, "ot": 4.5},
    "IL": {"tech": 9.0, "comp": 8.0, "wlb": 6.0, "remote": 8.0, "stab": 5.5, "ai": 9.0, "market": 7.0, "gender": 7.0, "edu": 8.5, "intl": 8.0, "reg": 5.5, "ot": 5.0},
    "GB": {"tech": 8.5, "comp": 8.0, "wlb": 7.0, "remote": 8.5, "stab": 6.5, "ai": 8.0, "market": 8.0, "gender": 7.5, "edu": 8.5, "intl": 9.0, "reg": 7.0, "ot": 6.0},
    "DE": {"tech": 8.0, "comp": 7.5, "wlb": 8.0, "remote": 7.0, "stab": 8.0, "ai": 7.5, "market": 8.0, "gender": 7.0, "edu": 8.0, "intl": 8.0, "reg": 7.5, "ot": 7.5},
    "CA": {"tech": 8.0, "comp": 7.5, "wlb": 7.5, "remote": 8.5, "stab": 7.0, "ai": 8.0, "market": 7.5, "gender": 8.0, "edu": 8.0, "intl": 9.0, "reg": 7.0, "ot": 6.5},
    "CH": {"tech": 8.0, "comp": 9.0, "wlb": 8.5, "remote": 7.0, "stab": 9.0, "ai": 7.5, "market": 6.0, "gender": 7.0, "edu": 9.0, "intl": 8.5, "reg": 7.0, "ot": 7.0},
    "AU": {"tech": 7.5, "comp": 7.5, "wlb": 8.0, "remote": 8.0, "stab": 7.5, "ai": 7.0, "market": 7.0, "gender": 8.0, "edu": 8.0, "intl": 8.5, "reg": 7.0, "ot": 7.0},
    "NL": {"tech": 8.0, "comp": 7.5, "wlb": 9.0, "remote": 8.5, "stab": 7.5, "ai": 7.5, "market": 6.5, "gender": 8.5, "edu": 8.0, "intl": 9.0, "reg": 7.0, "ot": 8.0},
    "SE": {"tech": 8.0, "comp": 7.0, "wlb": 9.0, "remote": 8.5, "stab": 8.0, "ai": 7.5, "market": 6.0, "gender": 9.0, "edu": 8.5, "intl": 8.5, "reg": 7.0, "ot": 8.5},
    "DK": {"tech": 7.5, "comp": 7.0, "wlb": 9.0, "remote": 8.0, "stab": 8.0, "ai": 7.0, "market": 5.5, "gender": 9.0, "edu": 8.5, "intl": 8.5, "reg": 7.0, "ot": 8.5},
    "FI": {"tech": 8.0, "comp": 6.5, "wlb": 9.0, "remote": 8.5, "stab": 7.5, "ai": 7.5, "market": 5.5, "gender": 9.0, "edu": 9.0, "intl": 8.0, "reg": 7.0, "ot": 8.5},
    "SG": {"tech": 8.5, "comp": 8.0, "wlb": 5.5, "remote": 7.0, "stab": 8.0, "ai": 8.0, "market": 6.5, "gender": 7.0, "edu": 8.5, "intl": 9.5, "reg": 8.0, "ot": 4.5},
    "FR": {"tech": 7.5, "comp": 6.5, "wlb": 8.0, "remote": 7.0, "stab": 7.0, "ai": 7.0, "market": 7.5, "gender": 7.0, "edu": 8.0, "intl": 7.5, "reg": 7.5, "ot": 7.0},
    "NZ": {"tech": 7.0, "comp": 6.5, "wlb": 8.5, "remote": 8.0, "stab": 7.5, "ai": 6.5, "market": 5.0, "gender": 8.5, "edu": 7.5, "intl": 8.0, "reg": 7.0, "ot": 7.5},
    "JP": {"tech": 8.0, "comp": 6.5, "wlb": 5.0, "remote": 6.0, "stab": 7.5, "ai": 7.0, "market": 8.0, "gender": 5.0, "edu": 8.0, "intl": 5.0, "reg": 6.5, "ot": 3.5},
    "KR": {"tech": 8.0, "comp": 6.5, "wlb": 4.5, "remote": 5.5, "stab": 6.0, "ai": 7.5, "market": 7.5, "gender": 4.5, "edu": 8.0, "intl": 6.0, "reg": 6.0, "ot": 3.0},
    "TW": {"tech": 8.0, "comp": 5.5, "wlb": 5.0, "remote": 5.5, "stab": 6.0, "ai": 7.0, "market": 6.5, "gender": 6.0, "edu": 7.5, "intl": 6.5, "reg": 6.0, "ot": 4.0},
    "HK": {"tech": 7.0, "comp": 7.0, "wlb": 4.5, "remote": 6.5, "stab": 6.5, "ai": 7.0, "market": 5.5, "gender": 6.5, "edu": 7.5, "intl": 9.0, "reg": 6.5, "ot": 3.5},
    # LARGE EMERGING TECH ECONOMIES
    "CN": {"tech": 8.5, "comp": 7.0, "wlb": 3.5, "remote": 5.0, "stab": 5.0, "ai": 8.5, "market": 9.5, "gender": 5.5, "edu": 7.5, "intl": 5.0, "reg": 5.0, "ot": 2.5},
    "IN": {"tech": 7.5, "comp": 5.0, "wlb": 4.5, "remote": 7.5, "stab": 5.0, "ai": 7.0, "market": 9.0, "gender": 4.5, "edu": 7.0, "intl": 7.5, "reg": 5.0, "ot": 4.0},
    "BR": {"tech": 6.0, "comp": 4.5, "wlb": 6.0, "remote": 7.0, "stab": 4.5, "ai": 5.0, "market": 7.5, "gender": 5.5, "edu": 6.0, "intl": 5.0, "reg": 5.5, "ot": 5.0},
    "RU": {"tech": 7.0, "comp": 4.5, "wlb": 5.5, "remote": 7.0, "stab": 4.0, "ai": 6.0, "market": 6.5, "gender": 6.0, "edu": 7.5, "intl": 3.5, "reg": 4.0, "ot": 5.5},
    "PL": {"tech": 7.0, "comp": 5.5, "wlb": 7.0, "remote": 7.5, "stab": 6.5, "ai": 6.0, "market": 6.0, "gender": 6.5, "edu": 7.0, "intl": 7.5, "reg": 6.5, "ot": 6.0},
    "CZ": {"tech": 7.0, "comp": 5.5, "wlb": 7.5, "remote": 7.0, "stab": 7.0, "ai": 6.0, "market": 5.5, "gender": 6.5, "edu": 7.0, "intl": 7.5, "reg": 6.5, "ot": 6.5},
    "IT": {"tech": 6.0, "comp": 5.5, "wlb": 6.5, "remote": 6.0, "stab": 5.5, "ai": 5.5, "market": 6.5, "gender": 5.5, "edu": 7.0, "intl": 6.5, "reg": 6.0, "ot": 5.5},
    "ES": {"tech": 6.0, "comp": 5.0, "wlb": 7.0, "remote": 7.0, "stab": 5.0, "ai": 5.5, "market": 6.0, "gender": 6.5, "edu": 7.0, "intl": 7.0, "reg": 6.0, "ot": 5.5},
    "PT": {"tech": 6.0, "comp": 4.5, "wlb": 7.0, "remote": 7.5, "stab": 5.5, "ai": 5.0, "market": 5.0, "gender": 7.0, "edu": 6.5, "intl": 7.5, "reg": 6.0, "ot": 6.0},
    "MX": {"tech": 5.5, "comp": 4.0, "wlb": 5.5, "remote": 6.5, "stab": 4.5, "ai": 4.5, "market": 6.5, "gender": 5.0, "edu": 5.5, "intl": 5.5, "reg": 5.0, "ot": 4.5},
    "AR": {"tech": 5.5, "comp": 3.5, "wlb": 5.5, "remote": 7.0, "stab": 3.5, "ai": 4.5, "market": 5.0, "gender": 5.5, "edu": 6.5, "intl": 5.5, "reg": 4.5, "ot": 5.0},
    "CL": {"tech": 5.5, "comp": 4.5, "wlb": 6.0, "remote": 6.5, "stab": 5.5, "ai": 4.5, "market": 4.5, "gender": 5.5, "edu": 6.0, "intl": 6.0, "reg": 5.5, "ot": 5.5},
    "CO": {"tech": 5.0, "comp": 3.5, "wlb": 5.5, "remote": 6.5, "stab": 4.5, "ai": 4.0, "market": 5.0, "gender": 5.0, "edu": 5.5, "intl": 5.0, "reg": 5.0, "ot": 5.0},
    # MIDDLE EAST
    "AE": {"tech": 7.5, "comp": 8.0, "wlb": 5.5, "remote": 6.0, "stab": 7.0, "ai": 7.0, "market": 5.5, "gender": 5.5, "edu": 7.0, "intl": 8.5, "reg": 6.5, "ot": 5.0},
    "SA": {"tech": 6.0, "comp": 6.5, "wlb": 5.5, "remote": 5.0, "stab": 6.0, "ai": 6.0, "market": 5.5, "gender": 4.0, "edu": 6.0, "intl": 5.5, "reg": 5.5, "ot": 5.0},
    "TR": {"tech": 6.0, "comp": 4.0, "wlb": 5.0, "remote": 6.0, "stab": 4.0, "ai": 5.0, "market": 6.5, "gender": 4.5, "edu": 6.5, "intl": 5.5, "reg": 5.0, "ot": 4.5},
    # SOUTHEAST ASIA
    "TH": {"tech": 5.0, "comp": 3.5, "wlb": 5.5, "remote": 5.5, "stab": 5.5, "ai": 4.0, "market": 5.5, "gender": 6.0, "edu": 5.5, "intl": 5.0, "reg": 5.0, "ot": 5.5},
    "VN": {"tech": 5.5, "comp": 3.5, "wlb": 5.0, "remote": 6.0, "stab": 5.0, "ai": 4.5, "market": 6.0, "gender": 5.5, "edu": 5.5, "intl": 5.5, "reg": 5.0, "ot": 4.5},
    "ID": {"tech": 5.0, "comp": 3.5, "wlb": 5.5, "remote": 5.5, "stab": 5.0, "ai": 4.0, "market": 6.5, "gender": 5.0, "edu": 5.0, "intl": 4.5, "reg": 5.0, "ot": 5.0},
    "MY": {"tech": 6.0, "comp": 4.5, "wlb": 5.5, "remote": 6.0, "stab": 6.0, "ai": 5.0, "market": 5.0, "gender": 5.5, "edu": 6.0, "intl": 6.5, "reg": 5.5, "ot": 5.0},
    "PH": {"tech": 5.0, "comp": 3.0, "wlb": 5.0, "remote": 7.0, "stab": 4.5, "ai": 4.0, "market": 5.5, "gender": 6.5, "edu": 5.5, "intl": 6.5, "reg": 4.5, "ot": 4.5},
    # SOUTH ASIA
    "PK": {"tech": 4.0, "comp": 2.5, "wlb": 4.5, "remote": 6.5, "stab": 3.5, "ai": 3.5, "market": 5.0, "gender": 3.0, "edu": 4.5, "intl": 5.0, "reg": 4.0, "ot": 4.5},
    "BD": {"tech": 3.5, "comp": 2.0, "wlb": 4.5, "remote": 6.5, "stab": 3.5, "ai": 3.0, "market": 4.5, "gender": 3.5, "edu": 4.0, "intl": 5.0, "reg": 3.5, "ot": 4.5},
    # AFRICA
    "ZA": {"tech": 5.0, "comp": 4.0, "wlb": 5.5, "remote": 6.0, "stab": 4.5, "ai": 4.5, "market": 5.0, "gender": 5.5, "edu": 5.5, "intl": 5.5, "reg": 5.0, "ot": 5.5},
    "NG": {"tech": 4.0, "comp": 2.5, "wlb": 4.5, "remote": 6.0, "stab": 3.5, "ai": 3.5, "market": 5.0, "gender": 4.0, "edu": 4.0, "intl": 5.0, "reg": 3.5, "ot": 4.5},
    "KE": {"tech": 4.5, "comp": 2.5, "wlb": 5.0, "remote": 6.0, "stab": 4.0, "ai": 3.5, "market": 4.0, "gender": 4.5, "edu": 4.5, "intl": 5.5, "reg": 4.0, "ot": 5.0},
    "EG": {"tech": 4.5, "comp": 2.5, "wlb": 5.0, "remote": 5.5, "stab": 4.0, "ai": 3.5, "market": 5.5, "gender": 3.5, "edu": 5.0, "intl": 5.0, "reg": 4.0, "ot": 4.5},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES — intrinsic characteristics of each occupation
# These are "global baseline" scores that get modulated by country profiles
# ---------------------------------------------------------------------------

# Base scores for each occupation on key dimensions.
# Format: (learning_cost, education_req, growth_coeff, career_lifespan,
#   opportunity, market_size, supply_demand, developed_scarcity,
#   value_added, cost_performance, stability, safety, occ_disease, overtime, burnout,
#   skill_versatility, career_switch, reputation_variance,
#   ai_resistance, social_status, remote_friendly, autonomy,
#   family_friendly, fulfillment, entrepreneurship, gender_equality,
#   age_flexibility, social_interaction, physical_demand, license_barrier,
#   cycle_sensitivity, side_job_compat, intl_mobility, industry_monopoly,
#   trend_2000_2026, trend_5yr, typical_education, typical_entry_age)

def occ_base(occ_id):
    """Return base (global average) scores for an occupation."""
    bases = {
        # ===== SOFTWARE_DEV =====
        "0101": {  # Front-end Engineer
            "learning_cost": 5.0, "education_req": 4.5,
            "growth_coeff": 6.5, "career_lifespan": 6.0,
            "opportunity": 7.5, "market_size": 8.5, "supply_demand": 5.5, "developed_scarcity": 5.0,
            "value_added": 6.5, "cost_performance": 7.0,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.0,
            "ai_resistance": 4.5, "social_status": 6.0, "remote_friendly": 9.0, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 7.5, "gender_equality": 6.0,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 8.0, "intl_mobility": 7.5, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 1, "edu": "本科/自学", "age": "20-28",
        },
        "0102": {  # Back-end Engineer
            "learning_cost": 5.5, "education_req": 5.0,
            "growth_coeff": 7.0, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 8.0, "supply_demand": 6.0, "developed_scarcity": 5.5,
            "value_added": 7.0, "cost_performance": 7.0,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 5.0, "social_status": 6.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.0, "entrepreneurship": 7.0, "gender_equality": 5.5,
            "age_flexibility": 6.0, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 7.5, "intl_mobility": 8.0, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科", "age": "21-28",
        },
        "0103": {  # Full-stack Engineer
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 7.5, "career_lifespan": 6.5,
            "opportunity": 8.0, "market_size": 7.0, "supply_demand": 6.5, "developed_scarcity": 6.0,
            "value_added": 7.5, "cost_performance": 7.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 8.5, "career_switch": 7.0, "reputation_variance": 2.0,
            "ai_resistance": 5.0, "social_status": 6.5, "remote_friendly": 9.0, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 7.0, "entrepreneurship": 8.5, "gender_equality": 5.5,
            "age_flexibility": 5.5, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 8.5, "intl_mobility": 8.0, "industry_monopoly": 1.5,
            "trend_long": 4, "trend_short": 2, "edu": "本科/自学", "age": "21-28",
        },
        "0104": {  # Mobile App Developer
            "learning_cost": 5.0, "education_req": 4.5,
            "growth_coeff": 6.0, "career_lifespan": 5.5,
            "opportunity": 7.0, "market_size": 7.5, "supply_demand": 5.0, "developed_scarcity": 4.5,
            "value_added": 6.5, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 2.0,
            "ai_resistance": 4.0, "social_status": 6.0, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 6.5, "entrepreneurship": 8.0, "gender_equality": 5.5,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 8.0, "intl_mobility": 7.5, "industry_monopoly": 2.5,
            "trend_long": 3, "trend_short": 0, "edu": "本科/自学", "age": "20-28",
        },
        "0105": {  # Embedded Software Engineer
            "learning_cost": 6.5, "education_req": 6.0,
            "growth_coeff": 6.5, "career_lifespan": 7.5,
            "opportunity": 6.0, "market_size": 5.5, "supply_demand": 6.5, "developed_scarcity": 7.0,
            "value_added": 7.0, "cost_performance": 6.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.0,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 5.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 5.5, "gender_equality": 4.5,
            "age_flexibility": 6.5, "social_interaction": 4.5, "physical_demand": 2.0, "license_barrier": 1.0,
            "cycle_sensitivity": 4.5, "side_job_compat": 5.5, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 3, "trend_short": 2, "edu": "本科/硕士", "age": "22-28",
        },
        "0106": {  # DevOps Engineer
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 6.5, "supply_demand": 7.5, "developed_scarcity": 7.0,
            "value_added": 7.5, "cost_performance": 7.5,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 4.5, "burnout": 5.5,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 5.5, "social_status": 6.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 6.5, "entrepreneurship": 6.5, "gender_equality": 5.0,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 6.5, "intl_mobility": 8.0, "industry_monopoly": 2.5,
            "trend_long": 4, "trend_short": 3, "edu": "本科", "age": "22-30",
        },
        "0107": {  # Software QA Engineer
            "learning_cost": 4.0, "education_req": 4.0,
            "growth_coeff": 5.0, "career_lifespan": 6.0,
            "opportunity": 6.0, "market_size": 7.0, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.5,
            "ai_resistance": 3.5, "social_status": 5.0, "remote_friendly": 8.0, "autonomy": 5.5,
            "family_friendly": 6.0, "fulfillment": 5.0, "entrepreneurship": 5.0, "gender_equality": 6.0,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 6.5, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": -1, "edu": "本科/大专", "age": "21-28",
        },
        "0108": {  # Software Architect
            "learning_cost": 7.5, "education_req": 6.5,
            "growth_coeff": 8.0, "career_lifespan": 8.0,
            "opportunity": 7.5, "market_size": 4.5, "supply_demand": 8.0, "developed_scarcity": 8.0,
            "value_added": 9.0, "cost_performance": 8.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 8.0, "career_switch": 7.5, "reputation_variance": 1.0,
            "ai_resistance": 7.0, "social_status": 8.0, "remote_friendly": 8.5, "autonomy": 8.5,
            "family_friendly": 6.0, "fulfillment": 8.0, "entrepreneurship": 7.5, "gender_equality": 5.0,
            "age_flexibility": 7.5, "social_interaction": 6.5, "physical_demand": 1.0, "license_barrier": 1.0,
            "cycle_sensitivity": 4.5, "side_job_compat": 7.0, "intl_mobility": 8.5, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科/硕士", "age": "28-35",
        },
        "0109": {  # SRE
            "learning_cost": 6.5, "education_req": 5.5,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.0, "market_size": 5.0, "supply_demand": 8.0, "developed_scarcity": 7.5,
            "value_added": 8.0, "cost_performance": 7.5,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 5.5, "overtime": 4.0, "burnout": 4.5,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 7.0, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 5.0, "fulfillment": 6.5, "entrepreneurship": 5.5, "gender_equality": 5.0,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 5.5, "intl_mobility": 8.5, "industry_monopoly": 3.0,
            "trend_long": 4, "trend_short": 3, "edu": "本科", "age": "23-30",
        },
        "0110": {  # Low-Code/No-Code Developer
            "learning_cost": 2.5, "education_req": 2.5,
            "growth_coeff": 5.0, "career_lifespan": 4.5,
            "opportunity": 6.0, "market_size": 5.0, "supply_demand": 5.0, "developed_scarcity": 3.5,
            "value_added": 4.5, "cost_performance": 6.5,
            "stability": 4.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 6.0, "burnout": 6.0,
            "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 3.0,
            "ai_resistance": 3.0, "social_status": 4.5, "remote_friendly": 8.5, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 5.0, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 7.0, "social_interaction": 5.0, "physical_demand": 0.5, "license_barrier": 0.0,
            "cycle_sensitivity": 5.0, "side_job_compat": 7.5, "intl_mobility": 6.0, "industry_monopoly": 3.0,
            "trend_long": 2, "trend_short": 3, "edu": "大专/自学", "age": "20-35",
        },
        "0111": {  # Game Server Engineer
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 6.0, "career_lifespan": 6.0,
            "opportunity": 5.5, "market_size": 4.5, "supply_demand": 6.0, "developed_scarcity": 5.5,
            "value_added": 6.5, "cost_performance": 6.0,
            "stability": 4.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 3.5, "burnout": 4.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.5,
            "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 7.5, "autonomy": 6.0,
            "family_friendly": 4.0, "fulfillment": 7.0, "entrepreneurship": 6.0, "gender_equality": 4.5,
            "age_flexibility": 5.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 6.5, "side_job_compat": 5.5, "intl_mobility": 7.0, "industry_monopoly": 3.5,
            "trend_long": 3, "trend_short": 1, "edu": "本科", "age": "21-28",
        },
        "0112": {  # Database Administrator
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 5.0, "career_lifespan": 7.5,
            "opportunity": 5.5, "market_size": 6.5, "supply_demand": 5.0, "developed_scarcity": 5.0,
            "value_added": 6.0, "cost_performance": 6.0,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 4.5, "social_status": 5.5, "remote_friendly": 7.5, "autonomy": 6.0,
            "family_friendly": 6.0, "fulfillment": 5.5, "entrepreneurship": 5.0, "gender_equality": 5.5,
            "age_flexibility": 6.5, "social_interaction": 4.5, "physical_demand": 1.0, "license_barrier": 1.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 6.0, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": -1, "edu": "本科", "age": "22-30",
        },
        "0113": {  # Technical Support Engineer
            "learning_cost": 3.5, "education_req": 3.5,
            "growth_coeff": 4.5, "career_lifespan": 6.0,
            "opportunity": 5.5, "market_size": 7.5, "supply_demand": 4.5, "developed_scarcity": 3.5,
            "value_added": 4.5, "cost_performance": 5.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 4.0, "social_status": 4.5, "remote_friendly": 7.0, "autonomy": 5.0,
            "family_friendly": 6.0, "fulfillment": 4.5, "entrepreneurship": 4.5, "gender_equality": 5.5,
            "age_flexibility": 6.0, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 5.5, "intl_mobility": 6.5, "industry_monopoly": 2.0,
            "trend_long": 1, "trend_short": -1, "edu": "大专/本科", "age": "20-28",
        },
        # ===== AI_DATA =====
        "0201": {  # Machine Learning Engineer
            "learning_cost": 7.0, "education_req": 7.0,
            "growth_coeff": 8.5, "career_lifespan": 7.0,
            "opportunity": 8.5, "market_size": 6.0, "supply_demand": 8.5, "developed_scarcity": 8.5,
            "value_added": 9.0, "cost_performance": 8.0,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 8.0, "career_switch": 7.0, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 8.0, "remote_friendly": 8.5, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 8.0, "entrepreneurship": 7.5, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.0, "intl_mobility": 9.0, "industry_monopoly": 3.0,
            "trend_long": 5, "trend_short": 5, "edu": "硕士/博士", "age": "24-30",
        },
        "0202": {  # Data Scientist
            "learning_cost": 7.0, "education_req": 7.0,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 8.0, "market_size": 6.5, "supply_demand": 7.0, "developed_scarcity": 7.0,
            "value_added": 8.5, "cost_performance": 7.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 8.5, "career_switch": 7.0, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 7.5, "remote_friendly": 8.5, "autonomy": 7.5,
            "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 7.0, "gender_equality": 5.5,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 7.5, "intl_mobility": 8.5, "industry_monopoly": 2.5,
            "trend_long": 5, "trend_short": 3, "edu": "硕士/博士", "age": "24-30",
        },
        "0203": {  # Data Analyst
            "learning_cost": 4.5, "education_req": 4.5,
            "growth_coeff": 5.5, "career_lifespan": 7.0,
            "opportunity": 7.0, "market_size": 8.0, "supply_demand": 5.5, "developed_scarcity": 4.5,
            "value_added": 5.5, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 4.0, "social_status": 5.5, "remote_friendly": 8.0, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 5.5, "entrepreneurship": 5.5, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 7.0, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科", "age": "22-28",
        },
        "0204": {  # Data Engineer
            "learning_cost": 6.0, "education_req": 5.5,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 6.5, "supply_demand": 7.5, "developed_scarcity": 7.0,
            "value_added": 7.5, "cost_performance": 7.5,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 5.5, "social_status": 6.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.0, "gender_equality": 5.5,
            "age_flexibility": 6.0, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 6.5, "intl_mobility": 8.0, "industry_monopoly": 2.5,
            "trend_long": 4, "trend_short": 3, "edu": "本科/硕士", "age": "22-28",
        },
        "0205": {  # NLP Engineer
            "learning_cost": 7.5, "education_req": 7.5,
            "growth_coeff": 8.0, "career_lifespan": 6.5,
            "opportunity": 8.0, "market_size": 5.0, "supply_demand": 8.5, "developed_scarcity": 8.5,
            "value_added": 9.0, "cost_performance": 7.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 7.5, "remote_friendly": 8.5, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 8.0, "entrepreneurship": 7.0, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 6.5, "intl_mobility": 8.5, "industry_monopoly": 3.5,
            "trend_long": 5, "trend_short": 5, "edu": "硕士/博士", "age": "24-30",
        },
        "0206": {  # Computer Vision Engineer
            "learning_cost": 7.5, "education_req": 7.5,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 5.0, "supply_demand": 8.0, "developed_scarcity": 8.0,
            "value_added": 8.5, "cost_performance": 7.0,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.0, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 7.5, "remote_friendly": 8.0, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 7.0, "gender_equality": 4.5,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 6.5, "intl_mobility": 8.5, "industry_monopoly": 3.5,
            "trend_long": 4, "trend_short": 4, "edu": "硕士/博士", "age": "24-30",
        },
        "0207": {  # AI Research Scientist
            "learning_cost": 9.0, "education_req": 9.5,
            "growth_coeff": 8.5, "career_lifespan": 8.0,
            "opportunity": 7.5, "market_size": 3.0, "supply_demand": 9.0, "developed_scarcity": 9.5,
            "value_added": 9.5, "cost_performance": 7.0,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.0,
            "ai_resistance": 8.0, "social_status": 9.0, "remote_friendly": 8.0, "autonomy": 8.5,
            "family_friendly": 5.5, "fulfillment": 9.0, "entrepreneurship": 7.0, "gender_equality": 5.0,
            "age_flexibility": 5.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 6.0, "intl_mobility": 9.5, "industry_monopoly": 4.0,
            "trend_long": 5, "trend_short": 5, "edu": "博士", "age": "27-35",
        },
        "0208": {  # Big Data Architect
            "learning_cost": 7.0, "education_req": 6.5,
            "growth_coeff": 7.5, "career_lifespan": 7.5,
            "opportunity": 7.0, "market_size": 4.5, "supply_demand": 7.5, "developed_scarcity": 7.5,
            "value_added": 8.5, "cost_performance": 7.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 1.0,
            "ai_resistance": 6.0, "social_status": 7.5, "remote_friendly": 8.0, "autonomy": 8.0,
            "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 6.5, "gender_equality": 5.0,
            "age_flexibility": 7.0, "social_interaction": 6.0, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 6.5, "intl_mobility": 8.0, "industry_monopoly": 3.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科/硕士", "age": "27-35",
        },
        # ===== NETWORK_SECURITY =====
        "0301": {  # Network Engineer
            "learning_cost": 5.5, "education_req": 5.0,
            "growth_coeff": 5.5, "career_lifespan": 7.0,
            "opportunity": 6.0, "market_size": 7.0, "supply_demand": 5.5, "developed_scarcity": 5.0,
            "value_added": 6.0, "cost_performance": 6.0,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 5.0, "social_status": 5.5, "remote_friendly": 6.5, "autonomy": 6.0,
            "family_friendly": 5.5, "fulfillment": 5.5, "entrepreneurship": 5.0, "gender_equality": 4.5,
            "age_flexibility": 6.0, "social_interaction": 5.0, "physical_demand": 2.0, "license_barrier": 3.0,
            "cycle_sensitivity": 4.0, "side_job_compat": 5.5, "intl_mobility": 6.5, "industry_monopoly": 3.5,
            "trend_long": 2, "trend_short": 0, "edu": "本科/大专", "age": "22-28",
        },
        "0302": {  # Cybersecurity Engineer
            "learning_cost": 6.5, "education_req": 5.5,
            "growth_coeff": 8.0, "career_lifespan": 8.0,
            "opportunity": 8.0, "market_size": 6.0, "supply_demand": 8.5, "developed_scarcity": 8.5,
            "value_added": 8.0, "cost_performance": 7.5,
            "stability": 7.5, "safety": 9.0, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.0, "reputation_variance": 1.0,
            "ai_resistance": 7.5, "social_status": 7.5, "remote_friendly": 7.5, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 7.0, "gender_equality": 4.5,
            "age_flexibility": 6.5, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 3.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 7.0, "intl_mobility": 8.0, "industry_monopoly": 3.0,
            "trend_long": 5, "trend_short": 4, "edu": "本科/硕士", "age": "23-30",
        },
        "0303": {  # Penetration Tester
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 4.0, "supply_demand": 8.5, "developed_scarcity": 8.5,
            "value_added": 8.0, "cost_performance": 7.5,
            "stability": 7.0, "safety": 8.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 7.5, "social_status": 7.0, "remote_friendly": 7.5, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 7.5, "gender_equality": 4.0,
            "age_flexibility": 6.0, "social_interaction": 5.0, "physical_demand": 1.0, "license_barrier": 3.0,
            "cycle_sensitivity": 3.0, "side_job_compat": 7.5, "intl_mobility": 8.0, "industry_monopoly": 2.5,
            "trend_long": 4, "trend_short": 4, "edu": "本科/自学", "age": "22-30",
        },
        "0304": {  # Security Operations Engineer
            "learning_cost": 5.5, "education_req": 5.0,
            "growth_coeff": 6.5, "career_lifespan": 7.0,
            "opportunity": 6.5, "market_size": 5.5, "supply_demand": 7.0, "developed_scarcity": 7.0,
            "value_added": 7.0, "cost_performance": 6.5,
            "stability": 7.0, "safety": 9.0, "occupational_disease": 6.0, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 6.0, "remote_friendly": 7.0, "autonomy": 6.0,
            "family_friendly": 5.0, "fulfillment": 6.0, "entrepreneurship": 5.0, "gender_equality": 4.5,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 2.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 5.5, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 3, "trend_short": 3, "edu": "本科", "age": "22-28",
        },
        "0305": {  # Cloud Engineer
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 8.0, "career_lifespan": 7.0,
            "opportunity": 8.0, "market_size": 7.0, "supply_demand": 8.0, "developed_scarcity": 7.5,
            "value_added": 8.0, "cost_performance": 7.5,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 8.0, "career_switch": 7.0, "reputation_variance": 1.5,
            "ai_resistance": 5.5, "social_status": 7.0, "remote_friendly": 9.0, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.0, "entrepreneurship": 6.5, "gender_equality": 5.0,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 1.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.0, "intl_mobility": 8.5, "industry_monopoly": 4.0,
            "trend_long": 5, "trend_short": 4, "edu": "本科", "age": "22-30",
        },
        "0306": {  # System Administrator
            "learning_cost": 4.5, "education_req": 4.0,
            "growth_coeff": 4.5, "career_lifespan": 6.5,
            "opportunity": 5.5, "market_size": 7.5, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 4.5, "social_status": 5.0, "remote_friendly": 6.5, "autonomy": 6.0,
            "family_friendly": 5.5, "fulfillment": 5.0, "entrepreneurship": 4.5, "gender_equality": 4.5,
            "age_flexibility": 6.0, "social_interaction": 5.0, "physical_demand": 2.0, "license_barrier": 2.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 5.5, "intl_mobility": 6.0, "industry_monopoly": 2.5,
            "trend_long": 0, "trend_short": -2, "edu": "大专/本科", "age": "22-28",
        },
        # ===== PRODUCT_DESIGN =====
        "0401": {  # Product Manager
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 8.0, "career_lifespan": 7.5,
            "opportunity": 8.0, "market_size": 6.5, "supply_demand": 6.0, "developed_scarcity": 5.5,
            "value_added": 7.5, "cost_performance": 7.0,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 4.5,
            "skill_versatility": 8.0, "career_switch": 7.5, "reputation_variance": 2.5,
            "ai_resistance": 6.5, "social_status": 7.0, "remote_friendly": 8.0, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 8.5, "gender_equality": 6.0,
            "age_flexibility": 6.5, "social_interaction": 8.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 6.5, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科/硕士", "age": "24-30",
        },
        "0402": {  # UI Designer
            "learning_cost": 4.5, "education_req": 4.0,
            "growth_coeff": 5.5, "career_lifespan": 6.0,
            "opportunity": 6.0, "market_size": 6.0, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 2.0,
            "ai_resistance": 4.0, "social_status": 5.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 7.0, "gender_equality": 7.0,
            "age_flexibility": 5.5, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 6.0, "side_job_compat": 8.0, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 0, "edu": "本科/专科", "age": "20-26",
        },
        "0403": {  # UX Designer
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 6.5, "career_lifespan": 7.0,
            "opportunity": 7.0, "market_size": 5.5, "supply_demand": 5.5, "developed_scarcity": 5.5,
            "value_added": 6.5, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.0,
            "ai_resistance": 6.0, "social_status": 6.0, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 7.0, "gender_equality": 7.5,
            "age_flexibility": 6.0, "social_interaction": 7.0, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 7.5, "intl_mobility": 7.5, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 2, "edu": "本科/硕士", "age": "22-28",
        },
        "0404": {  # Interaction Designer
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 6.0, "career_lifespan": 6.5,
            "opportunity": 6.5, "market_size": 4.5, "supply_demand": 5.0, "developed_scarcity": 5.0,
            "value_added": 6.0, "cost_performance": 6.0,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 2.5,
            "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 8.0, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.5, "gender_equality": 7.0,
            "age_flexibility": 5.5, "social_interaction": 6.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 5.5, "side_job_compat": 7.0, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 1, "edu": "本科", "age": "22-28",
        },
        "0405": {  # Technical Project Manager
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 7.0, "career_lifespan": 8.0,
            "opportunity": 7.5, "market_size": 6.5, "supply_demand": 5.5, "developed_scarcity": 5.5,
            "value_added": 7.0, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 7.5, "career_switch": 7.0, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 7.0, "remote_friendly": 8.0, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 6.5, "entrepreneurship": 7.0, "gender_equality": 6.0,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 0.5, "license_barrier": 1.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 6.0, "intl_mobility": 7.5, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 1, "edu": "本科/硕士", "age": "26-35",
        },
        # ===== EMERGING_DIGITAL =====
        "0501": {  # Blockchain Developer
            "learning_cost": 6.5, "education_req": 5.5,
            "growth_coeff": 6.5, "career_lifespan": 5.0,
            "opportunity": 6.5, "market_size": 3.5, "supply_demand": 7.0, "developed_scarcity": 6.5,
            "value_added": 7.5, "cost_performance": 6.5,
            "stability": 3.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 4.0,
            "ai_resistance": 5.5, "social_status": 6.0, "remote_friendly": 9.0, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 6.5, "entrepreneurship": 9.0, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 8.0, "side_job_compat": 7.5, "intl_mobility": 8.0, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 0, "edu": "本科/自学", "age": "22-30",
        },
        "0502": {  # IoT Engineer
            "learning_cost": 6.0, "education_req": 5.5,
            "growth_coeff": 7.0, "career_lifespan": 7.0,
            "opportunity": 7.0, "market_size": 5.5, "supply_demand": 7.0, "developed_scarcity": 6.5,
            "value_added": 7.0, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.0, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 5.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 7.0, "gender_equality": 4.5,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 2.5, "license_barrier": 1.0,
            "cycle_sensitivity": 4.5, "side_job_compat": 5.5, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 4, "trend_short": 3, "edu": "本科/硕士", "age": "22-28",
        },
        "0503": {  # RPA Developer
            "learning_cost": 4.5, "education_req": 4.0,
            "growth_coeff": 5.5, "career_lifespan": 5.5,
            "opportunity": 6.0, "market_size": 5.0, "supply_demand": 6.0, "developed_scarcity": 5.5,
            "value_added": 6.0, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 3.5, "social_status": 5.5, "remote_friendly": 8.0, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 5.5, "entrepreneurship": 6.5, "gender_equality": 6.0,
            "age_flexibility": 6.5, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 7.0, "intl_mobility": 6.5, "industry_monopoly": 3.5,
            "trend_long": 3, "trend_short": 1, "edu": "本科/大专", "age": "22-30",
        },
        "0504": {  # AR/VR Developer
            "learning_cost": 6.5, "education_req": 5.5,
            "growth_coeff": 7.0, "career_lifespan": 6.0,
            "opportunity": 7.0, "market_size": 3.5, "supply_demand": 7.0, "developed_scarcity": 6.5,
            "value_added": 7.0, "cost_performance": 6.0,
            "stability": 4.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.0, "reputation_variance": 3.0,
            "ai_resistance": 6.0, "social_status": 6.5, "remote_friendly": 7.0, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 7.5, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 5.5, "physical_demand": 1.5, "license_barrier": 0.5,
            "cycle_sensitivity": 7.0, "side_job_compat": 6.5, "intl_mobility": 7.5, "industry_monopoly": 3.5,
            "trend_long": 3, "trend_short": 2, "edu": "本科/硕士", "age": "22-28",
        },
        "0505": {  # Quantum Computing Researcher
            "learning_cost": 9.5, "education_req": 9.5,
            "growth_coeff": 7.0, "career_lifespan": 8.0,
            "opportunity": 5.0, "market_size": 1.5, "supply_demand": 9.0, "developed_scarcity": 9.5,
            "value_added": 9.0, "cost_performance": 5.5,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 7.5, "overtime": 5.0, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.0,
            "ai_resistance": 8.5, "social_status": 9.0, "remote_friendly": 7.0, "autonomy": 8.5,
            "family_friendly": 5.5, "fulfillment": 9.0, "entrepreneurship": 5.0, "gender_equality": 4.5,
            "age_flexibility": 4.5, "social_interaction": 5.0, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 4.0, "intl_mobility": 9.0, "industry_monopoly": 5.0,
            "trend_long": 3, "trend_short": 4, "edu": "博士", "age": "27-35",
        },
        "0506": {  # AI Prompt Engineer
            "learning_cost": 3.0, "education_req": 3.5,
            "growth_coeff": 5.0, "career_lifespan": 3.5,
            "opportunity": 7.0, "market_size": 4.0, "supply_demand": 6.0, "developed_scarcity": 5.0,
            "value_added": 6.0, "cost_performance": 7.5,
            "stability": 3.5, "safety": 9.5, "occupational_disease": 7.5, "overtime": 6.0, "burnout": 5.5,
            "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 3.5,
            "ai_resistance": 3.0, "social_status": 5.0, "remote_friendly": 9.5, "autonomy": 7.0,
            "family_friendly": 6.5, "fulfillment": 5.5, "entrepreneurship": 7.5, "gender_equality": 7.0,
            "age_flexibility": 7.5, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 0.0,
            "cycle_sensitivity": 6.5, "side_job_compat": 8.5, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 2, "trend_short": 4, "edu": "本科/自学", "age": "20-35",
        },
        "0507": {  # Data Annotator
            "learning_cost": 1.5, "education_req": 1.5,
            "growth_coeff": 2.5, "career_lifespan": 3.5,
            "opportunity": 4.0, "market_size": 5.5, "supply_demand": 4.0, "developed_scarcity": 2.0,
            "value_added": 2.5, "cost_performance": 4.0,
            "stability": 3.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.0, "burnout": 4.0,
            "skill_versatility": 3.5, "career_switch": 4.0, "reputation_variance": 3.0,
            "ai_resistance": 2.0, "social_status": 3.0, "remote_friendly": 8.5, "autonomy": 3.5,
            "family_friendly": 6.0, "fulfillment": 3.0, "entrepreneurship": 3.0, "gender_equality": 7.0,
            "age_flexibility": 8.0, "social_interaction": 3.5, "physical_demand": 1.0, "license_barrier": 0.0,
            "cycle_sensitivity": 5.5, "side_job_compat": 7.5, "intl_mobility": 4.5, "industry_monopoly": 3.0,
            "trend_long": 2, "trend_short": 1, "edu": "高中/大专", "age": "18-40",
        },
        "0508": {  # Digital Twin Engineer
            "learning_cost": 7.0, "education_req": 6.5,
            "growth_coeff": 7.0, "career_lifespan": 7.0,
            "opportunity": 7.0, "market_size": 3.0, "supply_demand": 7.5, "developed_scarcity": 7.5,
            "value_added": 7.5, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 6.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 6.0, "gender_equality": 4.5,
            "age_flexibility": 5.5, "social_interaction": 5.5, "physical_demand": 1.5, "license_barrier": 1.0,
            "cycle_sensitivity": 4.5, "side_job_compat": 5.0, "intl_mobility": 7.5, "industry_monopoly": 3.5,
            "trend_long": 3, "trend_short": 4, "edu": "本科/硕士", "age": "24-30",
        },
        "0509": {  # Edge Computing Engineer
            "learning_cost": 6.5, "education_req": 6.0,
            "growth_coeff": 7.0, "career_lifespan": 6.5,
            "opportunity": 6.5, "market_size": 3.5, "supply_demand": 7.5, "developed_scarcity": 7.0,
            "value_added": 7.5, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 6.0, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.0, "gender_equality": 4.5,
            "age_flexibility": 5.5, "social_interaction": 5.0, "physical_demand": 2.0, "license_barrier": 1.0,
            "cycle_sensitivity": 4.5, "side_job_compat": 5.0, "intl_mobility": 7.5, "industry_monopoly": 3.5,
            "trend_long": 3, "trend_short": 4, "edu": "本科/硕士", "age": "23-30",
        },
        "0510": {  # Web3 Developer
            "learning_cost": 6.0, "education_req": 5.0,
            "growth_coeff": 6.0, "career_lifespan": 4.5,
            "opportunity": 6.5, "market_size": 3.0, "supply_demand": 6.5, "developed_scarcity": 6.0,
            "value_added": 7.0, "cost_performance": 6.0,
            "stability": 3.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 4.5,
            "ai_resistance": 5.0, "social_status": 5.5, "remote_friendly": 9.5, "autonomy": 8.0,
            "family_friendly": 5.5, "fulfillment": 6.0, "entrepreneurship": 9.0, "gender_equality": 5.0,
            "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 8.5, "side_job_compat": 7.5, "intl_mobility": 8.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": -1, "edu": "本科/自学", "age": "22-30",
        },
        "0511": {  # AI Safety Researcher
            "learning_cost": 8.5, "education_req": 9.0,
            "growth_coeff": 8.0, "career_lifespan": 8.0,
            "opportunity": 7.0, "market_size": 2.0, "supply_demand": 9.0, "developed_scarcity": 9.5,
            "value_added": 9.0, "cost_performance": 7.0,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 7.5, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 8.5, "social_status": 8.5, "remote_friendly": 8.0, "autonomy": 8.5,
            "family_friendly": 5.5, "fulfillment": 9.0, "entrepreneurship": 5.5, "gender_equality": 5.0,
            "age_flexibility": 5.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 5.5, "intl_mobility": 9.0, "industry_monopoly": 4.0,
            "trend_long": 3, "trend_short": 5, "edu": "博士", "age": "27-35",
        },
        "0512": {  # MLOps Engineer
            "learning_cost": 6.5, "education_req": 5.5,
            "growth_coeff": 8.0, "career_lifespan": 6.5,
            "opportunity": 7.5, "market_size": 4.5, "supply_demand": 8.5, "developed_scarcity": 8.0,
            "value_added": 8.0, "cost_performance": 7.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 5.0,
            "skill_versatility": 7.5, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 7.0, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.0, "entrepreneurship": 6.5, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 5.5, "physical_demand": 1.0, "license_barrier": 0.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 6.5, "intl_mobility": 8.5, "industry_monopoly": 3.0,
            "trend_long": 4, "trend_short": 5, "edu": "本科/硕士", "age": "23-30",
        },
        "0513": {  # Synthetic Data Engineer
            "learning_cost": 7.0, "education_req": 6.5,
            "growth_coeff": 7.0, "career_lifespan": 6.0,
            "opportunity": 6.5, "market_size": 2.5, "supply_demand": 7.5, "developed_scarcity": 7.5,
            "value_added": 7.5, "cost_performance": 6.5,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 5.5, "social_status": 6.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.5, "gender_equality": 5.0,
            "age_flexibility": 5.5, "social_interaction": 4.5, "physical_demand": 0.5, "license_barrier": 0.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 6.0, "intl_mobility": 8.0, "industry_monopoly": 3.5,
            "trend_long": 2, "trend_short": 4, "edu": "硕士/博士", "age": "24-30",
        },
        "0514": {  # Digital Accessibility Specialist
            "learning_cost": 4.0, "education_req": 4.0,
            "growth_coeff": 5.5, "career_lifespan": 7.0,
            "opportunity": 6.0, "market_size": 3.5, "supply_demand": 6.5, "developed_scarcity": 6.5,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 7.0, "overtime": 6.5, "burnout": 6.0,
            "skill_versatility": 5.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 8.5, "autonomy": 6.5,
            "family_friendly": 7.0, "fulfillment": 7.5, "entrepreneurship": 5.5, "gender_equality": 7.5,
            "age_flexibility": 7.0, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 7.0, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 3, "edu": "本科", "age": "22-30",
        },
    }
    return bases.get(occ_id, {})


# ---------------------------------------------------------------------------
# COUNTRY-ADAPTIVE SCORING FUNCTIONS
# ---------------------------------------------------------------------------

def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))

def apply_country_modifiers(base_scores, country_profile, occ_id):
    """Adjust base scores based on country profile. Returns new dict of scores."""
    cp = country_profile
    s = dict(base_scores)  # copy

    # Tech maturity influences many dimensions
    tech_factor = (cp["tech"] - 6.0) / 4.0  # -1.0 to +1.0 range

    # Compensation / value-added: strongly affected by country compensation levels
    comp_factor = (cp["comp"] - 5.5) / 4.5  # normalized
    s["value_added"] = clamp(s["value_added"] + comp_factor * 2.0)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_factor * 1.0 + tech_factor * 0.5)

    # Growth coefficient: tech maturity + market dynamism
    s["growth_coeff"] = clamp(s["growth_coeff"] + tech_factor * 0.8 + (cp["market"] - 6.0) / 8.0)

    # Career lifespan: slightly longer in developed, stable markets
    stab_factor = (cp["stab"] - 5.5) / 4.5
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_factor * 0.8)

    # Opportunity: bigger in larger, more dynamic markets
    market_factor = (cp["market"] - 6.0) / 4.0
    s["opportunity"] = clamp(s["opportunity"] + market_factor * 1.0 + tech_factor * 0.5)

    # Market size: directly related to country market size
    s["market_size"] = clamp(s["market_size"] + market_factor * 1.5)

    # Supply-demand: higher in developed markets with strong tech sectors
    s["supply_demand"] = clamp(s["supply_demand"] + tech_factor * 1.0)

    # Developed scarcity: higher in developed countries with talent gaps
    dev_bonus = 1.0 if cp["tech"] >= 7.5 else (0.0 if cp["tech"] >= 5.0 else -1.0)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus * 0.8)

    # Stability: affected by country economic stability
    s["stability"] = clamp(s["stability"] + stab_factor * 1.5)

    # Safety: generally high for tech, slight variation
    s["safety"] = clamp(s["safety"] + stab_factor * 0.2)

    # Occupational disease: worse in countries with poor work-life balance
    wlb_factor = (cp["wlb"] - 6.0) / 4.0
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_factor * 0.8)

    # Overtime: strongly affected by work culture
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)

    # Burnout: overtime culture + tech intensity
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)

    # Remote friendly: country remote culture
    remote_factor = (cp["remote"] - 6.5) / 3.5
    s["remote_friendly"] = clamp(s["remote_friendly"] + remote_factor * 1.5)

    # Autonomy: related to workplace culture
    s["autonomy"] = clamp(s["autonomy"] + wlb_factor * 0.5 + remote_factor * 0.3)

    # Family friendly: work-life balance culture
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_factor * 1.5)

    # Social status: higher in tech-focused developed economies
    s["social_status"] = clamp(s["social_status"] + tech_factor * 0.8 + comp_factor * 0.5)

    # Fulfillment: slightly better in more innovative environments
    s["fulfillment"] = clamp(s["fulfillment"] + tech_factor * 0.5)

    # Gender equality: country-level gender equality
    gender_factor = (cp["gender"] - 5.5) / 4.5
    s["gender_equality"] = clamp(s["gender_equality"] + gender_factor * 2.0)

    # Age flexibility: better in more mature, inclusive markets
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_factor * 0.5 + tech_factor * 0.3)

    # Entrepreneurship: market dynamism + regulatory environment
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + market_factor * 0.5 + (cp["reg"] - 5.5) / 4.5 * 0.5)

    # International mobility: country openness
    intl_factor = (cp["intl"] - 6.0) / 4.0
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_factor * 1.5)

    # AI resistance: doesn't change much by country, slight boost for AI-advanced nations
    ai_factor = (cp["ai"] - 6.0) / 4.0
    s["ai_resistance"] = clamp(s["ai_resistance"] + ai_factor * 0.3)

    # Learning cost and education req: slightly higher in countries with formal education requirements
    edu_factor = (cp["edu"] - 6.0) / 4.0
    s["learning_cost"] = clamp(s["learning_cost"] + edu_factor * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_factor * 0.3)

    # License barrier: slightly higher in more regulated environments
    reg_factor = (cp["reg"] - 5.5) / 4.5
    s["license_barrier"] = clamp(s["license_barrier"] + reg_factor * 0.5)

    # Cycle sensitivity: slightly higher in volatile economies
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_factor * 0.5)

    # Side job compatibility: remote culture + market openness
    s["side_job_compat"] = clamp(s["side_job_compat"] + remote_factor * 0.5)

    # Industry monopoly: higher in less competitive markets
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - market_factor * 0.3 + (1 - cp["reg"] / 10.0) * 0.3)

    # Skill versatility: slightly better in mature tech ecosystems
    s["skill_versatility"] = clamp(s["skill_versatility"] + tech_factor * 0.5)

    # Career switch: easier in dynamic, large markets
    s["career_switch"] = clamp(s["career_switch"] + market_factor * 0.5 + tech_factor * 0.3)

    # Reputation variance: slightly higher in emerging markets
    rep_adj = -0.3 if cp["tech"] >= 7.5 else (0.3 if cp["tech"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # Social interaction: doesn't vary much by country
    # Physical demand: doesn't vary much by country

    return s


def get_trends(base_scores, country_profile):
    """Get trend values adjusted for country."""
    cp = country_profile
    t_long = base_scores["trend_long"]
    t_short = base_scores["trend_short"]

    # Adjust slightly based on country tech trajectory
    if cp["ai"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["ai"] < 4.0:
        t_short = max(-5, t_short - 1)

    if cp["tech"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["tech"] < 5.0:
        t_long = max(-5, t_long - 1)

    return t_long, t_short


def get_demand_direction(trend_5yr):
    """Map 5yr trend to demand direction arrow."""
    if trend_5yr >= 4:
        return "↑↑"
    elif trend_5yr >= 2:
        return "↑"
    elif trend_5yr >= -1:
        return "→"
    elif trend_5yr >= -3:
        return "↓"
    else:
        return "↓↓"


def get_ai_timeline(occ_id, ai_resistance):
    """Estimate AI impact timeline based on occupation and resistance."""
    # High resistance occupations
    if ai_resistance >= 7.5:
        return "2035+"
    elif ai_resistance >= 6.0:
        return "2032-2038"
    elif ai_resistance >= 4.5:
        return "2028-2033"
    elif ai_resistance >= 3.0:
        return "2026-2030"
    else:
        return "2025-2028"


def generate_summary(occ, country, scores, trend_5yr, ai_resistance):
    """Generate Chinese and English summaries."""
    occ_zh = occ["zh"]
    country_zh = country["name_zh"]
    country_en = country["name_en"]
    occ_en = occ["en"]

    # Pick 2-3 highlights
    highlights_zh = []
    highlights_en = []

    if scores["value_added"] >= 8.0:
        highlights_zh.append("薪资回报高")
        highlights_en.append("high compensation")
    elif scores["value_added"] <= 4.5:
        highlights_zh.append("薪资水平偏低")
        highlights_en.append("relatively low pay")

    if scores["supply_demand"] >= 7.5:
        highlights_zh.append("人才需求旺盛")
        highlights_en.append("strong talent demand")
    elif scores["supply_demand"] <= 4.0:
        highlights_zh.append("供过于求")
        highlights_en.append("oversupply of talent")

    if scores["ai_resistance"] <= 4.0:
        highlights_zh.append("AI替代风险较高")
        highlights_en.append("high AI displacement risk")
    elif scores["ai_resistance"] >= 7.5:
        highlights_zh.append("AI替代抗性强")
        highlights_en.append("strong AI resistance")

    if scores["remote_friendly"] >= 8.5:
        highlights_zh.append("远程友好度高")
        highlights_en.append("highly remote-friendly")

    if scores["overtime"] <= 3.5:
        highlights_zh.append("加班文化严重")
        highlights_en.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5:
        highlights_zh.append("工作时间规律")
        highlights_en.append("regular working hours")

    if scores["stability"] >= 7.5:
        highlights_zh.append("就业稳定")
        highlights_en.append("stable employment")
    elif scores["stability"] <= 4.0:
        highlights_zh.append("就业波动大")
        highlights_en.append("volatile employment")

    if trend_5yr >= 4:
        highlights_zh.append("近年增长迅猛")
        highlights_en.append("rapid recent growth")
    elif trend_5yr <= -2:
        highlights_zh.append("近年需求下降")
        highlights_en.append("declining demand")

    # Take top 3
    highlights_zh = highlights_zh[:3]
    highlights_en = highlights_en[:3]

    if not highlights_zh:
        highlights_zh = ["发展平稳"]
        highlights_en = ["steady development"]

    zh = f"{country_zh}{occ_zh}：{'，'.join(highlights_zh)}"
    en = f"{country_en} {occ_en}: {', '.join(highlights_en)}"

    return zh, en


# ---------------------------------------------------------------------------
# MAIN GENERATION
# ---------------------------------------------------------------------------

HEADERS = [
    "id", "major_category", "major_code", "mid_category", "sub_category",
    "sub_category_en", "isco_code", "onet_code", "region", "country_or_region",
    "iso_code", "type", "employer_type", "typical_education", "typical_entry_age",
    "locality", "learning_cost", "education_req", "growth_coeff", "career_lifespan",
    "opportunity", "market_size", "supply_demand", "developed_scarcity",
    "value_added", "cost_performance", "stability", "safety", "occupational_disease",
    "overtime", "burnout", "skill_versatility", "career_switch", "reputation_variance",
    "ai_resistance", "social_status", "remote_friendly", "autonomy", "family_friendly",
    "fulfillment", "entrepreneurship", "gender_equality", "age_flexibility",
    "social_interaction", "physical_demand", "license_barrier", "cycle_sensitivity",
    "side_job_compat", "intl_mobility", "industry_monopoly", "trend_2000_2026",
    "trend_5yr", "demand_direction", "ai_timeline", "composite_index",
    "summary_zh", "summary_en", "data_source"
]

SCORE_DIMS = [
    "learning_cost", "education_req", "growth_coeff", "career_lifespan",
    "opportunity", "market_size", "supply_demand", "developed_scarcity",
    "value_added", "cost_performance", "stability", "safety", "occupational_disease",
    "overtime", "burnout", "skill_versatility", "career_switch", "reputation_variance",
    "ai_resistance", "social_status", "remote_friendly", "autonomy", "family_friendly",
    "fulfillment", "entrepreneurship", "gender_equality", "age_flexibility",
    "social_interaction", "physical_demand", "license_barrier", "cycle_sensitivity",
    "side_job_compat", "intl_mobility", "industry_monopoly"
]


def main():
    random.seed(42)  # Reproducible

    weights = load_weights()
    output_path = PROJECT_ROOT / "data" / "csv" / "tech_digital.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for occ in OCCUPATIONS:
        base = occ_base(occ["id"])
        if not base:
            print(f"WARNING: No base scores for {occ['id']} ({occ['en']}), skipping")
            continue

        for country in COUNTRIES:
            iso = country["iso"]
            cp = COUNTRY_PROFILES[iso]

            # Apply country modifiers
            scores = apply_country_modifiers(base, cp, occ["id"])

            # Add small per-row noise for realism (seed ensures reproducibility)
            noise_seed = hash(f"{occ['id']}-{iso}") % 10000
            rng = random.Random(noise_seed)
            for dim in SCORE_DIMS:
                if dim == "reputation_variance":
                    scores[dim] = clamp5(scores[dim] + rng.uniform(-0.2, 0.2))
                elif dim in ("safety",):
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.1, 0.1))
                else:
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.3, 0.3))

            # Get trends
            trend_long, trend_short = get_trends(base, cp)
            demand_dir = get_demand_direction(trend_short)
            ai_tl = get_ai_timeline(occ["id"], scores["ai_resistance"])

            # Calculate composite
            score_dict = {dim: scores[dim] for dim in weights}
            composite = calculate_composite(score_dict, weights)

            # Generate summaries
            summary_zh, summary_en = generate_summary(occ, country, scores, trend_short, scores["ai_resistance"])

            # Build ID: TECH-{occ_id}-{ISO}-general
            row_id = f"TECH-{occ['id']}-{iso}-general"

            row = {
                "id": row_id,
                "major_category": "信息技术与数字化",
                "major_code": "TECH",
                "mid_category": occ["mid_zh"],
                "sub_category": occ["zh"],
                "sub_category_en": occ["en"],
                "isco_code": occ["isco"],
                "onet_code": occ["onet"],
                "region": country["region"],
                "country_or_region": country["name_zh"],
                "iso_code": iso,
                "type": country["type"],
                "employer_type": "general",
                "typical_education": base.get("edu", "本科"),
                "typical_entry_age": base.get("age", "22-28"),
                "locality": occ["locality"],
            }

            # Add all score dimensions
            for dim in SCORE_DIMS:
                row[dim] = scores[dim]

            row["trend_2000_2026"] = trend_long
            row["trend_5yr"] = trend_short
            row["demand_direction"] = demand_dir
            row["ai_timeline"] = ai_tl
            row["composite_index"] = composite
            row["summary_zh"] = summary_zh
            row["summary_en"] = summary_en
            row["data_source"] = "AI综合评估 + O*NET/ILO/OECD锚点校准"

            rows.append(row)

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows to {output_path}")
    print(f"Occupations: {len(OCCUPATIONS)}")
    print(f"Countries: {len(COUNTRIES)}")


if __name__ == "__main__":
    main()
