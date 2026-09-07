# C1-C3 Evaluation Kit (DIKWP-based)

本套件用于评估“意识相关能力声明”的可审计证据（C1-C3），不是意识本体证明。
你将得到：
- tests/*.jsonl：题库（可直接跑）
- run_suite.py：最小评测执行器（可换适配器）
- scoring/scoring_template.xlsx：打分表（人工评分为主）
- schemas/*.json：测试用例与审计日志的JSON Schema

## 快速开始（最小运行）
1) 安装Python依赖（若使用openai_compatible适配器需requests）：
   - pip install requests openpyxl
2) 复制 config.example.json 为 config.json，并填写：model、adapter、endpoint、api_key_env
3) 运行：
   - python run_suite.py --config config.json --tests tests/all.jsonl
4) 在 outputs/ 下生成 audit_*.jsonl 与 summary_*.csv
5) 用 scoring/scoring_template.xlsx 进行人工打分，并把证据路径填入表格。

## 适配器
- adapters/echo.py：离线干跑（不联网）
- adapters/openai_compatible.py：OpenAI风格ChatCompletions接口
你也可以新增 adapters/custom.py 并在config里写 adapter=custom。

## 审计与合规建议
- 高风险场景请启用“回放审计”：保留请求/响应、版本、引用与工具调用日志。
- 不要使用“AI检测器”作为主要证据；优先用口试/复现/过程证据与本套件的对抗测试。
