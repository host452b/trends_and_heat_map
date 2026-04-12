#!/usr/bin/env python3
"""Generate finance_business.csv — FIN data for Global Career Development Index.

Creates scored data for all FIN occupations across all 45 countries/regions.
Uses realistic, country-differentiated scoring based on global financial labor market knowledge.
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
# OCCUPATION DEFINITIONS (from categories.yaml FIN section)
# ---------------------------------------------------------------------------

OCCUPATIONS = [
    # ===== banking (12) =====
    {"id": "0101", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "银行柜员", "en": "Bank Teller", "isco": "4211", "onet": "43-3071.00", "locality": "global"},
    {"id": "0102", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "客户经理(银行)", "en": "Bank Relationship Manager", "isco": "2412", "onet": "13-2072.00", "locality": "global"},
    {"id": "0103", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "信贷审批员", "en": "Credit Analyst", "isco": "2413", "onet": "13-2041.00", "locality": "global"},
    {"id": "0104", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "风控专员", "en": "Risk Management Specialist", "isco": "2413", "onet": "13-2054.00", "locality": "global"},
    {"id": "0105", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "合规专员", "en": "Compliance Officer", "isco": "2413", "onet": "13-1041.00", "locality": "global"},
    {"id": "0106", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "私人银行家", "en": "Private Banker", "isco": "2412", "onet": "13-2052.00", "locality": "global"},
    {"id": "0107", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "贸易融资专员", "en": "Trade Finance Specialist", "isco": "2413", "onet": "13-2072.00", "locality": "global"},
    {"id": "0108", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "银行分行行长", "en": "Bank Branch Manager", "isco": "1346", "onet": "11-3031.01", "locality": "global"},
    {"id": "0109", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "外汇交易员(银行)", "en": "Bank FX Trader", "isco": "3311", "onet": "13-2051.00", "locality": "global"},
    {"id": "0110", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "信用卡业务经理", "en": "Credit Card Business Manager", "isco": "1346", "onet": "11-3031.01", "locality": "global"},
    {"id": "0111", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "金融科技产品经理", "en": "FinTech Product Manager", "isco": "2511", "onet": "15-1299.09", "locality": "global"},
    {"id": "0112", "mid": "banking", "mid_zh": "银行", "mid_en": "Banking",
     "zh": "反洗钱分析师", "en": "Anti-Money Laundering (AML) Analyst", "isco": "2413", "onet": "13-2054.00", "locality": "global"},
    # ===== securities_investment (15) =====
    {"id": "0201", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "股票分析师", "en": "Equity Analyst", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "0202", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "基金经理", "en": "Fund Manager", "isco": "2411", "onet": "11-3031.01", "locality": "global"},
    {"id": "0203", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "投行分析师", "en": "Investment Banking Analyst", "isco": "2411", "onet": "13-2051.00", "locality": "global"},
    {"id": "0204", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "PE投资经理", "en": "Private Equity Manager", "isco": "2411", "onet": "11-3031.02", "locality": "global"},
    {"id": "0205", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "风险投资人", "en": "Venture Capitalist", "isco": "2411", "onet": "11-3031.02", "locality": "global"},
    {"id": "0206", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "量化交易员", "en": "Quantitative Trader", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "0207", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "债券分析师", "en": "Fixed Income Analyst", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "0208", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "证券经纪人", "en": "Stockbroker", "isco": "3311", "onet": "41-3031.00", "locality": "global"},
    {"id": "0209", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "外汇交易员", "en": "Forex Trader", "isco": "3311", "onet": "13-2051.00", "locality": "global"},
    {"id": "0210", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "财富管理顾问", "en": "Wealth Management Advisor", "isco": "2412", "onet": "13-2052.00", "locality": "global"},
    {"id": "0211", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "信托经理", "en": "Trust Manager", "isco": "2411", "onet": "13-2052.00", "locality": "global"},
    {"id": "0212", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "衍生品交易员", "en": "Derivatives Trader", "isco": "3311", "onet": "13-2051.00", "locality": "global"},
    {"id": "0213", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "商品期货交易员", "en": "Commodity Futures Trader", "isco": "3311", "onet": "13-2051.00", "locality": "global"},
    {"id": "0214", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "投资组合分析师", "en": "Portfolio Analyst", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "0215", "mid": "securities_investment", "mid_zh": "证券投资", "mid_en": "Securities & Investment",
     "zh": "资产管理经理", "en": "Asset Manager", "isco": "2411", "onet": "11-3031.02", "locality": "global"},
    # ===== insurance (9) =====
    {"id": "0301", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "精算师", "en": "Actuary", "isco": "2120", "onet": "15-2011.00", "locality": "global"},
    {"id": "0302", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险代理人", "en": "Insurance Agent", "isco": "3321", "onet": "41-3021.00", "locality": "global"},
    {"id": "0303", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险理赔员", "en": "Claims Adjuster", "isco": "3315", "onet": "13-1031.02", "locality": "global"},
    {"id": "0304", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险精算分析师", "en": "Actuarial Analyst", "isco": "2120", "onet": "15-2011.00", "locality": "global"},
    {"id": "0305", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险核保师", "en": "Insurance Underwriter", "isco": "3321", "onet": "13-2053.00", "locality": "global"},
    {"id": "0306", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "再保险专员", "en": "Reinsurance Specialist", "isco": "3321", "onet": "13-2053.00", "locality": "global"},
    {"id": "0307", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险产品开发师", "en": "Insurance Product Developer", "isco": "3321", "onet": "13-2053.00", "locality": "global"},
    {"id": "0308", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "保险经纪人", "en": "Insurance Broker", "isco": "3321", "onet": "41-3021.00", "locality": "global"},
    {"id": "0309", "mid": "insurance", "mid_zh": "保险", "mid_en": "Insurance",
     "zh": "损失评估师", "en": "Loss Adjuster", "isco": "3315", "onet": "13-1031.02", "locality": "global"},
    # ===== accounting_audit (10) =====
    {"id": "0401", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "注册会计师", "en": "Certified Public Accountant (CPA)", "isco": "2411", "onet": "13-2011.01", "locality": "global"},
    {"id": "0402", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "审计师", "en": "Auditor", "isco": "2411", "onet": "13-2011.02", "locality": "global"},
    {"id": "0403", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "税务师", "en": "Tax Advisor", "isco": "2411", "onet": "13-2082.00", "locality": "global"},
    {"id": "0404", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "管理会计师", "en": "Management Accountant", "isco": "2411", "onet": "13-2011.01", "locality": "global"},
    {"id": "0405", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "法务会计师", "en": "Forensic Accountant", "isco": "2411", "onet": "13-2011.01", "locality": "global"},
    {"id": "0406", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "会计文员", "en": "Bookkeeper / Accounting Clerk", "isco": "3313", "onet": "43-3031.00", "locality": "global"},
    {"id": "0407", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "内部审计师", "en": "Internal Auditor", "isco": "2411", "onet": "13-2011.02", "locality": "global"},
    {"id": "0408", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "财务分析师", "en": "Financial Analyst", "isco": "2411", "onet": "13-2051.00", "locality": "global"},
    {"id": "0409", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "出纳员", "en": "Cashier / Treasury Clerk", "isco": "4211", "onet": "43-3031.00", "locality": "global"},
    {"id": "0410", "mid": "accounting_audit", "mid_zh": "会计审计", "mid_en": "Accounting & Auditing",
     "zh": "ERP财务顾问", "en": "ERP Financial Consultant", "isco": "2411", "onet": "13-2011.01", "locality": "global"},
    # ===== consulting (8) =====
    {"id": "0501", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "战略咨询顾问", "en": "Strategy Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0502", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "IT咨询顾问", "en": "IT Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0503", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "人力资源咨询顾问", "en": "HR Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0504", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "运营咨询顾问", "en": "Operations Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0505", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "财务咨询顾问", "en": "Financial Advisory Consultant", "isco": "2412", "onet": "13-2052.00", "locality": "global"},
    {"id": "0506", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "ESG咨询顾问", "en": "ESG Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0507", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "数字化转型咨询顾问", "en": "Digital Transformation Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    {"id": "0508", "mid": "consulting", "mid_zh": "管理咨询", "mid_en": "Management Consulting",
     "zh": "供应链咨询顾问", "en": "Supply Chain Consultant", "isco": "2421", "onet": "13-1111.00", "locality": "global"},
    # ===== real_estate (7) =====
    {"id": "0601", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "房地产经纪人", "en": "Real Estate Agent", "isco": "3334", "onet": "41-9022.00", "locality": "global"},
    {"id": "0602", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "房地产估价师", "en": "Real Estate Appraiser", "isco": "3334", "onet": "13-2023.00", "locality": "global"},
    {"id": "0603", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "物业管理经理", "en": "Property Manager", "isco": "1346", "onet": "11-9141.00", "locality": "global"},
    {"id": "0604", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "土地规划师", "en": "Land Use Planner", "isco": "2164", "onet": "19-3051.00", "locality": "global"},
    {"id": "0605", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "房地产开发商", "en": "Real Estate Developer", "isco": "1120", "onet": "11-9021.00", "locality": "global"},
    {"id": "0606", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "REITs分析师", "en": "REIT Analyst", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "0607", "mid": "real_estate", "mid_zh": "房地产", "mid_en": "Real Estate",
     "zh": "商业地产经理", "en": "Commercial Real Estate Manager", "isco": "1346", "onet": "11-9141.00", "locality": "global"},
    # ===== islamic_finance (5) =====
    {"id": "0701", "mid": "islamic_finance", "mid_zh": "伊斯兰金融", "mid_en": "Islamic Finance",
     "zh": "伊斯兰教法合规分析师", "en": "Sharia Compliance Analyst", "isco": "2413", "onet": "13-2054.00", "locality": "regional"},
    {"id": "0702", "mid": "islamic_finance", "mid_zh": "伊斯兰金融", "mid_en": "Islamic Finance",
     "zh": "伊斯兰银行产品经理", "en": "Islamic Banking Product Manager", "isco": "1346", "onet": "11-3031.01", "locality": "regional"},
    {"id": "0703", "mid": "islamic_finance", "mid_zh": "伊斯兰金融", "mid_en": "Islamic Finance",
     "zh": "伊斯兰金融顾问", "en": "Islamic Finance Advisor", "isco": "2412", "onet": "13-2052.00", "locality": "regional"},
    {"id": "0704", "mid": "islamic_finance", "mid_zh": "伊斯兰金融", "mid_en": "Islamic Finance",
     "zh": "塔卡福尔(伊斯兰保险)专员", "en": "Takaful Specialist", "isco": "3321", "onet": "13-2053.00", "locality": "regional"},
    {"id": "0705", "mid": "islamic_finance", "mid_zh": "伊斯兰金融", "mid_en": "Islamic Finance",
     "zh": "穆拉巴哈融资专员", "en": "Murabaha Finance Specialist", "isco": "2412", "onet": "13-2052.00", "locality": "regional"},
    # ===== corporate_management (13) =====
    {"id": "0801", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席执行官(CEO)", "en": "Chief Executive Officer (CEO)", "isco": "1120", "onet": "11-1011.00", "locality": "global"},
    {"id": "0802", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席运营官(COO)", "en": "Chief Operating Officer (COO)", "isco": "1120", "onet": "11-1011.00", "locality": "global"},
    {"id": "0803", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席财务官(CFO)", "en": "Chief Financial Officer (CFO)", "isco": "1211", "onet": "11-3031.01", "locality": "global"},
    {"id": "0804", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席营销官(CMO)", "en": "Chief Marketing Officer (CMO)", "isco": "1221", "onet": "11-2021.00", "locality": "global"},
    {"id": "0805", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席信息官(CIO)", "en": "Chief Information Officer (CIO)", "isco": "1330", "onet": "11-3021.00", "locality": "global"},
    {"id": "0806", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "总经理", "en": "General Manager", "isco": "1120", "onet": "11-1021.00", "locality": "global"},
    {"id": "0807", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "企业家/创业者", "en": "Entrepreneur", "isco": "1120", "onet": "11-1011.00", "locality": "global"},
    {"id": "0808", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "董事会秘书", "en": "Corporate Secretary", "isco": "2421", "onet": "11-3012.00", "locality": "global"},
    {"id": "0809", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席技术官(CTO)", "en": "Chief Technology Officer (CTO)", "isco": "1330", "onet": "11-3021.00", "locality": "global"},
    {"id": "0810", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席人力资源官(CHRO)", "en": "Chief Human Resources Officer (CHRO)", "isco": "1212", "onet": "11-3121.00", "locality": "global"},
    {"id": "0811", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席数据官(CDO)", "en": "Chief Data Officer (CDO)", "isco": "1330", "onet": "11-3021.00", "locality": "global"},
    {"id": "0812", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "首席可持续发展官(CSO)", "en": "Chief Sustainability Officer (CSO)", "isco": "1120", "onet": "11-1011.00", "locality": "global"},
    {"id": "0813", "mid": "corporate_management", "mid_zh": "企业管理", "mid_en": "Corporate Management",
     "zh": "投资者关系总监", "en": "Investor Relations Director", "isco": "2422", "onet": "11-2031.00", "locality": "global"},
    # ===== human_resources (10) =====
    {"id": "0901", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "招聘专员", "en": "Recruiter", "isco": "2423", "onet": "13-1071.00", "locality": "global"},
    {"id": "0902", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "培训与发展经理", "en": "Training & Development Manager", "isco": "1212", "onet": "11-3131.00", "locality": "global"},
    {"id": "0903", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "薪酬福利经理", "en": "Compensation & Benefits Manager", "isco": "1212", "onet": "11-3111.00", "locality": "global"},
    {"id": "0904", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "HRBP(人力资源业务伙伴)", "en": "HR Business Partner", "isco": "2423", "onet": "13-1071.00", "locality": "global"},
    {"id": "0905", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "人力资源总监", "en": "HR Director", "isco": "1212", "onet": "11-3121.00", "locality": "global"},
    {"id": "0906", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "劳动关系专员", "en": "Labor Relations Specialist", "isco": "2423", "onet": "13-1075.00", "locality": "global"},
    {"id": "0907", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "猎头顾问", "en": "Executive Search Consultant / Headhunter", "isco": "2423", "onet": "13-1071.00", "locality": "global"},
    {"id": "0908", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "组织发展顾问", "en": "Organizational Development Consultant", "isco": "2423", "onet": "13-1111.00", "locality": "global"},
    {"id": "0909", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "员工关系专员", "en": "Employee Relations Specialist", "isco": "2423", "onet": "13-1071.00", "locality": "global"},
    {"id": "0910", "mid": "human_resources", "mid_zh": "人力资源", "mid_en": "Human Resources",
     "zh": "人才测评顾问", "en": "Talent Assessment Consultant", "isco": "2423", "onet": "13-1071.00", "locality": "global"},
    # ===== supply_chain (8) =====
    {"id": "1001", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "采购经理", "en": "Procurement Manager", "isco": "1324", "onet": "11-3061.00", "locality": "global"},
    {"id": "1002", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "供应链经理", "en": "Supply Chain Manager", "isco": "1324", "onet": "11-3071.01", "locality": "global"},
    {"id": "1003", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "国际贸易专员", "en": "International Trade Specialist", "isco": "2433", "onet": "13-1199.06", "locality": "global"},
    {"id": "1004", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "采购分析师", "en": "Procurement Analyst", "isco": "2413", "onet": "13-1023.00", "locality": "global"},
    {"id": "1005", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "供应链分析师", "en": "Supply Chain Analyst", "isco": "2413", "onet": "13-1081.01", "locality": "global"},
    {"id": "1006", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "合同管理专员", "en": "Contract Manager", "isco": "2421", "onet": "13-1023.00", "locality": "global"},
    {"id": "1007", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "进出口经理", "en": "Import/Export Manager", "isco": "1324", "onet": "11-3071.01", "locality": "global"},
    {"id": "1008", "mid": "supply_chain", "mid_zh": "供应链", "mid_en": "Supply Chain",
     "zh": "关务经理", "en": "Customs Compliance Manager", "isco": "1324", "onet": "13-1041.06", "locality": "global"},
    # ===== marketing_sales (8) =====
    {"id": "1101", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "市场营销经理", "en": "Marketing Manager", "isco": "1221", "onet": "11-2021.00", "locality": "global"},
    {"id": "1102", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "销售经理", "en": "Sales Manager", "isco": "1221", "onet": "11-2022.00", "locality": "global"},
    {"id": "1103", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "大客户经理", "en": "Key Account Manager", "isco": "2433", "onet": "41-4012.00", "locality": "global"},
    {"id": "1104", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "渠道经理", "en": "Channel Manager", "isco": "1221", "onet": "11-2022.00", "locality": "global"},
    {"id": "1105", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "商务拓展经理(BD)", "en": "Business Development Manager", "isco": "2433", "onet": "11-2021.00", "locality": "global"},
    {"id": "1106", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "CRM分析师", "en": "CRM Analyst", "isco": "2431", "onet": "13-1161.00", "locality": "global"},
    {"id": "1107", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "数字营销专员", "en": "Digital Marketing Specialist", "isco": "2431", "onet": "13-1161.00", "locality": "global"},
    {"id": "1108", "mid": "marketing_sales", "mid_zh": "市场营销与销售", "mid_en": "Marketing & Sales",
     "zh": "产品营销经理", "en": "Product Marketing Manager", "isco": "1221", "onet": "11-2021.00", "locality": "global"},
    # ===== crypto_defi (6) =====
    {"id": "1201", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "加密货币分析师", "en": "Cryptocurrency Analyst", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "1202", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "DeFi策略师", "en": "DeFi Strategist", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "1203", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "代币经济学设计师", "en": "Tokenomics Designer", "isco": "2413", "onet": "13-2051.00", "locality": "global"},
    {"id": "1204", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "智能合约审计师", "en": "Smart Contract Auditor", "isco": "2529", "onet": "15-1212.00", "locality": "global"},
    {"id": "1205", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "加密合规专员", "en": "Crypto Compliance Specialist", "isco": "2413", "onet": "13-1041.00", "locality": "global"},
    {"id": "1206", "mid": "crypto_defi", "mid_zh": "加密货币与去中心化金融", "mid_en": "Cryptocurrency & DeFi",
     "zh": "量化加密交易员", "en": "Quantitative Crypto Trader", "isco": "3311", "onet": "13-2051.00", "locality": "global"},
]

# ---------------------------------------------------------------------------
# COUNTRY METADATA (same 45 countries as TECH/MED)
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
# COUNTRY PROFILES — finance-specific modifiers
# (fin_center: financial center rank, bank_reg: banking regulation strength,
#  fintech: fintech maturity, ins_market: insurance market size,
#  re_market: real estate market maturity, islamic: islamic finance relevance,
#  stock_mkt: stock market size/depth, consult: consulting industry size,
#  comp: compensation level, wlb: work-life balance, ot: overtime culture,
#  gender: gender equality, edu: education quality, intl: international openness,
#  reg: regulatory environment)
# All on 0-10 scale.
# ---------------------------------------------------------------------------

COUNTRY_PROFILES = {
    # --- TOP FINANCIAL CENTERS ---
    "US": {"fin_center": 10.0, "bank_reg": 8.0, "fintech": 9.5, "ins_market": 9.5,
           "re_market": 9.0, "islamic": 1.0, "stock_mkt": 10.0, "consult": 10.0,
           "comp": 9.5, "wlb": 5.0, "ot": 4.0, "gender": 7.5, "edu": 9.0,
           "intl": 8.5, "reg": 7.5},
    "GB": {"fin_center": 9.5, "bank_reg": 8.5, "fintech": 9.0, "ins_market": 9.0,
           "re_market": 8.5, "islamic": 3.5, "stock_mkt": 9.0, "consult": 9.5,
           "comp": 8.5, "wlb": 6.5, "ot": 5.5, "gender": 7.5, "edu": 8.5,
           "intl": 9.0, "reg": 8.0},
    "HK": {"fin_center": 9.0, "bank_reg": 8.0, "fintech": 8.0, "ins_market": 7.5,
           "re_market": 9.5, "islamic": 1.5, "stock_mkt": 8.5, "consult": 7.5,
           "comp": 8.5, "wlb": 4.0, "ot": 3.0, "gender": 6.0, "edu": 7.5,
           "intl": 9.5, "reg": 7.5},
    "SG": {"fin_center": 9.0, "bank_reg": 8.5, "fintech": 9.0, "ins_market": 7.5,
           "re_market": 8.5, "islamic": 4.5, "stock_mkt": 7.5, "consult": 8.0,
           "comp": 8.5, "wlb": 5.0, "ot": 4.0, "gender": 7.0, "edu": 8.5,
           "intl": 9.5, "reg": 8.5},
    "CH": {"fin_center": 9.0, "bank_reg": 9.0, "fintech": 7.5, "ins_market": 8.5,
           "re_market": 8.0, "islamic": 1.5, "stock_mkt": 7.5, "consult": 8.5,
           "comp": 10.0, "wlb": 8.0, "ot": 7.0, "gender": 7.0, "edu": 9.0,
           "intl": 8.5, "reg": 8.5},
    # --- MAJOR DEVELOPED FINANCIAL MARKETS ---
    "JP": {"fin_center": 8.0, "bank_reg": 8.0, "fintech": 6.5, "ins_market": 9.0,
           "re_market": 8.5, "islamic": 1.0, "stock_mkt": 8.5, "consult": 7.5,
           "comp": 7.0, "wlb": 4.5, "ot": 3.0, "gender": 4.5, "edu": 8.0,
           "intl": 5.0, "reg": 7.5},
    "DE": {"fin_center": 7.5, "bank_reg": 8.5, "fintech": 7.0, "ins_market": 8.5,
           "re_market": 7.5, "islamic": 1.5, "stock_mkt": 7.5, "consult": 8.5,
           "comp": 7.5, "wlb": 8.0, "ot": 7.5, "gender": 7.0, "edu": 8.5,
           "intl": 8.0, "reg": 8.0},
    "FR": {"fin_center": 7.5, "bank_reg": 8.0, "fintech": 7.0, "ins_market": 8.0,
           "re_market": 7.5, "islamic": 2.0, "stock_mkt": 7.0, "consult": 8.0,
           "comp": 7.0, "wlb": 7.5, "ot": 7.0, "gender": 7.0, "edu": 8.0,
           "intl": 7.5, "reg": 8.0},
    "CA": {"fin_center": 7.5, "bank_reg": 9.0, "fintech": 7.5, "ins_market": 7.5,
           "re_market": 8.5, "islamic": 1.5, "stock_mkt": 7.5, "consult": 8.0,
           "comp": 7.5, "wlb": 7.0, "ot": 6.5, "gender": 8.0, "edu": 8.0,
           "intl": 9.0, "reg": 7.5},
    "AU": {"fin_center": 7.5, "bank_reg": 8.5, "fintech": 7.5, "ins_market": 7.5,
           "re_market": 8.5, "islamic": 1.5, "stock_mkt": 7.0, "consult": 7.5,
           "comp": 7.5, "wlb": 7.5, "ot": 7.0, "gender": 8.0, "edu": 8.0,
           "intl": 8.5, "reg": 7.5},
    "NL": {"fin_center": 7.0, "bank_reg": 8.0, "fintech": 7.5, "ins_market": 8.0,
           "re_market": 7.0, "islamic": 1.0, "stock_mkt": 6.5, "consult": 7.5,
           "comp": 7.5, "wlb": 9.0, "ot": 8.0, "gender": 8.5, "edu": 8.0,
           "intl": 9.0, "reg": 7.5},
    "NZ": {"fin_center": 5.5, "bank_reg": 7.5, "fintech": 6.5, "ins_market": 6.0,
           "re_market": 7.5, "islamic": 1.0, "stock_mkt": 4.5, "consult": 5.5,
           "comp": 6.5, "wlb": 8.5, "ot": 7.5, "gender": 8.5, "edu": 7.5,
           "intl": 8.0, "reg": 7.0},
    "IL": {"fin_center": 6.5, "bank_reg": 7.5, "fintech": 8.5, "ins_market": 6.5,
           "re_market": 7.0, "islamic": 0.5, "stock_mkt": 6.5, "consult": 7.0,
           "comp": 7.5, "wlb": 6.0, "ot": 5.0, "gender": 7.0, "edu": 8.5,
           "intl": 8.0, "reg": 7.0},
    # --- NORDIC ---
    "SE": {"fin_center": 6.5, "bank_reg": 7.5, "fintech": 8.0, "ins_market": 7.0,
           "re_market": 7.0, "islamic": 1.0, "stock_mkt": 6.5, "consult": 7.0,
           "comp": 7.0, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "edu": 8.5,
           "intl": 8.5, "reg": 7.5},
    "DK": {"fin_center": 6.0, "bank_reg": 7.5, "fintech": 7.5, "ins_market": 7.0,
           "re_market": 6.5, "islamic": 1.0, "stock_mkt": 6.0, "consult": 6.5,
           "comp": 7.0, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "edu": 8.5,
           "intl": 8.5, "reg": 7.5},
    "FI": {"fin_center": 5.5, "bank_reg": 7.0, "fintech": 7.5, "ins_market": 6.0,
           "re_market": 6.0, "islamic": 1.0, "stock_mkt": 5.5, "consult": 6.0,
           "comp": 6.5, "wlb": 9.0, "ot": 8.5, "gender": 9.0, "edu": 9.0,
           "intl": 8.0, "reg": 7.0},
    # --- EAST ASIA (non-center) ---
    "KR": {"fin_center": 7.0, "bank_reg": 7.5, "fintech": 7.5, "ins_market": 8.0,
           "re_market": 8.0, "islamic": 0.5, "stock_mkt": 7.5, "consult": 6.5,
           "comp": 7.0, "wlb": 4.0, "ot": 3.0, "gender": 4.0, "edu": 8.0,
           "intl": 6.0, "reg": 7.0},
    "TW": {"fin_center": 6.5, "bank_reg": 7.0, "fintech": 6.5, "ins_market": 8.5,
           "re_market": 7.5, "islamic": 0.5, "stock_mkt": 7.0, "consult": 5.5,
           "comp": 5.5, "wlb": 5.0, "ot": 4.0, "gender": 6.0, "edu": 7.5,
           "intl": 6.5, "reg": 6.5},
    # --- LARGE EMERGING FINANCIAL MARKETS ---
    "CN": {"fin_center": 8.0, "bank_reg": 7.0, "fintech": 9.5, "ins_market": 8.0,
           "re_market": 9.0, "islamic": 1.5, "stock_mkt": 8.5, "consult": 7.5,
           "comp": 7.0, "wlb": 3.5, "ot": 2.5, "gender": 5.5, "edu": 7.5,
           "intl": 5.0, "reg": 6.0},
    "IN": {"fin_center": 6.5, "bank_reg": 6.5, "fintech": 8.0, "ins_market": 6.0,
           "re_market": 7.0, "islamic": 2.0, "stock_mkt": 7.0, "consult": 7.0,
           "comp": 5.0, "wlb": 4.5, "ot": 3.5, "gender": 4.0, "edu": 7.0,
           "intl": 7.0, "reg": 5.5},
    "BR": {"fin_center": 6.0, "bank_reg": 6.5, "fintech": 7.0, "ins_market": 6.5,
           "re_market": 6.5, "islamic": 0.5, "stock_mkt": 6.5, "consult": 6.0,
           "comp": 5.0, "wlb": 5.5, "ot": 5.0, "gender": 5.5, "edu": 6.0,
           "intl": 5.0, "reg": 5.5},
    "RU": {"fin_center": 5.0, "bank_reg": 5.5, "fintech": 6.0, "ins_market": 5.0,
           "re_market": 5.5, "islamic": 2.0, "stock_mkt": 5.5, "consult": 5.0,
           "comp": 4.5, "wlb": 5.5, "ot": 5.0, "gender": 6.0, "edu": 7.0,
           "intl": 3.5, "reg": 4.5},
    # --- MIDDLE EAST ---
    "AE": {"fin_center": 8.0, "bank_reg": 7.5, "fintech": 8.0, "ins_market": 7.0,
           "re_market": 9.0, "islamic": 9.0, "stock_mkt": 7.0, "consult": 7.5,
           "comp": 8.5, "wlb": 5.5, "ot": 5.0, "gender": 5.0, "edu": 7.0,
           "intl": 9.0, "reg": 7.0},
    "SA": {"fin_center": 6.5, "bank_reg": 7.0, "fintech": 7.0, "ins_market": 6.5,
           "re_market": 7.5, "islamic": 9.5, "stock_mkt": 6.5, "consult": 6.5,
           "comp": 7.0, "wlb": 5.0, "ot": 5.0, "gender": 3.5, "edu": 6.0,
           "intl": 5.5, "reg": 6.0},
    "TR": {"fin_center": 5.5, "bank_reg": 6.0, "fintech": 6.0, "ins_market": 5.5,
           "re_market": 6.5, "islamic": 6.0, "stock_mkt": 5.5, "consult": 5.5,
           "comp": 4.0, "wlb": 5.0, "ot": 4.5, "gender": 4.5, "edu": 6.5,
           "intl": 5.5, "reg": 5.0},
    # --- SOUTHERN EUROPE ---
    "IT": {"fin_center": 6.0, "bank_reg": 7.5, "fintech": 5.5, "ins_market": 7.0,
           "re_market": 7.0, "islamic": 1.0, "stock_mkt": 6.0, "consult": 6.5,
           "comp": 5.5, "wlb": 6.5, "ot": 5.5, "gender": 5.5, "edu": 7.0,
           "intl": 6.5, "reg": 7.0},
    "ES": {"fin_center": 5.5, "bank_reg": 7.0, "fintech": 6.0, "ins_market": 6.5,
           "re_market": 7.0, "islamic": 1.0, "stock_mkt": 5.5, "consult": 6.0,
           "comp": 5.0, "wlb": 6.5, "ot": 5.5, "gender": 6.5, "edu": 7.0,
           "intl": 7.0, "reg": 6.5},
    "PT": {"fin_center": 4.5, "bank_reg": 6.5, "fintech": 5.5, "ins_market": 5.5,
           "re_market": 6.0, "islamic": 0.5, "stock_mkt": 4.0, "consult": 5.0,
           "comp": 4.5, "wlb": 6.5, "ot": 6.0, "gender": 7.0, "edu": 6.5,
           "intl": 7.5, "reg": 6.0},
    # --- EASTERN EUROPE ---
    "PL": {"fin_center": 5.0, "bank_reg": 6.5, "fintech": 6.5, "ins_market": 5.5,
           "re_market": 6.0, "islamic": 0.5, "stock_mkt": 5.0, "consult": 5.5,
           "comp": 5.5, "wlb": 6.5, "ot": 6.0, "gender": 6.5, "edu": 7.0,
           "intl": 7.5, "reg": 6.5},
    "CZ": {"fin_center": 4.5, "bank_reg": 6.5, "fintech": 6.0, "ins_market": 5.5,
           "re_market": 6.0, "islamic": 0.5, "stock_mkt": 4.5, "consult": 5.0,
           "comp": 5.5, "wlb": 7.5, "ot": 6.5, "gender": 6.5, "edu": 7.0,
           "intl": 7.0, "reg": 6.5},
    # --- SOUTHEAST ASIA ---
    "TH": {"fin_center": 5.0, "bank_reg": 6.0, "fintech": 6.0, "ins_market": 5.5,
           "re_market": 6.5, "islamic": 2.0, "stock_mkt": 5.5, "consult": 4.5,
           "comp": 3.5, "wlb": 5.5, "ot": 5.5, "gender": 6.0, "edu": 5.5,
           "intl": 5.0, "reg": 5.0},
    "VN": {"fin_center": 4.0, "bank_reg": 5.0, "fintech": 6.5, "ins_market": 4.0,
           "re_market": 6.0, "islamic": 0.5, "stock_mkt": 5.0, "consult": 3.5,
           "comp": 3.0, "wlb": 5.0, "ot": 4.5, "gender": 5.5, "edu": 5.5,
           "intl": 5.5, "reg": 4.5},
    "ID": {"fin_center": 4.5, "bank_reg": 5.5, "fintech": 7.0, "ins_market": 4.5,
           "re_market": 6.5, "islamic": 7.0, "stock_mkt": 5.5, "consult": 4.5,
           "comp": 3.5, "wlb": 5.0, "ot": 5.0, "gender": 4.5, "edu": 5.0,
           "intl": 4.5, "reg": 5.0},
    "MY": {"fin_center": 6.0, "bank_reg": 7.0, "fintech": 7.0, "ins_market": 6.0,
           "re_market": 6.5, "islamic": 8.5, "stock_mkt": 6.0, "consult": 5.5,
           "comp": 4.5, "wlb": 5.5, "ot": 5.0, "gender": 5.5, "edu": 6.5,
           "intl": 7.0, "reg": 6.0},
    "PH": {"fin_center": 4.0, "bank_reg": 5.5, "fintech": 5.5, "ins_market": 4.5,
           "re_market": 5.5, "islamic": 2.0, "stock_mkt": 4.5, "consult": 4.0,
           "comp": 3.0, "wlb": 5.0, "ot": 4.5, "gender": 6.5, "edu": 5.5,
           "intl": 6.5, "reg": 4.5},
    # --- SOUTH ASIA (developing) ---
    "PK": {"fin_center": 3.0, "bank_reg": 4.5, "fintech": 4.5, "ins_market": 3.0,
           "re_market": 5.0, "islamic": 8.0, "stock_mkt": 3.5, "consult": 3.0,
           "comp": 2.5, "wlb": 4.5, "ot": 4.0, "gender": 2.5, "edu": 4.5,
           "intl": 4.5, "reg": 3.5},
    "BD": {"fin_center": 2.5, "bank_reg": 4.0, "fintech": 5.0, "ins_market": 2.5,
           "re_market": 4.5, "islamic": 6.5, "stock_mkt": 3.0, "consult": 2.5,
           "comp": 2.0, "wlb": 4.0, "ot": 4.0, "gender": 3.0, "edu": 4.0,
           "intl": 4.5, "reg": 3.5},
    # --- LATIN AMERICA ---
    "MX": {"fin_center": 5.0, "bank_reg": 6.0, "fintech": 6.5, "ins_market": 5.5,
           "re_market": 6.5, "islamic": 0.5, "stock_mkt": 5.0, "consult": 5.0,
           "comp": 4.0, "wlb": 5.0, "ot": 4.5, "gender": 5.0, "edu": 5.5,
           "intl": 5.5, "reg": 5.0},
    "AR": {"fin_center": 4.0, "bank_reg": 4.5, "fintech": 5.5, "ins_market": 4.5,
           "re_market": 5.0, "islamic": 0.5, "stock_mkt": 3.5, "consult": 4.5,
           "comp": 3.5, "wlb": 5.5, "ot": 5.0, "gender": 5.5, "edu": 6.5,
           "intl": 5.0, "reg": 4.0},
    "CL": {"fin_center": 5.0, "bank_reg": 7.0, "fintech": 6.0, "ins_market": 5.5,
           "re_market": 6.0, "islamic": 0.5, "stock_mkt": 5.0, "consult": 5.0,
           "comp": 4.5, "wlb": 5.5, "ot": 5.5, "gender": 5.5, "edu": 6.5,
           "intl": 6.0, "reg": 6.0},
    "CO": {"fin_center": 4.0, "bank_reg": 5.5, "fintech": 5.5, "ins_market": 4.5,
           "re_market": 5.5, "islamic": 0.5, "stock_mkt": 4.0, "consult": 4.0,
           "comp": 3.5, "wlb": 5.0, "ot": 5.0, "gender": 5.0, "edu": 5.5,
           "intl": 5.0, "reg": 5.0},
    # --- AFRICA ---
    "ZA": {"fin_center": 6.0, "bank_reg": 7.0, "fintech": 6.5, "ins_market": 6.5,
           "re_market": 6.0, "islamic": 1.5, "stock_mkt": 6.5, "consult": 5.5,
           "comp": 4.5, "wlb": 5.5, "ot": 5.5, "gender": 5.5, "edu": 5.5,
           "intl": 6.0, "reg": 6.0},
    "NG": {"fin_center": 3.5, "bank_reg": 4.5, "fintech": 6.0, "ins_market": 3.0,
           "re_market": 5.0, "islamic": 4.0, "stock_mkt": 3.5, "consult": 3.5,
           "comp": 2.5, "wlb": 4.5, "ot": 4.5, "gender": 3.5, "edu": 4.0,
           "intl": 5.0, "reg": 3.5},
    "KE": {"fin_center": 4.0, "bank_reg": 5.0, "fintech": 7.0, "ins_market": 3.5,
           "re_market": 5.0, "islamic": 3.0, "stock_mkt": 3.5, "consult": 3.5,
           "comp": 2.5, "wlb": 5.0, "ot": 5.0, "gender": 4.5, "edu": 4.5,
           "intl": 5.5, "reg": 4.5},
    "EG": {"fin_center": 4.0, "bank_reg": 5.0, "fintech": 5.0, "ins_market": 3.5,
           "re_market": 6.0, "islamic": 6.5, "stock_mkt": 4.0, "consult": 3.5,
           "comp": 2.5, "wlb": 4.5, "ot": 4.5, "gender": 3.0, "edu": 5.0,
           "intl": 5.0, "reg": 4.0},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES — intrinsic characteristics of each FIN occupation
# ---------------------------------------------------------------------------

# Mid-category default profiles (used as template; individual occs override)
MID_DEFAULTS = {
    "banking": {
        "learning_cost": 5.0, "education_req": 5.5,
        "growth_coeff": 5.5, "career_lifespan": 7.5,
        "opportunity": 6.5, "market_size": 8.0, "supply_demand": 5.5, "developed_scarcity": 5.0,
        "value_added": 6.5, "cost_performance": 6.0,
        "stability": 7.0, "safety": 9.0, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.0,
        "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 1.5,
        "ai_resistance": 5.0, "social_status": 6.5, "remote_friendly": 5.0, "autonomy": 5.5,
        "family_friendly": 5.5, "fulfillment": 5.5, "entrepreneurship": 4.5, "gender_equality": 5.5,
        "age_flexibility": 6.0, "social_interaction": 7.0, "physical_demand": 1.0, "license_barrier": 4.0,
        "cycle_sensitivity": 5.0, "side_job_compat": 3.5, "intl_mobility": 6.0, "industry_monopoly": 4.5,
        "trend_long": 2, "trend_short": 0, "edu": "本科", "age": "22-28",
    },
    "securities_investment": {
        "learning_cost": 7.0, "education_req": 7.0,
        "growth_coeff": 7.0, "career_lifespan": 6.5,
        "opportunity": 7.5, "market_size": 6.5, "supply_demand": 6.5, "developed_scarcity": 6.5,
        "value_added": 8.0, "cost_performance": 7.0,
        "stability": 5.0, "safety": 9.0, "occupational_disease": 5.5, "overtime": 3.5, "burnout": 3.5,
        "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 2.5,
        "ai_resistance": 5.5, "social_status": 8.0, "remote_friendly": 6.5, "autonomy": 6.5,
        "family_friendly": 4.0, "fulfillment": 6.5, "entrepreneurship": 7.0, "gender_equality": 4.5,
        "age_flexibility": 5.0, "social_interaction": 7.0, "physical_demand": 0.5, "license_barrier": 5.5,
        "cycle_sensitivity": 7.5, "side_job_compat": 4.5, "intl_mobility": 7.5, "industry_monopoly": 4.0,
        "trend_long": 3, "trend_short": 1, "edu": "本科/硕士", "age": "22-28",
    },
    "insurance": {
        "learning_cost": 5.5, "education_req": 5.5,
        "growth_coeff": 5.5, "career_lifespan": 8.0,
        "opportunity": 6.0, "market_size": 7.0, "supply_demand": 5.5, "developed_scarcity": 5.0,
        "value_added": 6.0, "cost_performance": 6.0,
        "stability": 7.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 6.0, "burnout": 5.5,
        "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 2.0,
        "ai_resistance": 5.5, "social_status": 5.5, "remote_friendly": 5.5, "autonomy": 5.5,
        "family_friendly": 6.0, "fulfillment": 5.5, "entrepreneurship": 6.5, "gender_equality": 5.5,
        "age_flexibility": 6.5, "social_interaction": 7.0, "physical_demand": 1.0, "license_barrier": 5.0,
        "cycle_sensitivity": 4.0, "side_job_compat": 4.5, "intl_mobility": 5.5, "industry_monopoly": 4.5,
        "trend_long": 2, "trend_short": 1, "edu": "本科", "age": "22-28",
    },
    "accounting_audit": {
        "learning_cost": 6.0, "education_req": 6.0,
        "growth_coeff": 5.0, "career_lifespan": 8.5,
        "opportunity": 6.5, "market_size": 8.0, "supply_demand": 5.5, "developed_scarcity": 5.0,
        "value_added": 6.0, "cost_performance": 6.0,
        "stability": 7.5, "safety": 9.5, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 4.5,
        "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 1.5,
        "ai_resistance": 4.5, "social_status": 6.5, "remote_friendly": 6.5, "autonomy": 6.0,
        "family_friendly": 5.0, "fulfillment": 5.5, "entrepreneurship": 6.5, "gender_equality": 6.0,
        "age_flexibility": 6.5, "social_interaction": 6.5, "physical_demand": 0.5, "license_barrier": 7.0,
        "cycle_sensitivity": 3.5, "side_job_compat": 5.5, "intl_mobility": 7.0, "industry_monopoly": 3.5,
        "trend_long": 2, "trend_short": 0, "edu": "本科", "age": "22-28",
    },
    "consulting": {
        "learning_cost": 7.0, "education_req": 7.0,
        "growth_coeff": 6.5, "career_lifespan": 6.5,
        "opportunity": 7.0, "market_size": 6.0, "supply_demand": 6.0, "developed_scarcity": 6.0,
        "value_added": 7.5, "cost_performance": 6.5,
        "stability": 5.5, "safety": 9.5, "occupational_disease": 6.0, "overtime": 3.5, "burnout": 3.5,
        "skill_versatility": 8.0, "career_switch": 7.5, "reputation_variance": 2.0,
        "ai_resistance": 6.0, "social_status": 7.5, "remote_friendly": 6.5, "autonomy": 6.5,
        "family_friendly": 4.0, "fulfillment": 6.5, "entrepreneurship": 7.5, "gender_equality": 5.5,
        "age_flexibility": 5.0, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 2.5,
        "cycle_sensitivity": 6.0, "side_job_compat": 5.0, "intl_mobility": 8.0, "industry_monopoly": 3.5,
        "trend_long": 3, "trend_short": 1, "edu": "硕士", "age": "24-30",
    },
    "real_estate": {
        "learning_cost": 4.0, "education_req": 4.0,
        "growth_coeff": 5.0, "career_lifespan": 7.0,
        "opportunity": 6.5, "market_size": 7.5, "supply_demand": 4.5, "developed_scarcity": 3.5,
        "value_added": 6.0, "cost_performance": 6.5,
        "stability": 4.5, "safety": 9.0, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 5.0,
        "skill_versatility": 5.0, "career_switch": 5.0, "reputation_variance": 3.0,
        "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 4.5, "autonomy": 7.0,
        "family_friendly": 5.0, "fulfillment": 5.5, "entrepreneurship": 8.5, "gender_equality": 5.0,
        "age_flexibility": 6.5, "social_interaction": 8.0, "physical_demand": 3.0, "license_barrier": 4.5,
        "cycle_sensitivity": 8.5, "side_job_compat": 6.5, "intl_mobility": 4.5, "industry_monopoly": 2.5,
        "trend_long": 2, "trend_short": -1, "edu": "大专/本科", "age": "22-30",
    },
    "islamic_finance": {
        "learning_cost": 6.5, "education_req": 6.5,
        "growth_coeff": 6.5, "career_lifespan": 7.5,
        "opportunity": 5.5, "market_size": 4.0, "supply_demand": 6.0, "developed_scarcity": 5.0,
        "value_added": 6.5, "cost_performance": 6.0,
        "stability": 6.5, "safety": 9.0, "occupational_disease": 7.0, "overtime": 6.0, "burnout": 5.5,
        "skill_versatility": 4.5, "career_switch": 4.0, "reputation_variance": 2.0,
        "ai_resistance": 6.5, "social_status": 6.5, "remote_friendly": 5.0, "autonomy": 5.5,
        "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 5.5, "gender_equality": 4.0,
        "age_flexibility": 6.0, "social_interaction": 7.0, "physical_demand": 1.0, "license_barrier": 5.5,
        "cycle_sensitivity": 4.5, "side_job_compat": 4.0, "intl_mobility": 5.0, "industry_monopoly": 4.0,
        "trend_long": 3, "trend_short": 3, "edu": "本科/硕士", "age": "24-30",
    },
    "corporate_management": {
        "learning_cost": 8.0, "education_req": 7.5,
        "growth_coeff": 6.0, "career_lifespan": 7.0,
        "opportunity": 5.5, "market_size": 5.0, "supply_demand": 4.5, "developed_scarcity": 5.5,
        "value_added": 9.0, "cost_performance": 6.5,
        "stability": 5.0, "safety": 9.5, "occupational_disease": 5.5, "overtime": 3.0, "burnout": 3.5,
        "skill_versatility": 7.5, "career_switch": 5.5, "reputation_variance": 3.5,
        "ai_resistance": 7.5, "social_status": 9.0, "remote_friendly": 5.5, "autonomy": 9.0,
        "family_friendly": 3.5, "fulfillment": 7.5, "entrepreneurship": 9.0, "gender_equality": 4.5,
        "age_flexibility": 5.5, "social_interaction": 8.5, "physical_demand": 1.5, "license_barrier": 2.0,
        "cycle_sensitivity": 5.5, "side_job_compat": 3.0, "intl_mobility": 7.0, "industry_monopoly": 3.0,
        "trend_long": 2, "trend_short": 1, "edu": "硕士/MBA", "age": "30-40",
    },
    "human_resources": {
        "learning_cost": 4.5, "education_req": 5.0,
        "growth_coeff": 5.5, "career_lifespan": 7.5,
        "opportunity": 6.5, "market_size": 7.5, "supply_demand": 5.0, "developed_scarcity": 4.5,
        "value_added": 5.5, "cost_performance": 6.0,
        "stability": 6.5, "safety": 9.5, "occupational_disease": 7.5, "overtime": 6.0, "burnout": 5.5,
        "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 1.5,
        "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 6.5, "autonomy": 6.0,
        "family_friendly": 6.5, "fulfillment": 6.0, "entrepreneurship": 5.5, "gender_equality": 7.0,
        "age_flexibility": 6.5, "social_interaction": 8.5, "physical_demand": 1.0, "license_barrier": 2.5,
        "cycle_sensitivity": 5.0, "side_job_compat": 5.0, "intl_mobility": 6.0, "industry_monopoly": 2.5,
        "trend_long": 2, "trend_short": 1, "edu": "本科", "age": "22-28",
    },
    "supply_chain": {
        "learning_cost": 5.0, "education_req": 5.0,
        "growth_coeff": 6.0, "career_lifespan": 7.5,
        "opportunity": 6.5, "market_size": 7.0, "supply_demand": 6.0, "developed_scarcity": 5.5,
        "value_added": 6.0, "cost_performance": 6.5,
        "stability": 6.5, "safety": 9.0, "occupational_disease": 7.5, "overtime": 5.5, "burnout": 5.5,
        "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 1.5,
        "ai_resistance": 5.5, "social_status": 6.0, "remote_friendly": 5.5, "autonomy": 6.0,
        "family_friendly": 5.5, "fulfillment": 5.5, "entrepreneurship": 5.5, "gender_equality": 5.5,
        "age_flexibility": 6.0, "social_interaction": 7.0, "physical_demand": 2.0, "license_barrier": 3.0,
        "cycle_sensitivity": 5.5, "side_job_compat": 4.0, "intl_mobility": 7.0, "industry_monopoly": 3.0,
        "trend_long": 3, "trend_short": 2, "edu": "本科", "age": "22-28",
    },
    "marketing_sales": {
        "learning_cost": 4.0, "education_req": 4.5,
        "growth_coeff": 5.5, "career_lifespan": 7.0,
        "opportunity": 7.0, "market_size": 8.5, "supply_demand": 5.0, "developed_scarcity": 4.0,
        "value_added": 6.0, "cost_performance": 6.5,
        "stability": 5.0, "safety": 9.0, "occupational_disease": 7.0, "overtime": 4.5, "burnout": 4.5,
        "skill_versatility": 7.0, "career_switch": 6.5, "reputation_variance": 2.5,
        "ai_resistance": 5.5, "social_status": 6.0, "remote_friendly": 6.5, "autonomy": 6.5,
        "family_friendly": 5.0, "fulfillment": 6.0, "entrepreneurship": 7.5, "gender_equality": 6.0,
        "age_flexibility": 6.0, "social_interaction": 9.0, "physical_demand": 2.0, "license_barrier": 1.5,
        "cycle_sensitivity": 6.5, "side_job_compat": 6.0, "intl_mobility": 6.5, "industry_monopoly": 2.5,
        "trend_long": 2, "trend_short": 1, "edu": "本科", "age": "22-28",
    },
    "crypto_defi": {
        "learning_cost": 6.0, "education_req": 5.5,
        "growth_coeff": 7.5, "career_lifespan": 4.5,
        "opportunity": 7.0, "market_size": 4.0, "supply_demand": 7.0, "developed_scarcity": 7.0,
        "value_added": 7.5, "cost_performance": 6.5,
        "stability": 3.0, "safety": 9.0, "occupational_disease": 6.0, "overtime": 4.0, "burnout": 4.0,
        "skill_versatility": 6.5, "career_switch": 5.5, "reputation_variance": 4.0,
        "ai_resistance": 6.0, "social_status": 5.5, "remote_friendly": 9.0, "autonomy": 7.5,
        "family_friendly": 5.0, "fulfillment": 6.5, "entrepreneurship": 9.0, "gender_equality": 5.0,
        "age_flexibility": 6.5, "social_interaction": 5.5, "physical_demand": 0.5, "license_barrier": 1.5,
        "cycle_sensitivity": 9.0, "side_job_compat": 7.0, "intl_mobility": 8.0, "industry_monopoly": 2.0,
        "trend_long": 4, "trend_short": 2, "edu": "本科/自学", "age": "22-30",
    },
}

# Per-occupation overrides on top of mid-category defaults
OCC_OVERRIDES = {
    # ===== BANKING =====
    "0101": {"en_comment": "Bank Teller - low skill, declining due to automation",
             "learning_cost": 2.5, "education_req": 3.0, "value_added": 3.5,
             "ai_resistance": 2.5, "social_status": 4.0, "supply_demand": 3.5,
             "trend_short": -2, "trend_long": -1, "edu": "大专/本科", "age": "20-25"},
    "0102": {"en_comment": "Relationship Manager - sales-driven, moderate",
             "overtime": 4.5, "social_interaction": 8.5, "value_added": 6.5,
             "entrepreneurship": 5.5, "trend_short": 0},
    "0103": {"en_comment": "Credit Analyst - analytical, moderate AI risk",
             "ai_resistance": 4.5, "education_req": 6.0, "value_added": 6.0,
             "trend_short": 0},
    "0104": {"en_comment": "Risk Management - growing post-2008, in demand",
             "growth_coeff": 7.0, "supply_demand": 7.0, "value_added": 7.5,
             "developed_scarcity": 6.5, "ai_resistance": 6.0, "trend_short": 2},
    "0105": {"en_comment": "Compliance Officer - regulatory-driven growth",
             "growth_coeff": 7.0, "supply_demand": 7.0, "value_added": 7.0,
             "stability": 8.0, "ai_resistance": 6.0, "license_barrier": 5.5,
             "trend_short": 3, "trend_long": 4},
    "0106": {"en_comment": "Private Banker - high-net-worth, high comp",
             "value_added": 8.5, "social_status": 8.0, "comp": 8.5,
             "ai_resistance": 6.5, "social_interaction": 9.0,
             "supply_demand": 6.5, "entrepreneurship": 6.0, "trend_short": 1},
    "0107": {"en_comment": "Trade Finance - niche, international",
             "intl_mobility": 7.5, "supply_demand": 5.5},
    "0108": {"en_comment": "Branch Manager - leadership role, declining branches",
             "learning_cost": 6.0, "social_status": 7.0, "autonomy": 7.0,
             "value_added": 7.0, "trend_short": -1, "trend_long": 0,
             "edu": "本科/硕士", "age": "30-40"},
    "0109": {"en_comment": "Bank FX Trader - high stress, high pay",
             "value_added": 8.0, "overtime": 3.0, "burnout": 3.0,
             "cycle_sensitivity": 7.5, "ai_resistance": 4.5, "stability": 4.5},
    "0110": {"en_comment": "Credit Card BM - product management",
             "value_added": 6.5, "trend_short": 0},
    "0111": {"en_comment": "FinTech PM - tech+finance hybrid, hot",
             "learning_cost": 6.0, "growth_coeff": 8.0, "supply_demand": 7.5,
             "value_added": 8.0, "ai_resistance": 6.0, "remote_friendly": 7.5,
             "trend_short": 4, "trend_long": 4, "edu": "本科/硕士"},
    "0112": {"en_comment": "AML Analyst - regulatory compliance, growing",
             "growth_coeff": 7.0, "supply_demand": 7.0, "stability": 8.0,
             "ai_resistance": 5.5, "trend_short": 3},
    # ===== SECURITIES_INVESTMENT =====
    "0201": {"en_comment": "Equity Analyst - analytical, moderate AI risk",
             "ai_resistance": 4.5, "value_added": 7.5},
    "0202": {"en_comment": "Fund Manager - high comp, high pressure",
             "value_added": 9.5, "social_status": 9.0, "overtime": 3.0,
             "burnout": 3.0, "stability": 4.5, "cycle_sensitivity": 8.0,
             "supply_demand": 5.5, "fulfillment": 7.0, "trend_short": 1},
    "0203": {"en_comment": "IB Analyst - extreme hours, high pay, prestigious",
             "learning_cost": 7.5, "value_added": 9.0, "overtime": 1.5,
             "burnout": 2.0, "social_status": 8.5, "family_friendly": 2.0,
             "stability": 4.5, "cycle_sensitivity": 8.0, "fulfillment": 5.5,
             "supply_demand": 6.0, "ai_resistance": 5.0, "trend_short": 0},
    "0204": {"en_comment": "PE Manager - very high comp, selective",
             "value_added": 9.5, "social_status": 9.0, "overtime": 2.5,
             "burnout": 2.5, "opportunity": 5.5, "market_size": 4.0,
             "supply_demand": 5.0, "developed_scarcity": 6.0, "fulfillment": 7.0,
             "ai_resistance": 6.5, "edu": "硕士/MBA", "age": "26-32"},
    "0205": {"en_comment": "VC - high opportunity, startup ecosystem",
             "value_added": 9.0, "social_status": 8.5, "overtime": 3.0,
             "burnout": 3.5, "opportunity": 6.0, "market_size": 3.5,
             "entrepreneurship": 9.5, "ai_resistance": 7.5, "fulfillment": 8.0,
             "supply_demand": 5.0, "edu": "硕士/MBA", "age": "28-35"},
    "0206": {"en_comment": "Quant Trader - math-heavy, tech-driven, very high comp",
             "learning_cost": 8.5, "education_req": 8.5, "value_added": 10.0,
             "overtime": 3.0, "burnout": 3.0, "ai_resistance": 6.5,
             "supply_demand": 8.0, "developed_scarcity": 8.5, "stability": 4.5,
             "remote_friendly": 7.5, "gender_equality": 3.5,
             "edu": "硕士/博士", "age": "24-30"},
    "0207": {"en_comment": "Fixed Income Analyst - steady, institutional",
             "value_added": 7.5, "stability": 5.5},
    "0208": {"en_comment": "Stockbroker - declining due to online trading",
             "learning_cost": 4.5, "education_req": 4.5, "value_added": 5.5,
             "ai_resistance": 3.5, "trend_short": -2, "trend_long": -1,
             "social_status": 5.5, "supply_demand": 4.0},
    "0209": {"en_comment": "Forex Trader - high volatility, shrinking retail",
             "value_added": 7.0, "stability": 4.0, "cycle_sensitivity": 8.5,
             "burnout": 3.0, "overtime": 3.0},
    "0210": {"en_comment": "Wealth Management Advisor - HNW segment growing",
             "value_added": 8.0, "social_interaction": 8.5, "social_status": 7.5,
             "ai_resistance": 6.5, "entrepreneurship": 7.5, "trend_short": 2},
    "0211": {"en_comment": "Trust Manager - niche, stable",
             "value_added": 7.0, "stability": 6.5, "market_size": 4.5,
             "supply_demand": 5.5},
    "0212": {"en_comment": "Derivatives Trader - complex products",
             "learning_cost": 8.0, "education_req": 7.5, "value_added": 9.0,
             "overtime": 2.5, "burnout": 2.5, "cycle_sensitivity": 8.5,
             "ai_resistance": 5.0, "stability": 4.0},
    "0213": {"en_comment": "Commodity Futures Trader - cyclical, volatile",
             "value_added": 7.5, "cycle_sensitivity": 9.0, "stability": 4.0,
             "burnout": 3.0, "overtime": 3.0},
    "0214": {"en_comment": "Portfolio Analyst - quantitative support role",
             "learning_cost": 6.5, "value_added": 7.0, "ai_resistance": 4.5},
    "0215": {"en_comment": "Asset Manager - institutional, high AUM",
             "value_added": 8.5, "social_status": 8.0, "supply_demand": 5.5,
             "ai_resistance": 6.0, "edu": "硕士", "age": "26-32"},
    # ===== INSURANCE =====
    "0301": {"en_comment": "Actuary - rare skill, high stability, math-heavy",
             "learning_cost": 8.5, "education_req": 8.0, "value_added": 8.0,
             "supply_demand": 7.5, "developed_scarcity": 7.5, "stability": 8.5,
             "ai_resistance": 6.5, "social_status": 7.5, "license_barrier": 8.5,
             "gender_equality": 5.0, "trend_short": 2, "fulfillment": 7.0,
             "edu": "本科/硕士(精算)", "age": "24-28"},
    "0302": {"en_comment": "Insurance Agent - sales-driven, high turnover",
             "learning_cost": 3.0, "education_req": 3.0, "value_added": 4.5,
             "stability": 4.5, "ai_resistance": 5.0, "social_status": 4.0,
             "entrepreneurship": 8.0, "reputation_variance": 3.0,
             "supply_demand": 4.0, "side_job_compat": 6.5, "trend_short": -1,
             "edu": "大专/本科", "age": "20-35"},
    "0303": {"en_comment": "Claims Adjuster - field work, moderate",
             "ai_resistance": 5.0, "remote_friendly": 4.0, "physical_demand": 3.0},
    "0304": {"en_comment": "Actuarial Analyst - junior actuary path",
             "learning_cost": 7.5, "education_req": 7.0, "value_added": 7.0,
             "supply_demand": 7.0, "ai_resistance": 6.0, "license_barrier": 7.5,
             "edu": "本科/硕士", "age": "22-26"},
    "0305": {"en_comment": "Underwriter - judgment-heavy, AI threat moderate",
             "ai_resistance": 5.0, "value_added": 6.5},
    "0306": {"en_comment": "Reinsurance Specialist - niche, international",
             "value_added": 7.0, "intl_mobility": 7.5, "market_size": 3.5,
             "supply_demand": 6.0},
    "0307": {"en_comment": "Insurance Product Developer - analytical",
             "learning_cost": 6.5, "value_added": 7.0, "ai_resistance": 5.5},
    "0308": {"en_comment": "Insurance Broker - independent, sales",
             "entrepreneurship": 8.0, "autonomy": 7.0, "value_added": 6.5,
             "side_job_compat": 5.5},
    "0309": {"en_comment": "Loss Adjuster - field investigative work",
             "ai_resistance": 6.0, "physical_demand": 3.5, "remote_friendly": 3.5},
    # ===== ACCOUNTING_AUDIT =====
    "0401": {"en_comment": "CPA - gold-standard license, stable",
             "license_barrier": 8.5, "social_status": 7.5, "value_added": 7.0,
             "stability": 8.0, "supply_demand": 6.0, "ai_resistance": 5.0,
             "entrepreneurship": 7.5, "intl_mobility": 7.5, "trend_short": 0},
    "0402": {"en_comment": "Auditor - busy season extreme hours",
             "overtime": 3.0, "burnout": 3.0, "value_added": 6.5,
             "stability": 7.5, "family_friendly": 3.5, "trend_short": 0},
    "0403": {"en_comment": "Tax Advisor - complex, always in demand",
             "value_added": 7.0, "ai_resistance": 5.5, "supply_demand": 6.0,
             "license_barrier": 7.5, "entrepreneurship": 7.5, "trend_short": 1},
    "0404": {"en_comment": "Management Accountant - internal, strategic",
             "value_added": 6.5, "remote_friendly": 7.0, "overtime": 5.5,
             "burnout": 5.5, "family_friendly": 6.0},
    "0405": {"en_comment": "Forensic Accountant - niche, investigative",
             "learning_cost": 7.0, "value_added": 7.5, "supply_demand": 6.5,
             "ai_resistance": 6.5, "fulfillment": 7.0, "market_size": 3.5,
             "social_status": 7.0},
    "0406": {"en_comment": "Bookkeeper - low barrier, high AI risk",
             "learning_cost": 2.5, "education_req": 2.5, "value_added": 3.5,
             "ai_resistance": 2.5, "social_status": 4.0, "supply_demand": 3.5,
             "license_barrier": 2.5, "trend_short": -2, "trend_long": -1,
             "edu": "大专/自学", "age": "20-30"},
    "0407": {"en_comment": "Internal Auditor - corporate governance",
             "value_added": 6.5, "stability": 7.5, "overtime": 5.0,
             "family_friendly": 5.5},
    "0408": {"en_comment": "Financial Analyst - broad, versatile",
             "learning_cost": 6.5, "value_added": 7.0, "supply_demand": 6.0,
             "skill_versatility": 7.5, "career_switch": 7.0, "ai_resistance": 4.5,
             "remote_friendly": 7.0, "edu": "本科/硕士", "age": "22-28"},
    "0409": {"en_comment": "Cashier/Treasury Clerk - declining, automatable",
             "learning_cost": 2.0, "education_req": 2.0, "value_added": 3.0,
             "ai_resistance": 2.0, "social_status": 3.5, "supply_demand": 3.0,
             "license_barrier": 1.5, "trend_short": -3, "trend_long": -2,
             "edu": "高中/大专", "age": "18-25"},
    "0410": {"en_comment": "ERP Financial Consultant - tech+accounting",
             "learning_cost": 6.5, "value_added": 7.5, "supply_demand": 6.5,
             "ai_resistance": 5.5, "remote_friendly": 7.5, "intl_mobility": 7.5,
             "trend_short": 2, "edu": "本科/硕士"},
    # ===== CONSULTING =====
    "0501": {"en_comment": "Strategy Consultant - MBB tier, prestigious",
             "value_added": 9.0, "social_status": 9.0, "overtime": 2.5,
             "burnout": 2.5, "fulfillment": 7.5, "supply_demand": 5.5,
             "edu": "硕士/MBA", "age": "24-30"},
    "0502": {"en_comment": "IT Consultant - tech transformation demand",
             "value_added": 7.5, "supply_demand": 7.0, "growth_coeff": 7.5,
             "remote_friendly": 7.5, "trend_short": 3},
    "0503": {"en_comment": "HR Consultant - moderate, stable",
             "value_added": 6.5, "gender_equality": 7.0},
    "0504": {"en_comment": "Operations Consultant - process improvement",
             "value_added": 7.0, "ai_resistance": 5.5},
    "0505": {"en_comment": "Financial Advisory - M&A, restructuring",
             "value_added": 8.5, "overtime": 3.0, "burnout": 3.0,
             "cycle_sensitivity": 7.0, "fulfillment": 7.0},
    "0506": {"en_comment": "ESG Consultant - fast growing, new field",
             "growth_coeff": 8.5, "supply_demand": 7.5, "value_added": 7.0,
             "trend_short": 5, "trend_long": 5, "fulfillment": 7.5,
             "market_size": 4.5},
    "0507": {"en_comment": "Digital Transformation - tech-savvy consulting",
             "growth_coeff": 8.0, "supply_demand": 7.5, "value_added": 8.0,
             "remote_friendly": 7.5, "trend_short": 4, "trend_long": 4},
    "0508": {"en_comment": "Supply Chain Consultant - post-COVID demand surge",
             "supply_demand": 7.0, "growth_coeff": 7.0, "trend_short": 3},
    # ===== REAL_ESTATE =====
    "0601": {"en_comment": "Real Estate Agent - cyclical, commission-based",
             "entrepreneurship": 9.0, "value_added": 5.5, "stability": 3.5,
             "ai_resistance": 5.5, "side_job_compat": 7.0,
             "license_barrier": 4.0},
    "0602": {"en_comment": "Appraiser - licensed, moderate stability",
             "license_barrier": 6.5, "ai_resistance": 5.5, "stability": 6.0,
             "value_added": 5.5},
    "0603": {"en_comment": "Property Manager - hands-on, stable income",
             "stability": 6.5, "remote_friendly": 3.5, "ai_resistance": 6.5,
             "value_added": 5.5, "physical_demand": 3.5},
    "0604": {"en_comment": "Land Use Planner - public/private, steady",
             "learning_cost": 6.0, "education_req": 6.0, "stability": 7.0,
             "ai_resistance": 7.0, "value_added": 6.0, "cycle_sensitivity": 5.5,
             "fulfillment": 7.0, "edu": "本科/硕士", "age": "24-30"},
    "0605": {"en_comment": "Real Estate Developer - high risk, high reward",
             "learning_cost": 7.0, "value_added": 9.0, "entrepreneurship": 10.0,
             "stability": 3.0, "cycle_sensitivity": 9.5, "burnout": 3.5,
             "social_status": 7.5, "ai_resistance": 7.5, "reputation_variance": 4.0,
             "edu": "本科/硕士", "age": "30-40"},
    "0606": {"en_comment": "REIT Analyst - finance+real estate hybrid",
             "learning_cost": 6.5, "education_req": 6.5, "value_added": 7.5,
             "remote_friendly": 7.0, "ai_resistance": 5.0,
             "edu": "本科/硕士", "age": "24-28"},
    "0607": {"en_comment": "Commercial RE Manager - institutional, steady",
             "value_added": 7.0, "stability": 5.5, "social_interaction": 8.5,
             "intl_mobility": 5.5, "edu": "本科/硕士", "age": "28-35"},
    # ===== ISLAMIC_FINANCE =====
    "0701": {"en_comment": "Sharia Compliance - unique niche, religious expertise",
             "ai_resistance": 7.5, "supply_demand": 6.5, "license_barrier": 7.0,
             "fulfillment": 7.0},
    "0702": {"en_comment": "Islamic Banking PM - growing in ME/MY/ID",
             "value_added": 7.0, "growth_coeff": 7.0, "supply_demand": 6.5},
    "0703": {"en_comment": "Islamic Finance Advisor - advisory, client-facing",
             "social_interaction": 8.0, "value_added": 7.0},
    "0704": {"en_comment": "Takaful Specialist - Islamic insurance niche",
             "market_size": 3.0, "supply_demand": 5.5},
    "0705": {"en_comment": "Murabaha Finance - trade finance, Islamic",
             "market_size": 3.0, "intl_mobility": 4.5},
    # ===== CORPORATE_MANAGEMENT =====
    "0801": {"en_comment": "CEO - highest executive, highest comp",
             "value_added": 10.0, "social_status": 10.0, "overtime": 2.0,
             "burnout": 2.5, "stability": 4.0, "fulfillment": 8.5,
             "reputation_variance": 4.5, "supply_demand": 3.5,
             "education_req": 8.5, "edu": "硕士/MBA/博士", "age": "35-50"},
    "0802": {"en_comment": "COO - operations leadership",
             "value_added": 9.5, "social_status": 9.0, "overtime": 2.5,
             "supply_demand": 3.5, "edu": "硕士/MBA", "age": "33-45"},
    "0803": {"en_comment": "CFO - finance leadership, high demand",
             "value_added": 9.5, "social_status": 9.5, "supply_demand": 5.0,
             "license_barrier": 4.0, "edu": "硕士/MBA/CPA", "age": "32-45"},
    "0804": {"en_comment": "CMO - marketing leadership, digital shift",
             "value_added": 9.0, "trend_short": 1, "cycle_sensitivity": 6.0,
             "edu": "硕士/MBA", "age": "32-45"},
    "0805": {"en_comment": "CIO - tech leadership, rising importance",
             "value_added": 9.0, "trend_short": 3, "growth_coeff": 7.0,
             "supply_demand": 6.0, "edu": "硕士/MBA", "age": "32-45"},
    "0806": {"en_comment": "General Manager - broad, common",
             "value_added": 8.0, "supply_demand": 5.0, "social_status": 7.5,
             "edu": "本科/硕士", "age": "30-40"},
    "0807": {"en_comment": "Entrepreneur - extreme risk/reward",
             "value_added": 8.5, "stability": 2.5, "entrepreneurship": 10.0,
             "autonomy": 10.0, "cycle_sensitivity": 8.0, "burnout": 2.5,
             "reputation_variance": 5.0, "license_barrier": 1.0,
             "fulfillment": 9.0, "supply_demand": 3.0,
             "edu": "不限", "age": "22-40"},
    "0808": {"en_comment": "Corporate Secretary - governance, compliance",
             "value_added": 7.0, "stability": 7.0, "social_status": 7.0,
             "license_barrier": 5.0, "overtime": 5.0},
    "0809": {"en_comment": "CTO - tech leadership at executive level",
             "value_added": 9.5, "trend_short": 3, "growth_coeff": 7.5,
             "supply_demand": 6.5, "edu": "硕士/博士", "age": "30-42"},
    "0810": {"en_comment": "CHRO - people leadership",
             "value_added": 8.5, "gender_equality": 6.0, "social_status": 8.0,
             "edu": "硕士/MBA", "age": "35-45"},
    "0811": {"en_comment": "CDO - data leadership, new role",
             "value_added": 9.0, "growth_coeff": 8.0, "supply_demand": 7.0,
             "trend_short": 4, "trend_long": 4, "edu": "硕士/博士", "age": "30-42"},
    "0812": {"en_comment": "CSO - sustainability, fast-growing",
             "value_added": 8.0, "growth_coeff": 8.5, "supply_demand": 7.0,
             "trend_short": 5, "trend_long": 5, "fulfillment": 8.5,
             "market_size": 3.5, "edu": "硕士/MBA", "age": "32-45"},
    "0813": {"en_comment": "IR Director - capital markets communications",
             "value_added": 7.5, "social_interaction": 8.5,
             "intl_mobility": 7.5, "market_size": 3.5},
    # ===== HUMAN_RESOURCES =====
    "0901": {"en_comment": "Recruiter - cyclical, people-oriented",
             "ai_resistance": 5.0, "cycle_sensitivity": 7.0, "stability": 5.0,
             "fulfillment": 5.5, "trend_short": 0},
    "0902": {"en_comment": "T&D Manager - development focus",
             "value_added": 6.0, "fulfillment": 7.0, "learning_cost": 5.5,
             "edu": "本科/硕士", "age": "28-35"},
    "0903": {"en_comment": "Comp & Benefits Manager - analytical HR",
             "value_added": 6.5, "ai_resistance": 5.0, "learning_cost": 5.5,
             "edu": "本科/硕士"},
    "0904": {"en_comment": "HRBP - strategic HR, growing role",
             "value_added": 6.5, "supply_demand": 6.0, "growth_coeff": 6.5,
             "trend_short": 2},
    "0905": {"en_comment": "HR Director - executive HR leadership",
             "value_added": 7.5, "social_status": 7.5, "overtime": 4.5,
             "edu": "硕士", "age": "32-42"},
    "0906": {"en_comment": "Labor Relations - legal + HR, steady",
             "ai_resistance": 6.5, "license_barrier": 3.5, "stability": 7.0},
    "0907": {"en_comment": "Headhunter - commission-driven, volatile",
             "value_added": 7.0, "entrepreneurship": 8.0, "stability": 4.5,
             "cycle_sensitivity": 7.5, "side_job_compat": 6.0,
             "burnout": 4.0, "overtime": 4.0},
    "0908": {"en_comment": "OD Consultant - organizational change",
             "value_added": 7.0, "learning_cost": 6.5, "education_req": 6.5,
             "fulfillment": 7.5, "edu": "硕士", "age": "28-35"},
    "0909": {"en_comment": "Employee Relations - mediation, compliance",
             "ai_resistance": 6.5, "stability": 7.0, "fulfillment": 6.0},
    "0910": {"en_comment": "Talent Assessment - IO psychology niche",
             "learning_cost": 6.0, "education_req": 6.0, "value_added": 6.5,
             "market_size": 4.0, "supply_demand": 5.5,
             "edu": "本科/硕士", "age": "26-32"},
    # ===== SUPPLY_CHAIN =====
    "1001": {"en_comment": "Procurement Manager - negotiation + strategy",
             "value_added": 6.5, "autonomy": 7.0, "social_interaction": 7.5,
             "edu": "本科/硕士", "age": "28-35"},
    "1002": {"en_comment": "Supply Chain Manager - end-to-end, growing",
             "value_added": 7.0, "supply_demand": 7.0, "growth_coeff": 7.0,
             "trend_short": 3, "edu": "本科/硕士", "age": "28-35"},
    "1003": {"en_comment": "International Trade - globalization sensitive",
             "intl_mobility": 8.5, "cycle_sensitivity": 6.5},
    "1004": {"en_comment": "Procurement Analyst - data + procurement",
             "ai_resistance": 4.5, "value_added": 5.5},
    "1005": {"en_comment": "Supply Chain Analyst - analytics-driven",
             "ai_resistance": 5.0, "value_added": 6.0, "remote_friendly": 6.5,
             "growth_coeff": 6.5, "trend_short": 2},
    "1006": {"en_comment": "Contract Manager - legal + commercial",
             "ai_resistance": 6.0, "license_barrier": 3.5, "stability": 7.0},
    "1007": {"en_comment": "Import/Export Manager - trade operations",
             "intl_mobility": 8.0, "value_added": 6.5},
    "1008": {"en_comment": "Customs Compliance Manager - regulatory",
             "license_barrier": 5.0, "stability": 7.5, "ai_resistance": 6.0},
    # ===== MARKETING_SALES =====
    "1101": {"en_comment": "Marketing Manager - strategic, brand-driven",
             "value_added": 7.0, "ai_resistance": 5.5, "fulfillment": 6.5,
             "edu": "本科/硕士", "age": "26-32"},
    "1102": {"en_comment": "Sales Manager - target-driven, high pressure",
             "value_added": 7.0, "overtime": 3.5, "burnout": 4.0,
             "entrepreneurship": 8.0, "stability": 4.5,
             "cycle_sensitivity": 7.0},
    "1103": {"en_comment": "Key Account Manager - relationship-heavy",
             "social_interaction": 9.5, "value_added": 7.0,
             "ai_resistance": 6.5, "stability": 5.5},
    "1104": {"en_comment": "Channel Manager - distribution strategy",
             "value_added": 6.5, "social_interaction": 8.5},
    "1105": {"en_comment": "BD Manager - deal-making, growth-oriented",
             "value_added": 7.0, "entrepreneurship": 8.5, "overtime": 4.0,
             "cycle_sensitivity": 7.0, "fulfillment": 6.5},
    "1106": {"en_comment": "CRM Analyst - data-driven marketing",
             "learning_cost": 5.0, "ai_resistance": 4.5, "remote_friendly": 7.5,
             "value_added": 6.0, "trend_short": 2},
    "1107": {"en_comment": "Digital Marketing - fast-growing, accessible",
             "learning_cost": 3.5, "growth_coeff": 7.5, "supply_demand": 6.5,
             "remote_friendly": 8.5, "side_job_compat": 8.0,
             "entrepreneurship": 8.5, "trend_short": 3, "trend_long": 4,
             "ai_resistance": 4.5, "edu": "本科/自学", "age": "20-28"},
    "1108": {"en_comment": "Product Marketing Manager - tech-adjacent",
             "value_added": 7.0, "learning_cost": 5.0, "supply_demand": 6.0,
             "trend_short": 2, "edu": "本科/硕士"},
    # ===== CRYPTO_DEFI =====
    "1201": {"en_comment": "Crypto Analyst - volatile sector, growing",
             "stability": 3.0, "value_added": 7.0, "trend_short": 2},
    "1202": {"en_comment": "DeFi Strategist - cutting edge, niche",
             "value_added": 8.0, "market_size": 3.0, "supply_demand": 7.5,
             "stability": 2.5, "trend_short": 3},
    "1203": {"en_comment": "Tokenomics Designer - game theory + economics",
             "learning_cost": 7.0, "education_req": 6.5, "value_added": 8.0,
             "market_size": 2.5, "supply_demand": 7.5, "stability": 2.5},
    "1204": {"en_comment": "Smart Contract Auditor - security + blockchain",
             "learning_cost": 7.5, "education_req": 6.5, "value_added": 9.0,
             "supply_demand": 8.5, "ai_resistance": 6.5, "stability": 3.5,
             "trend_short": 4, "edu": "本科/硕士"},
    "1205": {"en_comment": "Crypto Compliance - regulatory + crypto",
             "supply_demand": 7.0, "growth_coeff": 8.0, "stability": 4.0,
             "license_barrier": 3.5, "trend_short": 4},
    "1206": {"en_comment": "Quantitative Crypto Trader - math + crypto",
             "learning_cost": 8.0, "education_req": 7.5, "value_added": 9.5,
             "supply_demand": 7.5, "stability": 2.5, "burnout": 3.0,
             "overtime": 3.0, "edu": "硕士/博士"},
}


def occ_base(occ_id, mid_cat):
    """Return base scores for an occupation, merging mid defaults + overrides."""
    defaults = MID_DEFAULTS.get(mid_cat, {})
    if not defaults:
        return {}
    base = dict(defaults)
    overrides = OCC_OVERRIDES.get(occ_id, {})
    for k, v in overrides.items():
        if k != "en_comment":
            base[k] = v
    return base


# ---------------------------------------------------------------------------
# COUNTRY-ADAPTIVE SCORING
# ---------------------------------------------------------------------------

def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))


def apply_country_modifiers(base_scores, country_profile, occ_id, mid_cat):
    """Adjust base scores based on finance country profile."""
    cp = country_profile
    s = dict(base_scores)

    # Financial center rank influences many dimensions
    fin_factor = (cp["fin_center"] - 6.0) / 4.0  # normalized ~-1 to +1

    # Compensation: strongly affected by country compensation level
    comp_factor = (cp["comp"] - 5.5) / 4.5
    s["value_added"] = clamp(s["value_added"] + comp_factor * 2.0)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_factor * 1.0 + fin_factor * 0.5)

    # Growth coefficient: financial center + fintech maturity
    fintech_factor = (cp["fintech"] - 6.0) / 4.0
    s["growth_coeff"] = clamp(s["growth_coeff"] + fin_factor * 0.5 + fintech_factor * 0.5)

    # Career lifespan: more stable in well-regulated markets
    reg_factor = (cp["reg"] - 6.0) / 4.0
    s["career_lifespan"] = clamp(s["career_lifespan"] + reg_factor * 0.5 + fin_factor * 0.3)

    # Opportunity: financial center + market size proxy
    s["opportunity"] = clamp(s["opportunity"] + fin_factor * 1.0 + fintech_factor * 0.3)

    # Market size: directly correlated with financial center rank
    s["market_size"] = clamp(s["market_size"] + fin_factor * 1.5)

    # Supply-demand: higher in top financial centers
    s["supply_demand"] = clamp(s["supply_demand"] + fin_factor * 0.8)

    # Developed scarcity
    dev_bonus = 1.0 if cp["fin_center"] >= 7.5 else (0.0 if cp["fin_center"] >= 5.0 else -1.0)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus * 0.8)

    # Stability: banking regulation strength matters
    bank_reg_factor = (cp["bank_reg"] - 6.0) / 4.0
    s["stability"] = clamp(s["stability"] + bank_reg_factor * 1.0 + reg_factor * 0.5)

    # Safety: generally high for finance, slight variation
    s["safety"] = clamp(s["safety"] + reg_factor * 0.2)

    # Occupational disease: worse in countries with poor work-life balance
    wlb_factor = (cp["wlb"] - 6.0) / 4.0
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_factor * 0.8)

    # Overtime: strongly affected by financial center work culture
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)

    # Burnout: overtime culture + financial pressure
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)

    # Remote friendly: varies by country, finance is moderate
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_factor * 0.5 + fintech_factor * 0.3)

    # Autonomy: related to workplace culture
    s["autonomy"] = clamp(s["autonomy"] + wlb_factor * 0.3 + fin_factor * 0.2)

    # Family friendly: work-life balance culture
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_factor * 1.5)

    # Social status: higher in countries where finance is prestigious
    s["social_status"] = clamp(s["social_status"] + fin_factor * 0.8 + comp_factor * 0.5)

    # Fulfillment: slightly better in more developed financial markets
    s["fulfillment"] = clamp(s["fulfillment"] + fin_factor * 0.3)

    # Gender equality: country-level
    gender_factor = (cp["gender"] - 5.5) / 4.5
    s["gender_equality"] = clamp(s["gender_equality"] + gender_factor * 2.0)

    # Age flexibility: better in more mature, inclusive markets
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_factor * 0.5 + fin_factor * 0.2)

    # Entrepreneurship: market dynamism + regulatory environment
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + fin_factor * 0.3 + reg_factor * 0.3)

    # International mobility: country openness
    intl_factor = (cp["intl"] - 6.0) / 4.0
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_factor * 1.5)

    # AI resistance: fintech-advanced countries see more automation
    s["ai_resistance"] = clamp(s["ai_resistance"] - fintech_factor * 0.3)

    # Learning cost and education req
    edu_factor = (cp["edu"] - 6.0) / 4.0
    s["learning_cost"] = clamp(s["learning_cost"] + edu_factor * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_factor * 0.3)

    # License barrier: stricter in more regulated financial environments
    s["license_barrier"] = clamp(s["license_barrier"] + bank_reg_factor * 0.5 + reg_factor * 0.3)

    # Cycle sensitivity: slightly higher in volatile economies
    stab_adj = -(bank_reg_factor * 0.3)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] + stab_adj)

    # Side job compatibility: remote culture + market openness
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_factor * 0.3)

    # Industry monopoly: higher in less competitive markets
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - fin_factor * 0.3)

    # Skill versatility: slightly better in mature financial ecosystems
    s["skill_versatility"] = clamp(s["skill_versatility"] + fin_factor * 0.3)

    # Career switch: easier in dynamic, larger markets
    s["career_switch"] = clamp(s["career_switch"] + fin_factor * 0.5)

    # Reputation variance: higher in emerging markets
    rep_adj = -0.3 if cp["fin_center"] >= 7.5 else (0.3 if cp["fin_center"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # --- Mid-category-specific adjustments ---

    # Securities/Investment: stock market size matters heavily
    if mid_cat == "securities_investment":
        stock_factor = (cp["stock_mkt"] - 6.0) / 4.0
        s["value_added"] = clamp(s["value_added"] + stock_factor * 1.0)
        s["market_size"] = clamp(s["market_size"] + stock_factor * 1.5)
        s["supply_demand"] = clamp(s["supply_demand"] + stock_factor * 0.5)
        s["opportunity"] = clamp(s["opportunity"] + stock_factor * 0.5)

    # Insurance: insurance market size drives opportunity
    if mid_cat == "insurance":
        ins_factor = (cp["ins_market"] - 6.0) / 4.0
        s["market_size"] = clamp(s["market_size"] + ins_factor * 1.5)
        s["supply_demand"] = clamp(s["supply_demand"] + ins_factor * 0.5)
        s["value_added"] = clamp(s["value_added"] + ins_factor * 0.5)

    # Real estate: real estate market matters
    if mid_cat == "real_estate":
        re_factor = (cp["re_market"] - 6.0) / 4.0
        s["market_size"] = clamp(s["market_size"] + re_factor * 1.5)
        s["value_added"] = clamp(s["value_added"] + re_factor * 0.5)
        s["opportunity"] = clamp(s["opportunity"] + re_factor * 0.5)
        s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] + re_factor * 0.5)

    # Islamic finance: relevance varies enormously by country
    if mid_cat == "islamic_finance":
        islamic_factor = (cp["islamic"] - 3.0) / 7.0  # 0-10 scale, baseline at 3
        s["market_size"] = clamp(s["market_size"] + islamic_factor * 3.0)
        s["supply_demand"] = clamp(s["supply_demand"] + islamic_factor * 2.0)
        s["value_added"] = clamp(s["value_added"] + islamic_factor * 1.5)
        s["opportunity"] = clamp(s["opportunity"] + islamic_factor * 2.0)
        s["social_status"] = clamp(s["social_status"] + islamic_factor * 1.0)

    # Consulting: consulting industry maturity
    if mid_cat == "consulting":
        consult_factor = (cp["consult"] - 6.0) / 4.0
        s["market_size"] = clamp(s["market_size"] + consult_factor * 1.5)
        s["value_added"] = clamp(s["value_added"] + consult_factor * 0.5)
        s["supply_demand"] = clamp(s["supply_demand"] + consult_factor * 0.5)

    # Crypto/DeFi: fintech maturity + regulatory environment
    if mid_cat == "crypto_defi":
        crypto_adj = fintech_factor * 0.5 - reg_factor * 0.3  # more fintech = more crypto; more reg = mixed
        s["market_size"] = clamp(s["market_size"] + crypto_adj * 1.5)
        s["supply_demand"] = clamp(s["supply_demand"] + crypto_adj * 0.5)
        s["opportunity"] = clamp(s["opportunity"] + fintech_factor * 0.5)

    return s


def get_trends(base_scores, country_profile):
    """Get trend values adjusted for country."""
    cp = country_profile
    t_long = base_scores["trend_long"]
    t_short = base_scores["trend_short"]

    # Strong fintech countries boost short-term finance trends
    if cp["fintech"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["fintech"] < 4.0:
        t_short = max(-5, t_short - 1)

    # Financial center rank sustains long-term trends
    if cp["fin_center"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["fin_center"] < 4.0:
        t_long = max(-5, t_long - 1)

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

    if scores["remote_friendly"] >= 8.5:
        highlights_zh.append("远程友好度高")
        highlights_en.append("highly remote-friendly")

    if scores["overtime"] <= 3.5:
        highlights_zh.append("加班文化严重")
        highlights_en.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5:
        highlights_zh.append("工作时间规律")
        highlights_en.append("regular working hours")

    if scores["stability"] >= 8.0:
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

    if scores["burnout"] <= 3.0:
        highlights_zh.append("职业倦怠风险高")
        highlights_en.append("high burnout risk")

    if scores["fulfillment"] >= 8.5:
        highlights_zh.append("职业成就感高")
        highlights_en.append("high career fulfillment")

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
    random.seed(42)

    weights = load_weights()
    output_path = PROJECT_ROOT / "data" / "csv" / "finance_business.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

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
            noise_seed = hash(f"FIN-{occ['id']}-{iso}") % 10000
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

            row_id = f"FIN-{occ['id']}-{iso}-general"

            row = {
                "id": row_id,
                "major_category": "金融与商业",
                "major_code": "FIN",
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
            row["data_source"] = "AI综合评估 + O*NET/ILO/BIS锚点校准"

            rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows to {output_path}")
    print(f"Occupations: {len(OCCUPATIONS)}")
    print(f"Countries: {len(COUNTRIES)}")


if __name__ == "__main__":
    main()
