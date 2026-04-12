#!/usr/bin/env python3
"""Generate education_academia.csv — EDU pilot data for Global Career Development Index.

Creates scored data for all EDU occupations across all 45 countries/regions.
Uses realistic, country-differentiated scoring based on global education labor market knowledge.
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
# OCCUPATION DEFINITIONS (from categories.yaml EDU section)
# ---------------------------------------------------------------------------

OCCUPATIONS = [
    # k12_education
    {"id": "0101", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "小学教师", "en": "Elementary School Teacher", "isco": "2341", "onet": "25-2021.00", "locality": "global"},
    {"id": "0102", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "中学教师", "en": "Secondary School Teacher", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0103", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "特殊教育教师", "en": "Special Education Teacher", "isco": "2352", "onet": "25-2054.00", "locality": "global"},
    {"id": "0104", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "学校心理咨询师", "en": "School Counselor", "isco": "2634", "onet": "21-1012.00", "locality": "global"},
    {"id": "0105", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "国际学校教师", "en": "International School Teacher", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0106", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "体育教师", "en": "Physical Education Teacher", "isco": "2342", "onet": "25-2059.01", "locality": "global"},
    {"id": "0107", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "音乐教师", "en": "Music Teacher", "isco": "2354", "onet": "25-1121.00", "locality": "global"},
    {"id": "0108", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "美术教师", "en": "Art Teacher", "isco": "2354", "onet": "25-1121.00", "locality": "global"},
    {"id": "0109", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "高中数学教师", "en": "High School Math Teacher", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0110", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "信息技术教师", "en": "IT / Computer Science Teacher", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0111", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "外语教师(K12)", "en": "Foreign Language Teacher (K-12)", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0112", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "科学教师", "en": "Science Teacher", "isco": "2330", "onet": "25-2031.00", "locality": "global"},
    {"id": "0113", "mid": "k12_education", "mid_zh": "K12教育", "mid_en": "K-12 Education",
     "zh": "图书馆教师/媒体专员", "en": "School Library Media Specialist", "isco": "2622", "onet": "25-4022.00", "locality": "global"},
    # higher_education
    {"id": "0201", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "大学教授", "en": "University Professor", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    {"id": "0202", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "大学讲师", "en": "University Lecturer", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    {"id": "0203", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "博士后研究员", "en": "Postdoctoral Researcher", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    {"id": "0204", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "助教", "en": "Teaching Assistant", "isco": "2310", "onet": "25-1191.00", "locality": "global"},
    {"id": "0205", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "大学招生官", "en": "University Admissions Officer", "isco": "2424", "onet": "11-9033.00", "locality": "global"},
    {"id": "0206", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "终身教职教授", "en": "Tenured Professor", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    {"id": "0207", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "学术顾问/导师", "en": "Academic Advisor", "isco": "2424", "onet": "21-1012.00", "locality": "global"},
    {"id": "0208", "mid": "higher_education", "mid_zh": "高等教育", "mid_en": "Higher Education",
     "zh": "大学兼职讲师/客座教授", "en": "Adjunct / Visiting Professor", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    # vocational_training
    {"id": "0301", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "企业培训师", "en": "Corporate Trainer", "isco": "2424", "onet": "13-1151.00", "locality": "global"},
    {"id": "0302", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "职业认证讲师", "en": "Certification Instructor", "isco": "2320", "onet": "25-1194.00", "locality": "global"},
    {"id": "0303", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "职业技术教师", "en": "Vocational Education Teacher", "isco": "2320", "onet": "25-1194.00", "locality": "global"},
    {"id": "0304", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "驾校教练", "en": "Driving Instructor", "isco": "5165", "onet": "25-3021.00", "locality": "global"},
    {"id": "0305", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "语言培训教师", "en": "Language Training Teacher", "isco": "2353", "onet": "25-3011.00", "locality": "global"},
    {"id": "0306", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "飞行教官", "en": "Flight Instructor", "isco": "3153", "onet": "25-3021.00", "locality": "global"},
    {"id": "0307", "mid": "vocational_training", "mid_zh": "职业培训", "mid_en": "Vocational Training",
     "zh": "礼仪培训师", "en": "Etiquette Trainer", "isco": "2424", "onet": "13-1151.00", "locality": "global"},
    # online_education
    {"id": "0401", "mid": "online_education", "mid_zh": "在线教育", "mid_en": "Online Education",
     "zh": "在线课程设计师", "en": "Online Course Designer", "isco": "2424", "onet": "25-9031.00", "locality": "global"},
    {"id": "0402", "mid": "online_education", "mid_zh": "在线教育", "mid_en": "Online Education",
     "zh": "教育科技产品经理", "en": "EdTech Product Manager", "isco": "2511", "onet": "15-1299.09", "locality": "global"},
    {"id": "0403", "mid": "online_education", "mid_zh": "在线教育", "mid_en": "Online Education",
     "zh": "MOOC讲师", "en": "MOOC Instructor", "isco": "2310", "onet": "25-1099.00", "locality": "global"},
    {"id": "0404", "mid": "online_education", "mid_zh": "在线教育", "mid_en": "Online Education",
     "zh": "教学设计师", "en": "Instructional Designer", "isco": "2424", "onet": "25-9031.00", "locality": "global"},
    {"id": "0405", "mid": "online_education", "mid_zh": "在线教育", "mid_en": "Online Education",
     "zh": "在线教育运营", "en": "Online Education Operations Manager", "isco": "1345", "onet": "11-9033.00", "locality": "global"},
    # academic_research
    {"id": "0501", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "自然科学研究员", "en": "Natural Science Researcher", "isco": "2110", "onet": "19-2099.00", "locality": "global"},
    {"id": "0502", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "社会科学研究员", "en": "Social Science Researcher", "isco": "2632", "onet": "19-3099.00", "locality": "global"},
    {"id": "0503", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "人文学科研究员", "en": "Humanities Researcher", "isco": "2633", "onet": "25-1126.00", "locality": "global"},
    {"id": "0504", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "实验室主任", "en": "Laboratory Director", "isco": "1223", "onet": "11-9121.01", "locality": "global"},
    {"id": "0505", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "研究助理", "en": "Research Assistant", "isco": "2110", "onet": "19-4099.00", "locality": "global"},
    {"id": "0506", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "学术期刊编辑", "en": "Academic Journal Editor", "isco": "2641", "onet": "27-3041.00", "locality": "global"},
    {"id": "0507", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "科研基金管理员", "en": "Research Grants Administrator", "isco": "2422", "onet": "11-9199.00", "locality": "global"},
    {"id": "0508", "mid": "academic_research", "mid_zh": "学术研究", "mid_en": "Academic Research",
     "zh": "科学传播者/科普作家", "en": "Science Communicator", "isco": "2641", "onet": "27-3043.00", "locality": "global"},
    # education_admin
    {"id": "0601", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "校长(中小学)", "en": "School Principal", "isco": "1345", "onet": "11-9032.00", "locality": "global"},
    {"id": "0602", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "教务主任", "en": "Academic Dean", "isco": "1345", "onet": "11-9033.00", "locality": "global"},
    {"id": "0603", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "教育政策研究员", "en": "Education Policy Researcher", "isco": "2632", "onet": "19-3099.00", "locality": "global"},
    {"id": "0604", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "大学校长", "en": "University President", "isco": "1120", "onet": "11-9033.00", "locality": "global"},
    {"id": "0605", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "教育督导", "en": "Education Inspector / Superintendent", "isco": "1345", "onet": "11-9032.00", "locality": "global"},
    {"id": "0606", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "招生主任", "en": "Director of Admissions", "isco": "1345", "onet": "11-9033.00", "locality": "global"},
    {"id": "0607", "mid": "education_admin", "mid_zh": "教育管理", "mid_en": "Education Administration",
     "zh": "学生事务主任", "en": "Dean of Students", "isco": "1345", "onet": "11-9033.00", "locality": "global"},
    # early_childhood
    {"id": "0701", "mid": "early_childhood", "mid_zh": "早期教育", "mid_en": "Early Childhood Education",
     "zh": "幼儿园教师", "en": "Kindergarten Teacher", "isco": "2342", "onet": "25-2012.00", "locality": "global"},
    {"id": "0702", "mid": "early_childhood", "mid_zh": "早期教育", "mid_en": "Early Childhood Education",
     "zh": "蒙特梭利教师", "en": "Montessori Teacher", "isco": "2342", "onet": "25-2011.00", "locality": "global"},
    {"id": "0703", "mid": "early_childhood", "mid_zh": "早期教育", "mid_en": "Early Childhood Education",
     "zh": "育婴师", "en": "Infant Care Specialist / Nanny", "isco": "5311", "onet": "39-9011.00", "locality": "global"},
    {"id": "0704", "mid": "early_childhood", "mid_zh": "早期教育", "mid_en": "Early Childhood Education",
     "zh": "早教中心教师", "en": "Early Childhood Center Teacher", "isco": "2342", "onet": "25-2011.00", "locality": "global"},
    {"id": "0705", "mid": "early_childhood", "mid_zh": "早期教育", "mid_en": "Early Childhood Education",
     "zh": "儿童发展评估师", "en": "Child Development Assessor", "isco": "2634", "onet": "21-1012.00", "locality": "global"},
    # special_education (special ed & support)
    {"id": "0801", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "学习障碍辅导师", "en": "Learning Disability Specialist", "isco": "2352", "onet": "25-2054.00", "locality": "global"},
    {"id": "0802", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "教育心理学家", "en": "Educational Psychologist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    {"id": "0803", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "手语教师/翻译", "en": "Sign Language Teacher/Interpreter", "isco": "2352", "onet": "27-3091.00", "locality": "global"},
    {"id": "0804", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "课后辅导教师/补习教师", "en": "After-school Tutor", "isco": "2353", "onet": "25-3098.00", "locality": "global"},
    {"id": "0805", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "STEM教育专家", "en": "STEM Education Specialist", "isco": "2424", "onet": "25-9031.00", "locality": "global"},
    {"id": "0806", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "留学顾问", "en": "Study Abroad Counselor / Education Agent", "isco": "2424", "onet": "21-1012.00", "locality": "global"},
    {"id": "0807", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "考试出题人/评分员", "en": "Test Developer / Exam Grader", "isco": "2310", "onet": "25-9031.00", "locality": "global"},
    {"id": "0808", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "教育数据分析师", "en": "Education Data Analyst", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "0809", "mid": "special_education", "mid_zh": "特殊教育与辅助", "mid_en": "Special Education & Support",
     "zh": "图书管理员(学校)", "en": "School Librarian", "isco": "2622", "onet": "25-4022.00", "locality": "global"},
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
# COUNTRY PROFILES — education-sector-specific modifiers
# Dimensions:
#   edu_quality: education system quality/PISA-like rank
#   teacher_pay: teacher compensation relative to national average
#   teacher_respect: teacher social status / prestige
#   edu_invest: public education investment as % of GDP
#   higher_ed: higher education quality (research output, university rankings)
#   edtech: EdTech adoption / online education maturity
#   pub_sector: public sector strength for education jobs
#   comp: overall compensation level
#   wlb: work-life balance
#   ot: overtime culture (10=no overtime, low=lots of overtime)
#   gender: gender equality
#   intl: international openness
#   reg: regulatory environment
#   student_pop: student population scale/growth (demand driver)
#   research_fund: research funding level
# ---------------------------------------------------------------------------

COUNTRY_PROFILES = {
    # --- NORDIC (teachers highly respected, well-paid, strong public sector) ---
    "FI": {"edu_quality": 9.5, "teacher_pay": 8.0, "teacher_respect": 9.5, "edu_invest": 9.0,
            "higher_ed": 8.5, "edtech": 8.0, "pub_sector": 9.0,
            "comp": 6.5, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "intl": 8.0,
            "reg": 7.0, "student_pop": 3.5, "research_fund": 7.5},
    "SE": {"edu_quality": 8.0, "teacher_pay": 7.5, "teacher_respect": 8.5, "edu_invest": 8.5,
            "higher_ed": 8.5, "edtech": 8.0, "pub_sector": 8.5,
            "comp": 7.0, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "intl": 8.5,
            "reg": 7.0, "student_pop": 4.0, "research_fund": 8.0},
    "DK": {"edu_quality": 8.0, "teacher_pay": 8.0, "teacher_respect": 8.5, "edu_invest": 8.5,
            "higher_ed": 8.0, "edtech": 7.5, "pub_sector": 8.5,
            "comp": 7.0, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "intl": 8.5,
            "reg": 7.0, "student_pop": 3.5, "research_fund": 7.5},
    # --- WESTERN EUROPE ---
    "GB": {"edu_quality": 8.0, "teacher_pay": 6.0, "teacher_respect": 6.5, "edu_invest": 7.0,
            "higher_ed": 9.5, "edtech": 8.5, "pub_sector": 7.0,
            "comp": 7.5, "wlb": 7.0, "ot": 6.0, "gender": 7.5, "intl": 9.0,
            "reg": 7.0, "student_pop": 6.5, "research_fund": 8.5},
    "DE": {"edu_quality": 8.0, "teacher_pay": 8.0, "teacher_respect": 7.5, "edu_invest": 7.0,
            "higher_ed": 8.5, "edtech": 6.5, "pub_sector": 8.5,
            "comp": 7.5, "wlb": 8.0, "ot": 7.5, "gender": 7.0, "intl": 8.0,
            "reg": 7.5, "student_pop": 5.0, "research_fund": 8.5},
    "FR": {"edu_quality": 7.5, "teacher_pay": 5.5, "teacher_respect": 6.0, "edu_invest": 7.5,
            "higher_ed": 8.0, "edtech": 6.5, "pub_sector": 8.0,
            "comp": 6.5, "wlb": 8.0, "ot": 7.0, "gender": 7.0, "intl": 7.5,
            "reg": 7.5, "student_pop": 5.5, "research_fund": 7.5},
    "NL": {"edu_quality": 8.5, "teacher_pay": 7.0, "teacher_respect": 7.5, "edu_invest": 7.5,
            "higher_ed": 8.5, "edtech": 8.0, "pub_sector": 7.5,
            "comp": 7.5, "wlb": 9.0, "ot": 8.0, "gender": 8.5, "intl": 9.0,
            "reg": 7.0, "student_pop": 4.5, "research_fund": 8.0},
    "CH": {"edu_quality": 8.5, "teacher_pay": 9.0, "teacher_respect": 8.0, "edu_invest": 7.5,
            "higher_ed": 9.5, "edtech": 7.0, "pub_sector": 7.5,
            "comp": 9.0, "wlb": 8.5, "ot": 7.0, "gender": 7.0, "intl": 8.5,
            "reg": 7.0, "student_pop": 3.5, "research_fund": 9.5},
    # --- SOUTHERN EUROPE ---
    "IT": {"edu_quality": 6.5, "teacher_pay": 5.0, "teacher_respect": 5.5, "edu_invest": 5.5,
            "higher_ed": 7.0, "edtech": 5.5, "pub_sector": 7.5,
            "comp": 5.5, "wlb": 6.5, "ot": 5.5, "gender": 5.5, "intl": 6.5,
            "reg": 6.0, "student_pop": 4.5, "research_fund": 6.0},
    "ES": {"edu_quality": 6.5, "teacher_pay": 6.0, "teacher_respect": 6.0, "edu_invest": 6.0,
            "higher_ed": 7.0, "edtech": 6.0, "pub_sector": 7.0,
            "comp": 5.0, "wlb": 7.0, "ot": 5.5, "gender": 6.5, "intl": 7.0,
            "reg": 6.0, "student_pop": 4.5, "research_fund": 6.0},
    "PT": {"edu_quality": 6.5, "teacher_pay": 5.0, "teacher_respect": 6.0, "edu_invest": 6.0,
            "higher_ed": 6.5, "edtech": 6.0, "pub_sector": 7.0,
            "comp": 4.5, "wlb": 7.0, "ot": 6.0, "gender": 7.0, "intl": 7.5,
            "reg": 6.0, "student_pop": 3.5, "research_fund": 5.5},
    # --- EASTERN EUROPE ---
    "PL": {"edu_quality": 7.5, "teacher_pay": 4.5, "teacher_respect": 6.0, "edu_invest": 6.0,
            "higher_ed": 6.5, "edtech": 5.5, "pub_sector": 7.0,
            "comp": 5.5, "wlb": 7.0, "ot": 6.0, "gender": 6.5, "intl": 7.5,
            "reg": 6.5, "student_pop": 4.0, "research_fund": 5.5},
    "CZ": {"edu_quality": 7.5, "teacher_pay": 5.0, "teacher_respect": 6.0, "edu_invest": 6.0,
            "higher_ed": 7.0, "edtech": 6.0, "pub_sector": 7.0,
            "comp": 5.5, "wlb": 7.5, "ot": 6.5, "gender": 6.5, "intl": 7.5,
            "reg": 6.5, "student_pop": 3.5, "research_fund": 6.0},
    "RU": {"edu_quality": 7.0, "teacher_pay": 3.5, "teacher_respect": 5.5, "edu_invest": 5.5,
            "higher_ed": 7.0, "edtech": 5.5, "pub_sector": 8.0,
            "comp": 4.5, "wlb": 5.5, "ot": 5.5, "gender": 6.0, "intl": 3.5,
            "reg": 4.0, "student_pop": 5.5, "research_fund": 5.5},
    # --- NORTH AMERICA ---
    "US": {"edu_quality": 7.5, "teacher_pay": 5.5, "teacher_respect": 5.0, "edu_invest": 7.5,
            "higher_ed": 10.0, "edtech": 9.5, "pub_sector": 6.0,
            "comp": 8.0, "wlb": 5.5, "ot": 4.5, "gender": 7.5, "intl": 8.5,
            "reg": 6.0, "student_pop": 7.5, "research_fund": 10.0},
    "CA": {"edu_quality": 8.0, "teacher_pay": 7.5, "teacher_respect": 7.0, "edu_invest": 7.5,
            "higher_ed": 8.5, "edtech": 8.0, "pub_sector": 7.5,
            "comp": 7.5, "wlb": 7.5, "ot": 6.5, "gender": 8.0, "intl": 9.0,
            "reg": 7.0, "student_pop": 5.5, "research_fund": 8.0},
    "MX": {"edu_quality": 5.0, "teacher_pay": 4.0, "teacher_respect": 5.5, "edu_invest": 5.5,
            "higher_ed": 5.0, "edtech": 4.5, "pub_sector": 7.0,
            "comp": 4.0, "wlb": 5.5, "ot": 4.5, "gender": 5.0, "intl": 5.5,
            "reg": 5.0, "student_pop": 7.5, "research_fund": 3.5},
    # --- SOUTH AMERICA ---
    "BR": {"edu_quality": 5.0, "teacher_pay": 3.5, "teacher_respect": 4.5, "edu_invest": 6.5,
            "higher_ed": 6.0, "edtech": 5.5, "pub_sector": 6.5,
            "comp": 4.5, "wlb": 6.0, "ot": 5.0, "gender": 5.5, "intl": 5.0,
            "reg": 5.5, "student_pop": 8.0, "research_fund": 5.0},
    "AR": {"edu_quality": 5.5, "teacher_pay": 3.0, "teacher_respect": 5.0, "edu_invest": 6.0,
            "higher_ed": 6.0, "edtech": 5.0, "pub_sector": 7.5,
            "comp": 3.5, "wlb": 5.5, "ot": 5.0, "gender": 5.5, "intl": 5.5,
            "reg": 4.5, "student_pop": 5.5, "research_fund": 4.5},
    "CL": {"edu_quality": 6.0, "teacher_pay": 4.0, "teacher_respect": 5.0, "edu_invest": 6.0,
            "higher_ed": 6.0, "edtech": 5.5, "pub_sector": 6.0,
            "comp": 4.5, "wlb": 6.0, "ot": 5.5, "gender": 5.5, "intl": 6.0,
            "reg": 5.5, "student_pop": 4.5, "research_fund": 4.5},
    "CO": {"edu_quality": 5.0, "teacher_pay": 3.5, "teacher_respect": 5.0, "edu_invest": 5.5,
            "higher_ed": 5.0, "edtech": 4.5, "pub_sector": 6.5,
            "comp": 3.5, "wlb": 5.5, "ot": 5.0, "gender": 5.0, "intl": 5.0,
            "reg": 5.0, "student_pop": 5.5, "research_fund": 3.5},
    # --- EAST ASIA ---
    "CN": {"edu_quality": 7.5, "teacher_pay": 5.0, "teacher_respect": 7.5, "edu_invest": 6.5,
            "higher_ed": 7.5, "edtech": 8.5, "pub_sector": 9.0,
            "comp": 6.0, "wlb": 3.5, "ot": 2.5, "gender": 5.5, "intl": 5.0,
            "reg": 5.0, "student_pop": 9.5, "research_fund": 8.0},
    "JP": {"edu_quality": 8.0, "teacher_pay": 7.0, "teacher_respect": 7.0, "edu_invest": 5.5,
            "higher_ed": 8.0, "edtech": 6.0, "pub_sector": 8.0,
            "comp": 6.5, "wlb": 5.0, "ot": 3.5, "gender": 5.0, "intl": 5.0,
            "reg": 6.5, "student_pop": 3.0, "research_fund": 7.5},
    "KR": {"edu_quality": 8.5, "teacher_pay": 7.5, "teacher_respect": 7.5, "edu_invest": 7.0,
            "higher_ed": 7.5, "edtech": 7.5, "pub_sector": 7.5,
            "comp": 6.5, "wlb": 4.5, "ot": 3.0, "gender": 4.5, "intl": 6.0,
            "reg": 6.0, "student_pop": 3.0, "research_fund": 7.0},
    "TW": {"edu_quality": 7.5, "teacher_pay": 6.5, "teacher_respect": 7.0, "edu_invest": 6.0,
            "higher_ed": 7.0, "edtech": 6.5, "pub_sector": 7.5,
            "comp": 5.5, "wlb": 5.0, "ot": 4.0, "gender": 6.0, "intl": 6.5,
            "reg": 6.0, "student_pop": 2.5, "research_fund": 6.0},
    "HK": {"edu_quality": 7.5, "teacher_pay": 7.5, "teacher_respect": 6.5, "edu_invest": 5.5,
            "higher_ed": 8.0, "edtech": 7.0, "pub_sector": 6.5,
            "comp": 7.0, "wlb": 4.5, "ot": 3.5, "gender": 6.5, "intl": 9.0,
            "reg": 6.5, "student_pop": 2.5, "research_fund": 6.5},
    # --- SOUTHEAST ASIA ---
    "SG": {"edu_quality": 9.5, "teacher_pay": 8.0, "teacher_respect": 8.5, "edu_invest": 7.5,
            "higher_ed": 9.0, "edtech": 8.5, "pub_sector": 8.0,
            "comp": 8.0, "wlb": 5.5, "ot": 4.5, "gender": 7.0, "intl": 9.5,
            "reg": 8.0, "student_pop": 3.0, "research_fund": 8.5},
    "TH": {"edu_quality": 5.0, "teacher_pay": 4.0, "teacher_respect": 7.0, "edu_invest": 5.5,
            "higher_ed": 5.0, "edtech": 4.5, "pub_sector": 7.0,
            "comp": 3.5, "wlb": 5.5, "ot": 5.5, "gender": 6.0, "intl": 5.0,
            "reg": 5.0, "student_pop": 5.0, "research_fund": 3.5},
    "VN": {"edu_quality": 6.0, "teacher_pay": 3.0, "teacher_respect": 7.5, "edu_invest": 5.5,
            "higher_ed": 4.5, "edtech": 5.0, "pub_sector": 8.0,
            "comp": 3.0, "wlb": 5.0, "ot": 4.5, "gender": 5.5, "intl": 5.5,
            "reg": 5.0, "student_pop": 6.5, "research_fund": 3.0},
    "ID": {"edu_quality": 4.5, "teacher_pay": 3.0, "teacher_respect": 6.5, "edu_invest": 5.0,
            "higher_ed": 4.5, "edtech": 4.5, "pub_sector": 7.5,
            "comp": 3.5, "wlb": 5.5, "ot": 5.0, "gender": 5.0, "intl": 4.5,
            "reg": 5.0, "student_pop": 8.5, "research_fund": 3.0},
    "MY": {"edu_quality": 6.0, "teacher_pay": 5.0, "teacher_respect": 6.5, "edu_invest": 6.0,
            "higher_ed": 6.0, "edtech": 5.5, "pub_sector": 7.5,
            "comp": 4.5, "wlb": 5.5, "ot": 5.0, "gender": 5.5, "intl": 6.5,
            "reg": 5.5, "student_pop": 5.5, "research_fund": 4.5},
    "PH": {"edu_quality": 4.5, "teacher_pay": 2.5, "teacher_respect": 6.5, "edu_invest": 4.5,
            "higher_ed": 4.5, "edtech": 4.0, "pub_sector": 6.0,
            "comp": 3.0, "wlb": 5.0, "ot": 4.5, "gender": 6.5, "intl": 6.5,
            "reg": 4.5, "student_pop": 7.5, "research_fund": 2.5},
    # --- SOUTH ASIA ---
    "IN": {"edu_quality": 5.5, "teacher_pay": 3.0, "teacher_respect": 7.0, "edu_invest": 4.5,
            "higher_ed": 6.5, "edtech": 7.0, "pub_sector": 7.5,
            "comp": 4.0, "wlb": 4.5, "ot": 4.0, "gender": 4.5, "intl": 7.0,
            "reg": 5.0, "student_pop": 10.0, "research_fund": 5.0},
    "PK": {"edu_quality": 3.5, "teacher_pay": 2.5, "teacher_respect": 5.5, "edu_invest": 3.5,
            "higher_ed": 4.0, "edtech": 3.5, "pub_sector": 6.5,
            "comp": 2.5, "wlb": 4.5, "ot": 4.5, "gender": 3.0, "intl": 5.0,
            "reg": 4.0, "student_pop": 8.5, "research_fund": 2.5},
    "BD": {"edu_quality": 3.5, "teacher_pay": 2.0, "teacher_respect": 5.5, "edu_invest": 3.0,
            "higher_ed": 3.5, "edtech": 3.5, "pub_sector": 6.5,
            "comp": 2.0, "wlb": 4.5, "ot": 4.5, "gender": 3.5, "intl": 5.0,
            "reg": 3.5, "student_pop": 8.5, "research_fund": 2.0},
    # --- MIDDLE EAST ---
    "AE": {"edu_quality": 6.5, "teacher_pay": 7.5, "teacher_respect": 6.0, "edu_invest": 5.5,
            "higher_ed": 6.5, "edtech": 7.0, "pub_sector": 7.0,
            "comp": 8.0, "wlb": 5.5, "ot": 5.0, "gender": 5.0, "intl": 8.5,
            "reg": 6.5, "student_pop": 4.0, "research_fund": 5.5},
    "IL": {"edu_quality": 7.5, "teacher_pay": 6.0, "teacher_respect": 6.5, "edu_invest": 7.5,
            "higher_ed": 8.5, "edtech": 8.0, "pub_sector": 6.5,
            "comp": 7.0, "wlb": 6.0, "ot": 5.0, "gender": 7.0, "intl": 8.0,
            "reg": 5.5, "student_pop": 4.5, "research_fund": 8.5},
    "SA": {"edu_quality": 5.0, "teacher_pay": 6.5, "teacher_respect": 5.5, "edu_invest": 7.0,
            "higher_ed": 5.0, "edtech": 5.0, "pub_sector": 8.5,
            "comp": 6.5, "wlb": 5.5, "ot": 5.0, "gender": 3.5, "intl": 4.5,
            "reg": 5.5, "student_pop": 6.0, "research_fund": 5.0},
    "TR": {"edu_quality": 5.5, "teacher_pay": 4.0, "teacher_respect": 6.0, "edu_invest": 5.5,
            "higher_ed": 5.5, "edtech": 5.0, "pub_sector": 7.5,
            "comp": 4.0, "wlb": 5.0, "ot": 4.5, "gender": 4.5, "intl": 5.5,
            "reg": 5.0, "student_pop": 7.0, "research_fund": 4.0},
    # --- OCEANIA ---
    "AU": {"edu_quality": 8.0, "teacher_pay": 7.5, "teacher_respect": 6.5, "edu_invest": 7.0,
            "higher_ed": 9.0, "edtech": 8.0, "pub_sector": 7.5,
            "comp": 7.5, "wlb": 8.0, "ot": 7.0, "gender": 8.0, "intl": 8.5,
            "reg": 7.0, "student_pop": 5.5, "research_fund": 8.0},
    "NZ": {"edu_quality": 7.5, "teacher_pay": 6.5, "teacher_respect": 7.0, "edu_invest": 7.0,
            "higher_ed": 7.5, "edtech": 7.0, "pub_sector": 7.5,
            "comp": 6.5, "wlb": 8.5, "ot": 7.5, "gender": 8.5, "intl": 8.0,
            "reg": 7.0, "student_pop": 3.5, "research_fund": 6.5},
    # --- AFRICA ---
    "ZA": {"edu_quality": 4.5, "teacher_pay": 4.5, "teacher_respect": 5.5, "edu_invest": 6.5,
            "higher_ed": 5.5, "edtech": 4.5, "pub_sector": 6.5,
            "comp": 4.0, "wlb": 5.5, "ot": 5.5, "gender": 5.5, "intl": 5.5,
            "reg": 5.0, "student_pop": 6.5, "research_fund": 4.5},
    "NG": {"edu_quality": 3.5, "teacher_pay": 2.0, "teacher_respect": 4.5, "edu_invest": 3.0,
            "higher_ed": 3.5, "edtech": 3.5, "pub_sector": 5.5,
            "comp": 2.5, "wlb": 4.5, "ot": 4.5, "gender": 4.0, "intl": 5.0,
            "reg": 3.5, "student_pop": 9.5, "research_fund": 2.0},
    "KE": {"edu_quality": 4.5, "teacher_pay": 2.5, "teacher_respect": 5.5, "edu_invest": 5.0,
            "higher_ed": 4.5, "edtech": 4.5, "pub_sector": 6.0,
            "comp": 2.5, "wlb": 5.0, "ot": 5.0, "gender": 4.5, "intl": 5.5,
            "reg": 4.0, "student_pop": 7.5, "research_fund": 2.5},
    "EG": {"edu_quality": 4.5, "teacher_pay": 2.5, "teacher_respect": 5.0, "edu_invest": 4.5,
            "higher_ed": 5.0, "edtech": 4.0, "pub_sector": 7.5,
            "comp": 2.5, "wlb": 5.0, "ot": 4.5, "gender": 3.5, "intl": 5.0,
            "reg": 4.0, "student_pop": 8.0, "research_fund": 3.0},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES — intrinsic characteristics of each occupation
# ---------------------------------------------------------------------------

def occ_base(occ_id, mid_cat):
    """Return base (global average) scores for an occupation."""
    bases = {
        # ===== K12_EDUCATION =====
        "0101": {  # Elementary School Teacher
            "learning_cost": 5.0, "education_req": 5.5,
            "growth_coeff": 4.0, "career_lifespan": 8.5,
            "opportunity": 6.5, "market_size": 9.0, "supply_demand": 5.0, "developed_scarcity": 5.5,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 8.0, "safety": 9.0, "occupational_disease": 5.5, "overtime": 6.5, "burnout": 4.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 8.0, "social_status": 5.5, "remote_friendly": 3.0, "autonomy": 5.5,
            "family_friendly": 7.0, "fulfillment": 7.5, "entrepreneurship": 3.5, "gender_equality": 7.5,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 4.0, "license_barrier": 6.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 5.0, "intl_mobility": 4.5, "industry_monopoly": 2.5,
            "trend_long": 1, "trend_short": 0, "edu": "本科/教育学", "age": "22-28",
        },
        "0102": {  # Secondary School Teacher
            "learning_cost": 5.5, "education_req": 6.0,
            "growth_coeff": 4.0, "career_lifespan": 8.5,
            "opportunity": 6.5, "market_size": 8.5, "supply_demand": 5.5, "developed_scarcity": 6.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 8.0, "safety": 8.5, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 4.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 7.5, "social_status": 5.5, "remote_friendly": 3.5, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 3.5, "gender_equality": 6.5,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 3.5, "license_barrier": 6.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 5.5, "intl_mobility": 5.0, "industry_monopoly": 2.5,
            "trend_long": 1, "trend_short": 0, "edu": "本科/硕士", "age": "22-28",
        },
        "0103": {  # Special Education Teacher
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 5.0, "career_lifespan": 8.0,
            "opportunity": 6.0, "market_size": 5.5, "supply_demand": 7.0, "developed_scarcity": 7.5,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 8.0, "safety": 8.0, "occupational_disease": 5.0, "overtime": 6.0, "burnout": 3.5,
            "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.0,
            "ai_resistance": 9.0, "social_status": 6.0, "remote_friendly": 2.5, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 8.5, "entrepreneurship": 3.0, "gender_equality": 8.0,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 5.0, "license_barrier": 7.0,
            "cycle_sensitivity": 1.0, "side_job_compat": 4.0, "intl_mobility": 5.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 2, "edu": "本科/硕士(特教)", "age": "22-28",
        },
        "0104": {  # School Counselor
            "learning_cost": 6.5, "education_req": 6.5,
            "growth_coeff": 5.0, "career_lifespan": 8.5,
            "opportunity": 5.5, "market_size": 5.0, "supply_demand": 6.5, "developed_scarcity": 7.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 7.5, "safety": 9.0, "occupational_disease": 5.0, "overtime": 6.5, "burnout": 4.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 8.5, "social_status": 6.0, "remote_friendly": 4.0, "autonomy": 6.5,
            "family_friendly": 7.0, "fulfillment": 8.0, "entrepreneurship": 4.0, "gender_equality": 8.0,
            "age_flexibility": 7.5, "social_interaction": 9.0, "physical_demand": 1.5, "license_barrier": 7.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 5.5, "intl_mobility": 5.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 2, "edu": "硕士(心理学/教育)", "age": "24-30",
        },
        "0105": {  # International School Teacher
            "learning_cost": 5.5, "education_req": 6.0,
            "growth_coeff": 5.5, "career_lifespan": 7.5,
            "opportunity": 5.5, "market_size": 4.0, "supply_demand": 6.0, "developed_scarcity": 5.0,
            "value_added": 6.5, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.0, "occupational_disease": 6.0, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 7.5, "social_status": 6.5, "remote_friendly": 3.0, "autonomy": 6.0,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 3.5, "gender_equality": 7.0,
            "age_flexibility": 6.5, "social_interaction": 8.0, "physical_demand": 3.0, "license_barrier": 5.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 4.5, "intl_mobility": 8.5, "industry_monopoly": 2.5,
            "trend_long": 3, "trend_short": 2, "edu": "本科/硕士", "age": "22-30",
        },
        "0106": {  # Physical Education Teacher
            "learning_cost": 4.5, "education_req": 5.0,
            "growth_coeff": 3.5, "career_lifespan": 7.0,
            "opportunity": 5.5, "market_size": 7.0, "supply_demand": 4.5, "developed_scarcity": 4.5,
            "value_added": 4.0, "cost_performance": 5.0,
            "stability": 7.5, "safety": 7.5, "occupational_disease": 4.5, "overtime": 7.0, "burnout": 5.5,
            "skill_versatility": 4.0, "career_switch": 4.5, "reputation_variance": 2.0,
            "ai_resistance": 9.0, "social_status": 5.0, "remote_friendly": 1.5, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 4.0, "gender_equality": 5.5,
            "age_flexibility": 5.0, "social_interaction": 8.5, "physical_demand": 7.5, "license_barrier": 5.5,
            "cycle_sensitivity": 1.5, "side_job_compat": 5.5, "intl_mobility": 4.0, "industry_monopoly": 2.5,
            "trend_long": 1, "trend_short": 0, "edu": "本科(体育)", "age": "22-28",
        },
        "0107": {  # Music Teacher
            "learning_cost": 6.0, "education_req": 5.5,
            "growth_coeff": 3.5, "career_lifespan": 8.0,
            "opportunity": 5.0, "market_size": 5.5, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 4.0, "cost_performance": 4.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 8.5, "social_status": 5.5, "remote_friendly": 4.0, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 8.0, "entrepreneurship": 5.5, "gender_equality": 7.0,
            "age_flexibility": 7.5, "social_interaction": 7.5, "physical_demand": 2.5, "license_barrier": 4.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 7.5, "intl_mobility": 5.0, "industry_monopoly": 2.0,
            "trend_long": 0, "trend_short": 0, "edu": "本科(音乐)", "age": "22-28",
        },
        "0108": {  # Art Teacher
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 3.5, "career_lifespan": 8.0,
            "opportunity": 5.0, "market_size": 5.5, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 4.0, "cost_performance": 4.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 7.5, "social_status": 5.5, "remote_friendly": 3.5, "autonomy": 6.5,
            "family_friendly": 6.5, "fulfillment": 8.0, "entrepreneurship": 6.0, "gender_equality": 7.0,
            "age_flexibility": 7.5, "social_interaction": 7.5, "physical_demand": 2.0, "license_barrier": 4.0,
            "cycle_sensitivity": 2.0, "side_job_compat": 7.5, "intl_mobility": 5.0, "industry_monopoly": 2.0,
            "trend_long": 0, "trend_short": 0, "edu": "本科(美术)", "age": "22-28",
        },
        "0109": {  # High School Math Teacher
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 4.5, "career_lifespan": 8.5,
            "opportunity": 6.5, "market_size": 7.5, "supply_demand": 6.5, "developed_scarcity": 7.0,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 8.0, "safety": 9.0, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 4.5,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 6.0, "remote_friendly": 4.0, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 5.0, "gender_equality": 5.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 2.0, "license_barrier": 6.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 7.0, "intl_mobility": 5.5, "industry_monopoly": 2.5,
            "trend_long": 1, "trend_short": 1, "edu": "本科/硕士(数学)", "age": "22-28",
        },
        "0110": {  # IT / Computer Science Teacher
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 6.0, "career_lifespan": 7.5,
            "opportunity": 6.5, "market_size": 6.0, "supply_demand": 7.0, "developed_scarcity": 7.5,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 7.0, "reputation_variance": 2.0,
            "ai_resistance": 6.0, "social_status": 6.0, "remote_friendly": 5.5, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 5.5, "gender_equality": 5.5,
            "age_flexibility": 6.5, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 5.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 7.0, "intl_mobility": 6.0, "industry_monopoly": 2.5,
            "trend_long": 3, "trend_short": 3, "edu": "本科(计算机/教育)", "age": "22-30",
        },
        "0111": {  # Foreign Language Teacher (K-12)
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 4.0, "career_lifespan": 8.0,
            "opportunity": 6.0, "market_size": 7.0, "supply_demand": 5.0, "developed_scarcity": 5.0,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 5.5, "overtime": 6.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 5.5, "remote_friendly": 5.0, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 5.0, "gender_equality": 7.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 2.0, "license_barrier": 5.5,
            "cycle_sensitivity": 1.5, "side_job_compat": 7.0, "intl_mobility": 6.5, "industry_monopoly": 2.0,
            "trend_long": 1, "trend_short": 0, "edu": "本科(外语)", "age": "22-28",
        },
        "0112": {  # Science Teacher
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 4.5, "career_lifespan": 8.5,
            "opportunity": 6.5, "market_size": 7.5, "supply_demand": 6.0, "developed_scarcity": 6.5,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 8.0, "safety": 8.0, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 6.0, "remote_friendly": 3.5, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 4.0, "gender_equality": 5.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 3.0, "license_barrier": 6.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 6.0, "intl_mobility": 5.5, "industry_monopoly": 2.5,
            "trend_long": 2, "trend_short": 1, "edu": "本科/硕士(理科)", "age": "22-28",
        },
        "0113": {  # School Library Media Specialist
            "learning_cost": 5.0, "education_req": 5.5,
            "growth_coeff": 2.5, "career_lifespan": 8.0,
            "opportunity": 4.0, "market_size": 4.5, "supply_demand": 3.5, "developed_scarcity": 3.5,
            "value_added": 3.5, "cost_performance": 4.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 7.5, "burnout": 6.5,
            "skill_versatility": 4.5, "career_switch": 4.5, "reputation_variance": 1.0,
            "ai_resistance": 5.5, "social_status": 4.5, "remote_friendly": 3.0, "autonomy": 6.0,
            "family_friendly": 7.5, "fulfillment": 6.5, "entrepreneurship": 2.5, "gender_equality": 8.0,
            "age_flexibility": 8.0, "social_interaction": 7.0, "physical_demand": 2.0, "license_barrier": 5.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 4.5, "intl_mobility": 3.5, "industry_monopoly": 2.5,
            "trend_long": -1, "trend_short": -1, "edu": "本科/硕士(图书馆学)", "age": "22-30",
        },
        # ===== HIGHER_EDUCATION =====
        "0201": {  # University Professor
            "learning_cost": 9.0, "education_req": 9.5,
            "growth_coeff": 5.5, "career_lifespan": 9.0,
            "opportunity": 5.5, "market_size": 5.0, "supply_demand": 5.0, "developed_scarcity": 5.5,
            "value_added": 7.0, "cost_performance": 5.5,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.0, "burnout": 4.0,
            "skill_versatility": 7.0, "career_switch": 5.5, "reputation_variance": 2.5,
            "ai_resistance": 7.5, "social_status": 8.0, "remote_friendly": 5.5, "autonomy": 8.5,
            "family_friendly": 6.0, "fulfillment": 8.5, "entrepreneurship": 5.0, "gender_equality": 5.5,
            "age_flexibility": 8.0, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 8.0,
            "cycle_sensitivity": 2.0, "side_job_compat": 6.5, "intl_mobility": 7.5, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 0, "edu": "博士", "age": "30-40",
        },
        "0202": {  # University Lecturer
            "learning_cost": 7.5, "education_req": 7.5,
            "growth_coeff": 4.5, "career_lifespan": 8.0,
            "opportunity": 5.5, "market_size": 5.5, "supply_demand": 4.5, "developed_scarcity": 4.5,
            "value_added": 5.5, "cost_performance": 5.0,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.5, "burnout": 4.5,
            "skill_versatility": 6.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 7.0, "social_status": 7.0, "remote_friendly": 5.5, "autonomy": 7.0,
            "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 4.5, "gender_equality": 5.5,
            "age_flexibility": 7.5, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 7.0,
            "cycle_sensitivity": 2.5, "side_job_compat": 6.5, "intl_mobility": 7.0, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": -1, "edu": "硕士/博士", "age": "27-35",
        },
        "0203": {  # Postdoctoral Researcher
            "learning_cost": 9.5, "education_req": 9.5,
            "growth_coeff": 5.0, "career_lifespan": 4.0,
            "opportunity": 5.0, "market_size": 3.5, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 5.0, "cost_performance": 3.5,
            "stability": 3.5, "safety": 9.5, "occupational_disease": 5.5, "overtime": 4.0, "burnout": 3.5,
            "skill_versatility": 7.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 7.5, "social_status": 7.0, "remote_friendly": 6.0, "autonomy": 7.0,
            "family_friendly": 4.0, "fulfillment": 7.5, "entrepreneurship": 4.5, "gender_equality": 5.0,
            "age_flexibility": 3.5, "social_interaction": 6.5, "physical_demand": 2.0, "license_barrier": 9.0,
            "cycle_sensitivity": 3.0, "side_job_compat": 5.0, "intl_mobility": 9.0, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 0, "edu": "博士", "age": "27-35",
        },
        "0204": {  # Teaching Assistant
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 3.5, "career_lifespan": 4.0,
            "opportunity": 5.0, "market_size": 5.0, "supply_demand": 4.0, "developed_scarcity": 3.5,
            "value_added": 3.0, "cost_performance": 3.5,
            "stability": 4.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 4.5, "remote_friendly": 5.0, "autonomy": 4.5,
            "family_friendly": 5.5, "fulfillment": 6.0, "entrepreneurship": 3.0, "gender_equality": 6.5,
            "age_flexibility": 4.0, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 5.0,
            "cycle_sensitivity": 2.5, "side_job_compat": 5.5, "intl_mobility": 6.0, "industry_monopoly": 3.0,
            "trend_long": 0, "trend_short": -1, "edu": "硕士在读/硕士", "age": "22-28",
        },
        "0205": {  # University Admissions Officer
            "learning_cost": 4.5, "education_req": 5.5,
            "growth_coeff": 4.0, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 4.0, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 5.0, "autonomy": 5.0,
            "family_friendly": 6.5, "fulfillment": 6.0, "entrepreneurship": 3.0, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 1.0, "license_barrier": 3.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 4.0, "intl_mobility": 5.0, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 0, "edu": "本科/硕士", "age": "24-30",
        },
        "0206": {  # Tenured Professor
            "learning_cost": 9.5, "education_req": 10.0,
            "growth_coeff": 4.5, "career_lifespan": 10.0,
            "opportunity": 3.5, "market_size": 3.0, "supply_demand": 3.0, "developed_scarcity": 3.5,
            "value_added": 8.0, "cost_performance": 6.0,
            "stability": 9.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.5, "burnout": 4.5,
            "skill_versatility": 7.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 8.0, "social_status": 9.0, "remote_friendly": 6.0, "autonomy": 9.5,
            "family_friendly": 7.0, "fulfillment": 9.0, "entrepreneurship": 5.5, "gender_equality": 5.0,
            "age_flexibility": 9.0, "social_interaction": 7.0, "physical_demand": 1.0, "license_barrier": 9.5,
            "cycle_sensitivity": 0.5, "side_job_compat": 7.0, "intl_mobility": 7.5, "industry_monopoly": 3.5,
            "trend_long": 0, "trend_short": -1, "edu": "博士+多年研究", "age": "35-50",
        },
        "0207": {  # Academic Advisor
            "learning_cost": 5.5, "education_req": 6.0,
            "growth_coeff": 4.0, "career_lifespan": 7.5,
            "opportunity": 5.0, "market_size": 4.5, "supply_demand": 5.0, "developed_scarcity": 4.5,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 5.5, "remote_friendly": 5.5, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 3.5, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 1.0, "license_barrier": 4.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 4.5, "intl_mobility": 5.0, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 1, "edu": "硕士", "age": "25-32",
        },
        "0208": {  # Adjunct / Visiting Professor
            "learning_cost": 8.0, "education_req": 8.5,
            "growth_coeff": 4.0, "career_lifespan": 6.0,
            "opportunity": 5.0, "market_size": 4.5, "supply_demand": 3.5, "developed_scarcity": 3.0,
            "value_added": 4.0, "cost_performance": 3.5,
            "stability": 3.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 4.0,
            "skill_versatility": 6.5, "career_switch": 5.0, "reputation_variance": 2.5,
            "ai_resistance": 7.0, "social_status": 6.5, "remote_friendly": 5.5, "autonomy": 7.0,
            "family_friendly": 4.5, "fulfillment": 7.0, "entrepreneurship": 5.0, "gender_equality": 5.5,
            "age_flexibility": 6.5, "social_interaction": 7.0, "physical_demand": 1.5, "license_barrier": 7.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.0, "intl_mobility": 8.0, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 0, "edu": "博士", "age": "30-45",
        },
        # ===== VOCATIONAL_TRAINING =====
        "0301": {  # Corporate Trainer
            "learning_cost": 4.5, "education_req": 5.0,
            "growth_coeff": 5.5, "career_lifespan": 7.0,
            "opportunity": 6.5, "market_size": 6.5, "supply_demand": 5.5, "developed_scarcity": 4.5,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 5.5, "remote_friendly": 6.5, "autonomy": 6.5,
            "family_friendly": 5.5, "fulfillment": 6.5, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 8.5, "physical_demand": 2.0, "license_barrier": 2.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 7.5, "intl_mobility": 5.5, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 1, "edu": "本科/硕士", "age": "25-35",
        },
        "0302": {  # Certification Instructor
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 5.0, "career_lifespan": 7.0,
            "opportunity": 5.5, "market_size": 5.0, "supply_demand": 5.5, "developed_scarcity": 5.0,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 6.0, "autonomy": 6.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.0, "gender_equality": 6.0,
            "age_flexibility": 7.0, "social_interaction": 7.5, "physical_demand": 1.5, "license_barrier": 4.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.0, "intl_mobility": 5.0, "industry_monopoly": 2.5,
            "trend_long": 2, "trend_short": 1, "edu": "本科+行业认证", "age": "25-35",
        },
        "0303": {  # Vocational Education Teacher
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 4.0, "career_lifespan": 8.0,
            "opportunity": 5.5, "market_size": 6.5, "supply_demand": 5.5, "developed_scarcity": 5.5,
            "value_added": 4.5, "cost_performance": 5.5,
            "stability": 7.5, "safety": 8.5, "occupational_disease": 5.5, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 7.5, "social_status": 5.0, "remote_friendly": 3.5, "autonomy": 5.5,
            "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 4.0, "gender_equality": 5.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 4.0, "license_barrier": 4.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 5.5, "intl_mobility": 4.0, "industry_monopoly": 2.5,
            "trend_long": 2, "trend_short": 1, "edu": "大专/本科+实操经验", "age": "25-35",
        },
        "0304": {  # Driving Instructor
            "learning_cost": 2.5, "education_req": 2.5,
            "growth_coeff": 2.5, "career_lifespan": 7.0,
            "opportunity": 5.5, "market_size": 7.0, "supply_demand": 4.5, "developed_scarcity": 3.0,
            "value_added": 3.5, "cost_performance": 5.0,
            "stability": 6.5, "safety": 6.5, "occupational_disease": 4.0, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 2.5, "career_switch": 3.5, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 3.5, "remote_friendly": 0.5, "autonomy": 6.5,
            "family_friendly": 5.5, "fulfillment": 5.0, "entrepreneurship": 6.5, "gender_equality": 4.0,
            "age_flexibility": 6.5, "social_interaction": 7.5, "physical_demand": 4.0, "license_barrier": 5.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 6.5, "intl_mobility": 2.5, "industry_monopoly": 2.0,
            "trend_long": -1, "trend_short": -2, "edu": "高中/大专+驾照", "age": "25-40",
        },
        "0305": {  # Language Training Teacher
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 4.5, "career_lifespan": 7.5,
            "opportunity": 6.0, "market_size": 7.0, "supply_demand": 5.0, "developed_scarcity": 4.5,
            "value_added": 4.5, "cost_performance": 5.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 5.5, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 6.0, "social_status": 5.0, "remote_friendly": 7.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 7.0, "gender_equality": 7.5,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 3.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 8.0, "intl_mobility": 7.0, "industry_monopoly": 1.5,
            "trend_long": 1, "trend_short": -1, "edu": "本科(语言)+认证", "age": "22-30",
        },
        "0306": {  # Flight Instructor
            "learning_cost": 8.0, "education_req": 5.5,
            "growth_coeff": 4.5, "career_lifespan": 6.5,
            "opportunity": 4.5, "market_size": 2.5, "supply_demand": 6.5, "developed_scarcity": 6.5,
            "value_added": 6.5, "cost_performance": 5.5,
            "stability": 5.5, "safety": 5.0, "occupational_disease": 4.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 3.5, "career_switch": 3.5, "reputation_variance": 1.0,
            "ai_resistance": 8.0, "social_status": 7.0, "remote_friendly": 0.5, "autonomy": 6.5,
            "family_friendly": 4.0, "fulfillment": 8.0, "entrepreneurship": 5.5, "gender_equality": 3.5,
            "age_flexibility": 5.0, "social_interaction": 7.0, "physical_demand": 4.0, "license_barrier": 9.0,
            "cycle_sensitivity": 5.0, "side_job_compat": 4.0, "intl_mobility": 7.0, "industry_monopoly": 4.0,
            "trend_long": 1, "trend_short": 1, "edu": "飞行执照+培训资质", "age": "25-35",
        },
        "0307": {  # Etiquette Trainer
            "learning_cost": 3.5, "education_req": 3.5,
            "growth_coeff": 3.5, "career_lifespan": 7.0,
            "opportunity": 4.0, "market_size": 3.0, "supply_demand": 3.5, "developed_scarcity": 2.5,
            "value_added": 4.0, "cost_performance": 5.0,
            "stability": 4.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.5, "burnout": 6.0,
            "skill_versatility": 4.0, "career_switch": 4.5, "reputation_variance": 3.0,
            "ai_resistance": 7.0, "social_status": 5.0, "remote_friendly": 4.0, "autonomy": 7.5,
            "family_friendly": 6.0, "fulfillment": 6.0, "entrepreneurship": 7.5, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 2.5, "license_barrier": 1.5,
            "cycle_sensitivity": 5.0, "side_job_compat": 8.0, "intl_mobility": 4.0, "industry_monopoly": 1.0,
            "trend_long": 0, "trend_short": 0, "edu": "大专/本科+培训", "age": "25-35",
        },
        # ===== ONLINE_EDUCATION =====
        "0401": {  # Online Course Designer
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 6.5, "career_lifespan": 6.5,
            "opportunity": 7.0, "market_size": 6.0, "supply_demand": 6.5, "developed_scarcity": 5.5,
            "value_added": 5.5, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.0,
            "ai_resistance": 5.0, "social_status": 5.5, "remote_friendly": 9.0, "autonomy": 7.0,
            "family_friendly": 7.0, "fulfillment": 7.0, "entrepreneurship": 7.0, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 1.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 8.0, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 4, "trend_short": 3, "edu": "本科/硕士(教育技术)", "age": "24-32",
        },
        "0402": {  # EdTech Product Manager
            "learning_cost": 6.0, "education_req": 5.5,
            "growth_coeff": 7.5, "career_lifespan": 7.0,
            "opportunity": 7.5, "market_size": 5.5, "supply_demand": 7.0, "developed_scarcity": 6.5,
            "value_added": 7.0, "cost_performance": 7.0,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 4.5,
            "skill_versatility": 8.0, "career_switch": 7.5, "reputation_variance": 2.5,
            "ai_resistance": 6.0, "social_status": 6.5, "remote_friendly": 8.0, "autonomy": 7.5,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 8.5, "gender_equality": 6.0,
            "age_flexibility": 6.0, "social_interaction": 8.0, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 5.5, "side_job_compat": 6.5, "intl_mobility": 7.5, "industry_monopoly": 3.0,
            "trend_long": 5, "trend_short": 4, "edu": "本科/硕士", "age": "25-33",
        },
        "0403": {  # MOOC Instructor
            "learning_cost": 6.5, "education_req": 7.0,
            "growth_coeff": 5.5, "career_lifespan": 6.0,
            "opportunity": 6.0, "market_size": 5.0, "supply_demand": 5.0, "developed_scarcity": 4.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 4.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.5,
            "ai_resistance": 5.5, "social_status": 6.0, "remote_friendly": 9.5, "autonomy": 7.0,
            "family_friendly": 7.0, "fulfillment": 7.5, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 7.0, "social_interaction": 5.0, "physical_demand": 0.5, "license_barrier": 3.5,
            "cycle_sensitivity": 4.5, "side_job_compat": 8.5, "intl_mobility": 8.0, "industry_monopoly": 3.5,
            "trend_long": 4, "trend_short": 2, "edu": "硕士/博士", "age": "28-40",
        },
        "0404": {  # Instructional Designer
            "learning_cost": 5.0, "education_req": 5.5,
            "growth_coeff": 6.5, "career_lifespan": 7.0,
            "opportunity": 6.5, "market_size": 5.5, "supply_demand": 6.5, "developed_scarcity": 5.5,
            "value_added": 5.5, "cost_performance": 6.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.5,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 1.5,
            "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 8.5, "autonomy": 7.0,
            "family_friendly": 7.0, "fulfillment": 7.0, "entrepreneurship": 6.5, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 2.0,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.5, "intl_mobility": 7.0, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 2, "edu": "本科/硕士(教育技术)", "age": "24-32",
        },
        "0405": {  # Online Education Operations Manager
            "learning_cost": 4.5, "education_req": 5.0,
            "growth_coeff": 6.0, "career_lifespan": 6.5,
            "opportunity": 6.5, "market_size": 5.0, "supply_demand": 5.5, "developed_scarcity": 4.5,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 4.5, "burnout": 4.5,
            "skill_versatility": 6.5, "career_switch": 6.5, "reputation_variance": 2.5,
            "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 8.0, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 6.0, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 6.0, "social_interaction": 7.5, "physical_demand": 0.5, "license_barrier": 1.0,
            "cycle_sensitivity": 5.5, "side_job_compat": 6.0, "intl_mobility": 6.0, "industry_monopoly": 3.0,
            "trend_long": 4, "trend_short": 3, "edu": "本科", "age": "24-30",
        },
        # ===== ACADEMIC_RESEARCH =====
        "0501": {  # Natural Science Researcher
            "learning_cost": 9.0, "education_req": 9.0,
            "growth_coeff": 5.0, "career_lifespan": 8.0,
            "opportunity": 5.5, "market_size": 4.0, "supply_demand": 5.5, "developed_scarcity": 6.5,
            "value_added": 6.5, "cost_performance": 5.0,
            "stability": 6.5, "safety": 7.5, "occupational_disease": 5.5, "overtime": 4.5, "burnout": 4.0,
            "skill_versatility": 7.0, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 7.0, "social_status": 7.5, "remote_friendly": 4.5, "autonomy": 7.5,
            "family_friendly": 5.0, "fulfillment": 8.5, "entrepreneurship": 5.0, "gender_equality": 5.0,
            "age_flexibility": 6.5, "social_interaction": 6.0, "physical_demand": 3.5, "license_barrier": 8.0,
            "cycle_sensitivity": 3.0, "side_job_compat": 5.0, "intl_mobility": 8.5, "industry_monopoly": 3.5,
            "trend_long": 2, "trend_short": 1, "edu": "博士", "age": "27-35",
        },
        "0502": {  # Social Science Researcher
            "learning_cost": 8.0, "education_req": 8.5,
            "growth_coeff": 4.0, "career_lifespan": 8.0,
            "opportunity": 5.0, "market_size": 4.0, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 5.5, "cost_performance": 4.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.0, "burnout": 4.5,
            "skill_versatility": 7.0, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 7.0, "remote_friendly": 7.0, "autonomy": 8.0,
            "family_friendly": 5.5, "fulfillment": 8.0, "entrepreneurship": 4.5, "gender_equality": 6.0,
            "age_flexibility": 7.5, "social_interaction": 6.5, "physical_demand": 1.0, "license_barrier": 7.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 6.5, "intl_mobility": 7.5, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 0, "edu": "博士", "age": "27-35",
        },
        "0503": {  # Humanities Researcher
            "learning_cost": 8.0, "education_req": 8.5,
            "growth_coeff": 3.0, "career_lifespan": 8.5,
            "opportunity": 4.0, "market_size": 3.0, "supply_demand": 3.5, "developed_scarcity": 3.5,
            "value_added": 4.5, "cost_performance": 3.5,
            "stability": 5.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 7.5, "autonomy": 8.5,
            "family_friendly": 6.0, "fulfillment": 8.5, "entrepreneurship": 4.0, "gender_equality": 6.5,
            "age_flexibility": 8.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 7.5,
            "cycle_sensitivity": 2.5, "side_job_compat": 7.0, "intl_mobility": 7.0, "industry_monopoly": 2.5,
            "trend_long": -1, "trend_short": -1, "edu": "博士", "age": "27-35",
        },
        "0504": {  # Laboratory Director
            "learning_cost": 8.5, "education_req": 9.0,
            "growth_coeff": 5.5, "career_lifespan": 8.5,
            "opportunity": 4.5, "market_size": 3.0, "supply_demand": 5.5, "developed_scarcity": 6.0,
            "value_added": 7.5, "cost_performance": 6.0,
            "stability": 7.5, "safety": 7.0, "occupational_disease": 5.0, "overtime": 4.5, "burnout": 4.0,
            "skill_versatility": 6.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 7.5, "social_status": 8.0, "remote_friendly": 3.5, "autonomy": 8.0,
            "family_friendly": 5.0, "fulfillment": 8.0, "entrepreneurship": 6.0, "gender_equality": 5.0,
            "age_flexibility": 6.5, "social_interaction": 7.0, "physical_demand": 2.5, "license_barrier": 8.0,
            "cycle_sensitivity": 3.0, "side_job_compat": 4.5, "intl_mobility": 7.5, "industry_monopoly": 4.0,
            "trend_long": 2, "trend_short": 1, "edu": "博士+管理经验", "age": "35-45",
        },
        "0505": {  # Research Assistant
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 4.0, "career_lifespan": 4.5,
            "opportunity": 5.5, "market_size": 5.0, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 3.5, "cost_performance": 4.0,
            "stability": 4.0, "safety": 8.0, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 4.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 6.0, "social_status": 5.0, "remote_friendly": 5.0, "autonomy": 4.5,
            "family_friendly": 5.0, "fulfillment": 6.5, "entrepreneurship": 3.5, "gender_equality": 6.0,
            "age_flexibility": 4.5, "social_interaction": 6.5, "physical_demand": 3.0, "license_barrier": 4.5,
            "cycle_sensitivity": 3.5, "side_job_compat": 4.5, "intl_mobility": 6.5, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 0, "edu": "本科/硕士在读", "age": "22-28",
        },
        "0506": {  # Academic Journal Editor
            "learning_cost": 7.0, "education_req": 7.5,
            "growth_coeff": 3.5, "career_lifespan": 8.0,
            "opportunity": 4.0, "market_size": 2.5, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 5.0, "cost_performance": 4.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.0,
            "ai_resistance": 5.5, "social_status": 6.5, "remote_friendly": 8.0, "autonomy": 7.0,
            "family_friendly": 7.0, "fulfillment": 7.0, "entrepreneurship": 3.5, "gender_equality": 6.5,
            "age_flexibility": 8.0, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 6.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 6.5, "intl_mobility": 7.0, "industry_monopoly": 3.5,
            "trend_long": 0, "trend_short": -1, "edu": "博士/硕士", "age": "28-38",
        },
        "0507": {  # Research Grants Administrator
            "learning_cost": 5.0, "education_req": 6.0,
            "growth_coeff": 4.5, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 3.5, "supply_demand": 5.0, "developed_scarcity": 5.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 5.5, "reputation_variance": 1.0,
            "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 6.5, "autonomy": 5.5,
            "family_friendly": 7.0, "fulfillment": 5.5, "entrepreneurship": 3.0, "gender_equality": 7.0,
            "age_flexibility": 7.0, "social_interaction": 7.0, "physical_demand": 0.5, "license_barrier": 3.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 4.0, "intl_mobility": 5.5, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 1, "edu": "硕士", "age": "25-33",
        },
        "0508": {  # Science Communicator
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 5.5, "career_lifespan": 7.5,
            "opportunity": 5.5, "market_size": 4.0, "supply_demand": 5.0, "developed_scarcity": 4.5,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 6.0, "burnout": 5.5,
            "skill_versatility": 7.0, "career_switch": 6.0, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 6.0, "remote_friendly": 7.5, "autonomy": 7.0,
            "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 1.5, "license_barrier": 2.0,
            "cycle_sensitivity": 3.5, "side_job_compat": 8.0, "intl_mobility": 6.5, "industry_monopoly": 2.0,
            "trend_long": 3, "trend_short": 2, "edu": "硕士/博士", "age": "25-35",
        },
        # ===== EDUCATION_ADMIN =====
        "0601": {  # School Principal
            "learning_cost": 7.0, "education_req": 7.0,
            "growth_coeff": 4.5, "career_lifespan": 8.0,
            "opportunity": 4.5, "market_size": 5.5, "supply_demand": 5.0, "developed_scarcity": 5.0,
            "value_added": 6.5, "cost_performance": 6.0,
            "stability": 8.0, "safety": 9.0, "occupational_disease": 5.5, "overtime": 4.5, "burnout": 3.5,
            "skill_versatility": 6.5, "career_switch": 5.0, "reputation_variance": 2.0,
            "ai_resistance": 8.5, "social_status": 7.5, "remote_friendly": 2.5, "autonomy": 7.5,
            "family_friendly": 5.0, "fulfillment": 8.0, "entrepreneurship": 4.5, "gender_equality": 5.5,
            "age_flexibility": 6.5, "social_interaction": 9.0, "physical_demand": 2.5, "license_barrier": 7.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 3.0, "intl_mobility": 4.5, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 0, "edu": "硕士+教学经验", "age": "35-45",
        },
        "0602": {  # Academic Dean
            "learning_cost": 7.5, "education_req": 7.5,
            "growth_coeff": 4.5, "career_lifespan": 7.5,
            "opportunity": 4.0, "market_size": 4.0, "supply_demand": 4.5, "developed_scarcity": 4.5,
            "value_added": 6.5, "cost_performance": 6.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.0, "burnout": 4.0,
            "skill_versatility": 6.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 7.5, "social_status": 7.5, "remote_friendly": 4.0, "autonomy": 7.0,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 4.0, "gender_equality": 5.5,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 6.5,
            "cycle_sensitivity": 1.5, "side_job_compat": 3.5, "intl_mobility": 5.0, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 0, "edu": "硕士/博士", "age": "35-45",
        },
        "0603": {  # Education Policy Researcher
            "learning_cost": 7.5, "education_req": 8.0,
            "growth_coeff": 4.5, "career_lifespan": 8.0,
            "opportunity": 4.5, "market_size": 3.0, "supply_demand": 4.5, "developed_scarcity": 5.0,
            "value_added": 5.5, "cost_performance": 5.0,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 6.5, "social_status": 7.0, "remote_friendly": 6.5, "autonomy": 7.5,
            "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 3.5, "gender_equality": 6.0,
            "age_flexibility": 7.0, "social_interaction": 7.0, "physical_demand": 0.5, "license_barrier": 6.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 6.0, "intl_mobility": 7.0, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 1, "edu": "博士", "age": "28-35",
        },
        "0604": {  # University President
            "learning_cost": 9.5, "education_req": 9.5,
            "growth_coeff": 4.0, "career_lifespan": 7.0,
            "opportunity": 2.5, "market_size": 1.5, "supply_demand": 2.5, "developed_scarcity": 3.0,
            "value_added": 9.5, "cost_performance": 7.0,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 5.5, "overtime": 3.5, "burnout": 3.0,
            "skill_versatility": 7.5, "career_switch": 5.0, "reputation_variance": 3.0,
            "ai_resistance": 9.0, "social_status": 9.5, "remote_friendly": 3.0, "autonomy": 9.0,
            "family_friendly": 4.0, "fulfillment": 8.5, "entrepreneurship": 5.5, "gender_equality": 4.5,
            "age_flexibility": 6.0, "social_interaction": 9.5, "physical_demand": 2.0, "license_barrier": 9.5,
            "cycle_sensitivity": 1.0, "side_job_compat": 2.5, "intl_mobility": 6.0, "industry_monopoly": 4.0,
            "trend_long": 0, "trend_short": 0, "edu": "博士+高管经验", "age": "45-60",
        },
        "0605": {  # Education Inspector / Superintendent
            "learning_cost": 6.5, "education_req": 7.0,
            "growth_coeff": 3.5, "career_lifespan": 7.5,
            "opportunity": 4.0, "market_size": 3.5, "supply_demand": 4.0, "developed_scarcity": 4.0,
            "value_added": 6.0, "cost_performance": 5.5,
            "stability": 8.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 4.5, "reputation_variance": 1.5,
            "ai_resistance": 7.5, "social_status": 7.0, "remote_friendly": 3.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 3.0, "gender_equality": 5.5,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 2.0, "license_barrier": 6.5,
            "cycle_sensitivity": 1.0, "side_job_compat": 3.0, "intl_mobility": 4.0, "industry_monopoly": 4.0,
            "trend_long": 0, "trend_short": 0, "edu": "硕士+行政经验", "age": "35-45",
        },
        "0606": {  # Director of Admissions
            "learning_cost": 5.0, "education_req": 6.0,
            "growth_coeff": 4.5, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 3.5, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 5.5, "cost_performance": 5.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.0, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.5, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 6.0, "remote_friendly": 4.5, "autonomy": 6.0,
            "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 3.5, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 4.0,
            "cycle_sensitivity": 2.5, "side_job_compat": 3.5, "intl_mobility": 5.5, "industry_monopoly": 3.5,
            "trend_long": 1, "trend_short": 0, "edu": "硕士", "age": "28-38",
        },
        "0607": {  # Dean of Students
            "learning_cost": 6.0, "education_req": 6.5,
            "growth_coeff": 4.0, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 4.0, "supply_demand": 4.5, "developed_scarcity": 4.0,
            "value_added": 5.5, "cost_performance": 5.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 5.5, "overtime": 5.0, "burnout": 4.5,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 8.0, "social_status": 6.5, "remote_friendly": 3.5, "autonomy": 6.5,
            "family_friendly": 5.5, "fulfillment": 7.5, "entrepreneurship": 3.5, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 9.0, "physical_demand": 2.0, "license_barrier": 5.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 3.0, "intl_mobility": 5.0, "industry_monopoly": 3.0,
            "trend_long": 1, "trend_short": 1, "edu": "硕士+学生工作经验", "age": "30-40",
        },
        # ===== EARLY_CHILDHOOD =====
        "0701": {  # Kindergarten Teacher
            "learning_cost": 4.0, "education_req": 4.5,
            "growth_coeff": 4.0, "career_lifespan": 7.5,
            "opportunity": 6.5, "market_size": 8.0, "supply_demand": 5.5, "developed_scarcity": 6.0,
            "value_added": 3.5, "cost_performance": 4.5,
            "stability": 7.5, "safety": 8.5, "occupational_disease": 5.0, "overtime": 6.5, "burnout": 4.5,
            "skill_versatility": 4.5, "career_switch": 4.5, "reputation_variance": 1.5,
            "ai_resistance": 9.0, "social_status": 5.0, "remote_friendly": 1.5, "autonomy": 5.0,
            "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 4.5, "gender_equality": 9.0,
            "age_flexibility": 6.0, "social_interaction": 9.0, "physical_demand": 6.0, "license_barrier": 5.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 4.0, "intl_mobility": 4.0, "industry_monopoly": 2.0,
            "trend_long": 1, "trend_short": 1, "edu": "大专/本科(学前教育)", "age": "20-26",
        },
        "0702": {  # Montessori Teacher
            "learning_cost": 5.5, "education_req": 5.0,
            "growth_coeff": 5.0, "career_lifespan": 7.5,
            "opportunity": 5.0, "market_size": 4.0, "supply_demand": 5.5, "developed_scarcity": 5.5,
            "value_added": 4.5, "cost_performance": 5.0,
            "stability": 6.0, "safety": 8.5, "occupational_disease": 5.0, "overtime": 6.5, "burnout": 5.0,
            "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.5,
            "ai_resistance": 9.0, "social_status": 5.5, "remote_friendly": 1.5, "autonomy": 6.5,
            "family_friendly": 6.0, "fulfillment": 8.0, "entrepreneurship": 6.0, "gender_equality": 8.5,
            "age_flexibility": 6.5, "social_interaction": 8.5, "physical_demand": 5.5, "license_barrier": 5.0,
            "cycle_sensitivity": 3.0, "side_job_compat": 4.5, "intl_mobility": 6.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 1, "edu": "蒙氏认证+大专以上", "age": "22-28",
        },
        "0703": {  # Infant Care Specialist / Nanny
            "learning_cost": 2.5, "education_req": 2.5,
            "growth_coeff": 4.0, "career_lifespan": 6.5,
            "opportunity": 6.0, "market_size": 7.0, "supply_demand": 5.0, "developed_scarcity": 5.5,
            "value_added": 3.0, "cost_performance": 4.5,
            "stability": 5.5, "safety": 8.0, "occupational_disease": 4.5, "overtime": 5.0, "burnout": 4.5,
            "skill_versatility": 3.0, "career_switch": 3.5, "reputation_variance": 2.0,
            "ai_resistance": 9.5, "social_status": 4.0, "remote_friendly": 0.5, "autonomy": 5.0,
            "family_friendly": 5.0, "fulfillment": 7.0, "entrepreneurship": 5.0, "gender_equality": 9.5,
            "age_flexibility": 6.0, "social_interaction": 8.0, "physical_demand": 7.0, "license_barrier": 3.0,
            "cycle_sensitivity": 2.5, "side_job_compat": 4.0, "intl_mobility": 4.5, "industry_monopoly": 1.0,
            "trend_long": 1, "trend_short": 1, "edu": "高中/大专+育婴证", "age": "20-35",
        },
        "0704": {  # Early Childhood Center Teacher
            "learning_cost": 4.0, "education_req": 4.5,
            "growth_coeff": 4.5, "career_lifespan": 7.0,
            "opportunity": 6.0, "market_size": 6.5, "supply_demand": 5.5, "developed_scarcity": 5.5,
            "value_added": 3.5, "cost_performance": 4.5,
            "stability": 6.5, "safety": 8.5, "occupational_disease": 5.0, "overtime": 6.5, "burnout": 4.5,
            "skill_versatility": 4.5, "career_switch": 4.5, "reputation_variance": 1.5,
            "ai_resistance": 9.0, "social_status": 5.0, "remote_friendly": 1.5, "autonomy": 5.0,
            "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 5.0, "gender_equality": 9.0,
            "age_flexibility": 6.0, "social_interaction": 9.0, "physical_demand": 6.0, "license_barrier": 4.5,
            "cycle_sensitivity": 2.5, "side_job_compat": 4.0, "intl_mobility": 4.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 1, "edu": "大专/本科(学前教育)", "age": "20-26",
        },
        "0705": {  # Child Development Assessor
            "learning_cost": 6.5, "education_req": 6.5,
            "growth_coeff": 5.0, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 3.5, "supply_demand": 5.5, "developed_scarcity": 6.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 6.5, "safety": 9.0, "occupational_disease": 5.5, "overtime": 6.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 8.0, "social_status": 6.0, "remote_friendly": 4.0, "autonomy": 6.5,
            "family_friendly": 6.5, "fulfillment": 8.0, "entrepreneurship": 5.0, "gender_equality": 8.0,
            "age_flexibility": 7.0, "social_interaction": 8.0, "physical_demand": 2.0, "license_barrier": 6.5,
            "cycle_sensitivity": 2.0, "side_job_compat": 5.5, "intl_mobility": 5.5, "industry_monopoly": 2.5,
            "trend_long": 2, "trend_short": 2, "edu": "硕士(发展心理学)", "age": "25-32",
        },
        # ===== SPECIAL_EDUCATION (& Support) =====
        "0801": {  # Learning Disability Specialist
            "learning_cost": 6.5, "education_req": 6.5,
            "growth_coeff": 5.0, "career_lifespan": 8.0,
            "opportunity": 5.5, "market_size": 4.5, "supply_demand": 6.5, "developed_scarcity": 7.0,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 7.5, "safety": 8.5, "occupational_disease": 5.0, "overtime": 6.0, "burnout": 4.0,
            "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.0,
            "ai_resistance": 8.5, "social_status": 6.0, "remote_friendly": 3.0, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 8.5, "entrepreneurship": 4.0, "gender_equality": 8.0,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 3.5, "license_barrier": 6.5,
            "cycle_sensitivity": 1.5, "side_job_compat": 5.0, "intl_mobility": 5.0, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 2, "edu": "硕士(特殊教育)", "age": "24-30",
        },
        "0802": {  # Educational Psychologist
            "learning_cost": 8.0, "education_req": 8.0,
            "growth_coeff": 5.5, "career_lifespan": 8.5,
            "opportunity": 5.5, "market_size": 4.0, "supply_demand": 6.5, "developed_scarcity": 7.0,
            "value_added": 6.5, "cost_performance": 6.0,
            "stability": 7.0, "safety": 9.0, "occupational_disease": 5.0, "overtime": 6.0, "burnout": 4.0,
            "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
            "ai_resistance": 8.0, "social_status": 7.5, "remote_friendly": 5.0, "autonomy": 7.5,
            "family_friendly": 6.5, "fulfillment": 8.5, "entrepreneurship": 6.0, "gender_equality": 7.0,
            "age_flexibility": 7.5, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 8.0,
            "cycle_sensitivity": 1.5, "side_job_compat": 6.5, "intl_mobility": 6.5, "industry_monopoly": 2.5,
            "trend_long": 2, "trend_short": 2, "edu": "博士/硕士(心理学)", "age": "26-33",
        },
        "0803": {  # Sign Language Teacher/Interpreter
            "learning_cost": 5.5, "education_req": 5.0,
            "growth_coeff": 4.0, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 3.0, "supply_demand": 6.0, "developed_scarcity": 6.5,
            "value_added": 4.0, "cost_performance": 5.0,
            "stability": 6.5, "safety": 9.0, "occupational_disease": 5.5, "overtime": 6.5, "burnout": 5.5,
            "skill_versatility": 4.0, "career_switch": 4.0, "reputation_variance": 1.0,
            "ai_resistance": 7.5, "social_status": 5.5, "remote_friendly": 4.5, "autonomy": 6.0,
            "family_friendly": 6.0, "fulfillment": 8.0, "entrepreneurship": 4.5, "gender_equality": 7.5,
            "age_flexibility": 7.0, "social_interaction": 8.5, "physical_demand": 3.0, "license_barrier": 5.5,
            "cycle_sensitivity": 1.5, "side_job_compat": 6.5, "intl_mobility": 4.5, "industry_monopoly": 2.0,
            "trend_long": 1, "trend_short": 0, "edu": "大专/本科(手语)", "age": "22-30",
        },
        "0804": {  # After-school Tutor
            "learning_cost": 3.0, "education_req": 3.5,
            "growth_coeff": 4.0, "career_lifespan": 6.0,
            "opportunity": 6.5, "market_size": 7.5, "supply_demand": 4.0, "developed_scarcity": 3.0,
            "value_added": 3.5, "cost_performance": 5.0,
            "stability": 4.0, "safety": 9.5, "occupational_disease": 5.5, "overtime": 5.0, "burnout": 4.5,
            "skill_versatility": 4.0, "career_switch": 5.0, "reputation_variance": 2.5,
            "ai_resistance": 6.0, "social_status": 4.0, "remote_friendly": 6.5, "autonomy": 6.5,
            "family_friendly": 5.0, "fulfillment": 6.0, "entrepreneurship": 7.0, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 8.0, "physical_demand": 1.5, "license_barrier": 1.5,
            "cycle_sensitivity": 3.5, "side_job_compat": 9.0, "intl_mobility": 3.5, "industry_monopoly": 1.0,
            "trend_long": 1, "trend_short": -1, "edu": "大专/本科", "age": "20-30",
        },
        "0805": {  # STEM Education Specialist
            "learning_cost": 6.0, "education_req": 6.0,
            "growth_coeff": 6.5, "career_lifespan": 7.5,
            "opportunity": 6.0, "market_size": 5.0, "supply_demand": 6.5, "developed_scarcity": 6.5,
            "value_added": 5.5, "cost_performance": 6.0,
            "stability": 6.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 6.0, "burnout": 5.0,
            "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.0,
            "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 5.5, "autonomy": 6.5,
            "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 6.5, "gender_equality": 6.0,
            "age_flexibility": 6.5, "social_interaction": 7.5, "physical_demand": 2.0, "license_barrier": 3.5,
            "cycle_sensitivity": 3.0, "side_job_compat": 7.0, "intl_mobility": 6.5, "industry_monopoly": 2.5,
            "trend_long": 3, "trend_short": 3, "edu": "硕士(STEM+教育)", "age": "25-33",
        },
        "0806": {  # Study Abroad Counselor / Education Agent
            "learning_cost": 4.0, "education_req": 4.5,
            "growth_coeff": 5.0, "career_lifespan": 7.0,
            "opportunity": 6.0, "market_size": 5.5, "supply_demand": 4.5, "developed_scarcity": 3.5,
            "value_added": 4.5, "cost_performance": 5.5,
            "stability": 5.0, "safety": 9.5, "occupational_disease": 6.0, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 5.5, "career_switch": 6.0, "reputation_variance": 3.0,
            "ai_resistance": 6.0, "social_status": 5.0, "remote_friendly": 6.0, "autonomy": 6.0,
            "family_friendly": 5.5, "fulfillment": 6.0, "entrepreneurship": 7.5, "gender_equality": 7.0,
            "age_flexibility": 6.0, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 2.0,
            "cycle_sensitivity": 5.5, "side_job_compat": 7.0, "intl_mobility": 7.5, "industry_monopoly": 2.0,
            "trend_long": 2, "trend_short": 0, "edu": "本科+留学经历", "age": "23-30",
        },
        "0807": {  # Test Developer / Exam Grader
            "learning_cost": 6.0, "education_req": 6.5,
            "growth_coeff": 3.5, "career_lifespan": 7.5,
            "opportunity": 4.5, "market_size": 4.0, "supply_demand": 4.5, "developed_scarcity": 4.5,
            "value_added": 5.0, "cost_performance": 5.5,
            "stability": 7.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.5,
            "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 1.5,
            "ai_resistance": 5.0, "social_status": 5.5, "remote_friendly": 6.5, "autonomy": 6.0,
            "family_friendly": 6.5, "fulfillment": 6.0, "entrepreneurship": 3.5, "gender_equality": 6.5,
            "age_flexibility": 7.0, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 5.0,
            "cycle_sensitivity": 2.5, "side_job_compat": 6.0, "intl_mobility": 5.5, "industry_monopoly": 3.5,
            "trend_long": 0, "trend_short": -1, "edu": "硕士(教育测量)", "age": "25-33",
        },
        "0808": {  # Education Data Analyst
            "learning_cost": 5.5, "education_req": 5.5,
            "growth_coeff": 6.5, "career_lifespan": 7.0,
            "opportunity": 6.5, "market_size": 4.5, "supply_demand": 6.5, "developed_scarcity": 6.0,
            "value_added": 5.5, "cost_performance": 6.5,
            "stability": 6.0, "safety": 9.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
            "skill_versatility": 7.5, "career_switch": 7.0, "reputation_variance": 1.5,
            "ai_resistance": 4.5, "social_status": 5.5, "remote_friendly": 8.0, "autonomy": 6.5,
            "family_friendly": 6.5, "fulfillment": 6.5, "entrepreneurship": 6.0, "gender_equality": 6.5,
            "age_flexibility": 6.5, "social_interaction": 6.0, "physical_demand": 0.5, "license_barrier": 1.5,
            "cycle_sensitivity": 4.0, "side_job_compat": 7.5, "intl_mobility": 7.0, "industry_monopoly": 2.5,
            "trend_long": 4, "trend_short": 3, "edu": "本科/硕士(数据科学)", "age": "23-30",
        },
        "0809": {  # School Librarian
            "learning_cost": 5.0, "education_req": 5.0,
            "growth_coeff": 2.0, "career_lifespan": 8.0,
            "opportunity": 3.5, "market_size": 4.5, "supply_demand": 3.0, "developed_scarcity": 3.0,
            "value_added": 3.5, "cost_performance": 4.0,
            "stability": 7.5, "safety": 9.5, "occupational_disease": 6.5, "overtime": 7.5, "burnout": 7.0,
            "skill_versatility": 4.0, "career_switch": 4.5, "reputation_variance": 1.0,
            "ai_resistance": 5.0, "social_status": 4.5, "remote_friendly": 2.5, "autonomy": 6.0,
            "family_friendly": 8.0, "fulfillment": 6.5, "entrepreneurship": 2.0, "gender_equality": 8.5,
            "age_flexibility": 8.5, "social_interaction": 6.5, "physical_demand": 2.5, "license_barrier": 4.5,
            "cycle_sensitivity": 1.0, "side_job_compat": 4.5, "intl_mobility": 3.5, "industry_monopoly": 2.5,
            "trend_long": -2, "trend_short": -2, "edu": "本科/硕士(图书馆学)", "age": "22-30",
        },
    }
    return bases.get(occ_id, {})


# ---------------------------------------------------------------------------
# SCORING ENGINE
# ---------------------------------------------------------------------------

def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))


def apply_country_modifiers(base_scores, country_profile, occ_id, mid_cat):
    """Adjust base scores based on education-specific country profile."""
    cp = country_profile
    s = dict(base_scores)

    # Education quality influences many dimensions
    eq_factor = (cp["edu_quality"] - 6.0) / 4.0  # ~-1 to +1

    # Teacher pay strongly affects compensation dimensions
    pay_factor = (cp["teacher_pay"] - 5.0) / 5.0  # normalized
    comp_factor = (cp["comp"] - 5.0) / 5.0

    s["value_added"] = clamp(s["value_added"] + pay_factor * 1.5 + comp_factor * 1.0)
    s["cost_performance"] = clamp(s["cost_performance"] + pay_factor * 0.8 + eq_factor * 0.5)

    # Growth coefficient: education investment + student population (demand)
    invest_factor = (cp["edu_invest"] - 6.0) / 4.0
    pop_factor = (cp["student_pop"] - 5.0) / 5.0
    s["growth_coeff"] = clamp(s["growth_coeff"] + invest_factor * 0.5 + pop_factor * 0.3)

    # Career lifespan: public sector strength = stability = longer careers
    pub_factor = (cp["pub_sector"] - 6.5) / 3.5
    s["career_lifespan"] = clamp(s["career_lifespan"] + pub_factor * 0.6)

    # Opportunity: student population + education investment
    s["opportunity"] = clamp(s["opportunity"] + pop_factor * 1.0 + invest_factor * 0.5)

    # Market size: student population is the primary driver
    s["market_size"] = clamp(s["market_size"] + pop_factor * 1.5)

    # Supply-demand: teacher shortage indicators
    s["supply_demand"] = clamp(s["supply_demand"] + eq_factor * 0.5 + pay_factor * 0.5)

    # Developed scarcity: higher in developed countries with teacher shortages
    dev_bonus = 1.0 if cp["edu_quality"] >= 7.5 else (0.0 if cp["edu_quality"] >= 5.0 else -1.0)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus * 0.8)

    # Stability: public sector strength is the #1 driver for education
    s["stability"] = clamp(s["stability"] + pub_factor * 1.2 + invest_factor * 0.3)

    # Safety
    s["safety"] = clamp(s["safety"] + eq_factor * 0.2)

    # Occupational disease: work-life balance
    wlb_factor = (cp["wlb"] - 6.0) / 4.0
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_factor * 0.8)

    # Overtime: country overtime culture
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)

    # Burnout
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)

    # Remote friendly: EdTech adoption level
    edtech_factor = (cp["edtech"] - 5.5) / 4.5
    s["remote_friendly"] = clamp(s["remote_friendly"] + edtech_factor * 1.0)

    # Autonomy: teacher respect + work culture
    respect_factor = (cp["teacher_respect"] - 6.0) / 4.0
    s["autonomy"] = clamp(s["autonomy"] + respect_factor * 0.5 + wlb_factor * 0.3)

    # Family friendly: work-life balance
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_factor * 1.5)

    # Social status: teacher respect is the primary driver
    s["social_status"] = clamp(s["social_status"] + respect_factor * 1.5 + comp_factor * 0.5)

    # Fulfillment: education quality correlates with teacher fulfillment
    s["fulfillment"] = clamp(s["fulfillment"] + eq_factor * 0.5)

    # Gender equality
    gender_factor = (cp["gender"] - 5.5) / 4.5
    s["gender_equality"] = clamp(s["gender_equality"] + gender_factor * 2.0)

    # Age flexibility: better in strong public sectors
    s["age_flexibility"] = clamp(s["age_flexibility"] + pub_factor * 0.5 + wlb_factor * 0.3)

    # Entrepreneurship: EdTech + regulatory environment
    reg_factor = (cp["reg"] - 5.5) / 4.5
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + edtech_factor * 0.5 + reg_factor * 0.3)

    # International mobility: country openness
    intl_factor = (cp["intl"] - 6.0) / 4.0
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_factor * 1.5)

    # AI resistance: doesn't vary hugely by country
    s["ai_resistance"] = clamp(s["ai_resistance"] + edtech_factor * 0.2)

    # Learning cost / education req: formal education system requirements
    s["learning_cost"] = clamp(s["learning_cost"] + eq_factor * 0.3)
    s["education_req"] = clamp(s["education_req"] + eq_factor * 0.3)

    # License barrier: more regulated in high-quality education systems
    s["license_barrier"] = clamp(s["license_barrier"] + eq_factor * 0.5 + reg_factor * 0.3)

    # Cycle sensitivity: education is counter-cyclical in strong public sectors
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - pub_factor * 0.5)

    # Side job compat: EdTech openness
    s["side_job_compat"] = clamp(s["side_job_compat"] + edtech_factor * 0.3)

    # Industry monopoly: higher in less competitive systems
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - eq_factor * 0.3 + pub_factor * 0.2)

    # Skill versatility: better in higher quality education systems
    s["skill_versatility"] = clamp(s["skill_versatility"] + eq_factor * 0.4)

    # Career switch: easier in more dynamic education markets
    s["career_switch"] = clamp(s["career_switch"] + eq_factor * 0.3 + edtech_factor * 0.3)

    # Reputation variance: higher in emerging markets
    rep_adj = -0.3 if cp["edu_quality"] >= 7.5 else (0.3 if cp["edu_quality"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # --- Mid-category-specific adjustments ---

    # Higher education: university ranking / research output matters
    if mid_cat == "higher_education":
        he_factor = (cp["higher_ed"] - 6.5) / 3.5
        rf_factor = (cp["research_fund"] - 5.5) / 4.5
        s["value_added"] = clamp(s["value_added"] + he_factor * 1.0)
        s["social_status"] = clamp(s["social_status"] + he_factor * 0.8)
        s["opportunity"] = clamp(s["opportunity"] + he_factor * 0.5)
        s["intl_mobility"] = clamp(s["intl_mobility"] + he_factor * 0.5)
        s["supply_demand"] = clamp(s["supply_demand"] + rf_factor * 0.5)

    # Online education: EdTech maturity is critical
    if mid_cat == "online_education":
        s["remote_friendly"] = clamp(s["remote_friendly"] + edtech_factor * 1.5)
        s["opportunity"] = clamp(s["opportunity"] + edtech_factor * 1.0)
        s["growth_coeff"] = clamp(s["growth_coeff"] + edtech_factor * 0.8)
        s["market_size"] = clamp(s["market_size"] + edtech_factor * 1.0)

    # Academic research: research funding is critical
    if mid_cat == "academic_research":
        rf_factor = (cp["research_fund"] - 5.5) / 4.5
        s["value_added"] = clamp(s["value_added"] + rf_factor * 1.5)
        s["opportunity"] = clamp(s["opportunity"] + rf_factor * 0.8)
        s["supply_demand"] = clamp(s["supply_demand"] + rf_factor * 0.5)
        s["stability"] = clamp(s["stability"] + rf_factor * 0.5)
        s["intl_mobility"] = clamp(s["intl_mobility"] + rf_factor * 0.5)

    # Early childhood: different dynamics - always in demand, low pay
    if mid_cat == "early_childhood":
        s["supply_demand"] = clamp(s["supply_demand"] + pop_factor * 0.5)
        s["stability"] = clamp(s["stability"] + pop_factor * 0.3)

    # K12: teacher pay and respect are especially important
    if mid_cat == "k12_education":
        s["stability"] = clamp(s["stability"] + pub_factor * 0.3)
        s["social_status"] = clamp(s["social_status"] + respect_factor * 0.5)

    # Education admin: public sector + regulation
    if mid_cat == "education_admin":
        s["stability"] = clamp(s["stability"] + pub_factor * 0.5)
        s["value_added"] = clamp(s["value_added"] + pub_factor * 0.5)

    return s


def get_trends(base_scores, country_profile):
    """Get trend values adjusted for country."""
    cp = country_profile
    t_long = base_scores["trend_long"]
    t_short = base_scores["trend_short"]

    # EdTech-advanced countries boost online/tech-related education trends
    if cp["edtech"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["edtech"] < 4.0:
        t_short = max(-5, t_short - 1)

    # Declining student population depresses long-term trends
    if cp["student_pop"] <= 3.0:
        t_long = max(-5, t_long - 1)
    elif cp["student_pop"] >= 8.0:
        t_long = min(5, t_long + 1)

    return t_long, t_short


def get_demand_direction(trend_5yr):
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

    if scores["stability"] >= 8.0:
        highlights_zh.append("就业稳定")
        highlights_en.append("stable employment")
    elif scores["stability"] <= 4.0:
        highlights_zh.append("就业波动大")
        highlights_en.append("volatile employment")

    if scores["fulfillment"] >= 8.0:
        highlights_zh.append("职业满足感高")
        highlights_en.append("high job fulfillment")

    if scores["overtime"] <= 3.5:
        highlights_zh.append("加班文化严重")
        highlights_en.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5:
        highlights_zh.append("工作时间规律")
        highlights_en.append("regular working hours")

    if scores["remote_friendly"] >= 8.5:
        highlights_zh.append("远程友好度高")
        highlights_en.append("highly remote-friendly")

    if trend_5yr >= 4:
        highlights_zh.append("近年增长迅猛")
        highlights_en.append("rapid recent growth")
    elif trend_5yr <= -2:
        highlights_zh.append("近年需求下降")
        highlights_en.append("declining demand")

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
    csv_path = PROJECT_ROOT / "data" / "csv" / "education_academia.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        if not base:
            print(f"WARNING: No base scores for {occ['id']} ({occ['en']}), skipping")
            continue

        for country in COUNTRIES:
            iso = country["iso"]
            cp = COUNTRY_PROFILES[iso]

            scores = apply_country_modifiers(base, cp, occ["id"], occ["mid"])

            # Add small per-row noise for realism
            noise_seed = hash(f"EDU-{occ['id']}-{iso}") % 10000
            rng = random.Random(noise_seed)
            for dim in SCORE_DIMS:
                if dim == "reputation_variance":
                    scores[dim] = clamp5(scores[dim] + rng.uniform(-0.2, 0.2))
                elif dim in ("safety",):
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.1, 0.1))
                else:
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.3, 0.3))

            trend_long, trend_short = get_trends(base, cp)
            demand_dir = get_demand_direction(trend_short)
            ai_tl = get_ai_timeline(occ["id"], scores["ai_resistance"])

            score_dict = {dim: scores[dim] for dim in weights}
            composite = calculate_composite(score_dict, weights)

            summary_zh, summary_en = generate_summary(occ, country, scores, trend_short, scores["ai_resistance"])

            row_id = f"EDU-{occ['id']}-{iso}-general"

            row = {
                "id": row_id,
                "major_category": "教育与学术",
                "major_code": "EDU",
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

            for dim in SCORE_DIMS:
                row[dim] = scores[dim]

            row["trend_2000_2026"] = trend_long
            row["trend_5yr"] = trend_short
            row["demand_direction"] = demand_dir
            row["ai_timeline"] = ai_tl
            row["composite_index"] = composite
            row["summary_zh"] = summary_zh
            row["summary_en"] = summary_en
            row["data_source"] = "AI综合评估 + O*NET/ILO/UNESCO锚点校准"

            rows.append(row)

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows to {csv_path}")
    print(f"Occupations: {len(OCCUPATIONS)}")
    print(f"Countries: {len(COUNTRIES)}")

    # Generate JSON
    from tools.csv_to_json import convert_csv_to_json
    json_path = PROJECT_ROOT / "data" / "json" / "education_academia.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Generate notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "04_education_academia.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="教育与学术 (EDU) — 完整数据",
        description="62 occupations × 45 countries/regions = 2,790 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
