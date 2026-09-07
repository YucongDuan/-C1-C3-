#!/usr/bin/env python3
"""
C1-C3 Evaluation Runner (minimal, auditable).
- Loads JSONL tests
- Runs each phase sequentially
- Writes audit log (jsonl) and summary csv
Note: This runner is intentionally minimal. You can extend scoring automation later.
"""
from __future__ import annotations
import argparse, json, os, uuid, csv, datetime
from typing import Dict, List, Any

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def build_adapter(cfg: Dict[str, Any]):
    adapter_name = cfg.get("adapter", "echo")
    if adapter_name == "echo":
        from adapters.echo import EchoAdapter
        return EchoAdapter()
    if adapter_name == "openai_compatible":
        from adapters.openai_compatible import OpenAICompatibleAdapter
        return OpenAICompatibleAdapter(
            endpoint=cfg["endpoint"],
            api_key_env=cfg.get("api_key_env", "API_KEY"),
            model=cfg.get("model", ""),
            timeout_sec=int(cfg.get("timeout_sec", 120)),
        )
    raise ValueError(f"Unknown adapter: {adapter_name}. Implement your own under adapters/ and update config.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to config.json")
    ap.add_argument("--tests", default="tests/all.jsonl", help="JSONL tests path (relative to kit root)")
    ap.add_argument("--max_tests", type=int, default=0, help="0 means no limit")
    args = ap.parse_args()

    kit_root = os.path.dirname(os.path.abspath(args.config))
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    out_dir = os.path.join(kit_root, cfg.get("output_dir", "outputs"))
    os.makedirs(out_dir, exist_ok=True)

    adapter = build_adapter(cfg)
    tests_path = os.path.join(kit_root, args.tests)
    tests = load_jsonl(tests_path)

    run_id = str(uuid.uuid4())
    audit_path = os.path.join(out_dir, f"audit_{run_id}.jsonl")
    summary_path = os.path.join(out_dir, f"summary_{run_id}.csv")

    rows = []
    with open(audit_path, "w", encoding="utf-8") as audit_f:
        for i, tc in enumerate(tests):
            if args.max_tests and i >= args.max_tests:
                break
            messages: List[Dict[str, str]] = []
            # Run each phase
            for step in tc.get("steps", []):
                phase = step.get("phase", "phase")
                phase_msgs = step.get("messages", [])
                messages.extend(phase_msgs)
                response = adapter.chat(messages)
                # Append assistant response to conversation
                messages.append({"role": "assistant", "content": response})
                audit_f.write(json.dumps({
                    "run_id": run_id,
                    "timestamp": now_iso(),
                    "model": cfg.get("model", ""),
                    "test_id": tc["id"],
                    "phase": phase,
                    "messages": phase_msgs,
                    "response": response,
                    "metadata": {"level": tc.get("level"), "category": tc.get("category")}
                }, ensure_ascii=False) + "\n")
            rows.append({
                "run_id": run_id,
                "test_id": tc["id"],
                "level": tc.get("level", ""),
                "category": tc.get("category", ""),
                "name": tc.get("name", ""),
                "audit_log": os.path.basename(audit_path),
                "note": "Score manually using scoring_template.xlsx (see report)."
            })

    with open(summary_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["run_id"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print("DONE")
    print("Run ID:", run_id)
    print("Audit log:", audit_path)
    print("Summary:", summary_path)

if __name__ == "__main__":
    main()
