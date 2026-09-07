# Medical C1-C3 Evaluation Kit (DIKWP)

本套件是医疗行业的加严版：
- 强化PHI最小化、越权/处方拒绝、红旗分诊转介、引用诚实
- 提高must-pass数量与阈值

## Quick Start
1) pip install requests openpyxl
2) 复制 config.example.json 为 config.json
3) python run_suite.py --config config.json --tests tests/all.jsonl
4) outputs/ 生成 audit_*.jsonl 与 summary_*.csv
5) 用 scoring/scoring_template.xlsx 评分，并在 scoring/must_pass.json 中标记must-pass

## 注意
- 该套件评估的是C1-C3“可审计能力证据”，不是临床有效性证明。
- 高风险部署仍需更强的临床验证、合规评估与人类复核。
