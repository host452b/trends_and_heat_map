# 数据维护流程 (Flow)

## 扩展数据
1. 新职业 → 先更新 schema/categories.yaml
2. 每条记录必须包含 58 列完整数据
3. 评分 0-10 统一制，综合加权按 weights.yaml 计算
4. 用 tools/validate_data.py 验证后再提交

## 校准数据
1. O*NET → 校准美国职业评分
2. ILO ILOSTAT → 校准全球就业/安全/工时
3. OECD → 校准发达国家数据
4. Glassdoor/LinkedIn → 校准口碑和供需
5. 实际薪资数据 → 校准附加值

## 生成产出
1. 每个 CSV 对应一个 .ipynb (红绿色阶完整数据)
2. JSON 镜像: `from tools.csv_to_json import convert_csv_to_json`
3. Notebook: `from tools.generate_notebook import create_data_notebook`
4. README 含完整权重表和列说明

## 58 列统一结构
id/大类/代码/中类/细类/英文/ISCO/O*NET/区域/国家/ISO/类型/雇主/学历/年龄/地区性
34 个评分维度
趋势(2)/需求方向/AI时间线/综合指数/摘要中/摘要英/来源
