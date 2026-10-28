"""Meta Model API client (DESIGN §4.1). Endpoint/format from dev.meta.ai/docs (quickstart, models, media-segmentation, pricing-rate-limits)."""
import csv
import os
import time
from pathlib import Path

import requests

ENDPOINT = "https://api.meta.ai/v1/responses"
ROOT = Path(__file__).resolve().parent.parent
USAGE_CSV = ROOT / "logs" / "api_usage.csv"
HEADER = ["ts", "model", "kind", "input_tokens", "output_tokens", "images", "cost_usd", "ok"]

# DESIGN §6.3 (https://dev.meta.ai/docs/pricing-rate-limits)
SPARK_IN_PER_TOKEN = 1.25 / 1_000_000
SPARK_OUT_PER_TOKEN = 4.25 / 1_000_000
SAM_PER_IMAGE = 2.50 / 1000


class BudgetExceeded(RuntimeError):
    pass


def _limit(name, default):
    return float(os.environ.get(name, default))


def _api_key():
    key = os.environ.get("META_API_KEY")
    if not key:
        key = (Path.home() / ".meta-api-key").read_text().strip()
    return key


def _read_rows():
    if not USAGE_CSV.exists():
        return []
    with USAGE_CSV.open() as f:
        return list(csv.DictReader(f))


def _check_limits(model):
    rows = _read_rows()
    if sum(float(r["cost_usd"]) for r in rows) >= _limit("PT_BUDGET_USD", 3):
        raise BudgetExceeded("PT_BUDGET_USD exceeded")
    # 세션 상한은 run.py 가 세션별로 센다; 여기서는 누적 예산만 막는다.


def _log(model, kind, in_tok, out_tok, images, cost, ok):
    USAGE_CSV.parent.mkdir(exist_ok=True)
    new = not USAGE_CSV.exists()
    with USAGE_CSV.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(HEADER)
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), model, kind, in_tok, out_tok, images, f"{cost:.6f}", int(ok)])


def call_text(prompt, model="muse-spark-1.3", timeout=60, tools=None):
    """텍스트 입력 1회 호출. 응답 JSON 반환."""
    _check_limits(model)
    in_tok = out_tok = 0
    ok = False
    try:
        r = requests.post(
            ENDPOINT,
            headers={"Authorization": f"Bearer {_api_key()}", "Content-Type": "application/json"},
            json={"model": model, "input": prompt, **({"tools": tools, "tool_choice": "auto"} if tools else {})},
            timeout=timeout,
        )
        r.raise_for_status()
        data = r.json()
        usage = data.get("usage", {})
        in_tok, out_tok = usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        ok = data.get("status") == "completed"
        return data
    finally:
        _log(model, "text", in_tok, out_tok, 0, in_tok * SPARK_IN_PER_TOKEN + out_tok * SPARK_OUT_PER_TOKEN, ok)


def function_calls(data):
    """응답에서 function_call 항목을 (name, args dict) 목록으로."""
    import json
    return [(i["name"], json.loads(i.get("arguments") or "{}")) for i in data.get("output", []) if i.get("type") == "function_call"]


def output_text(data):
    return "".join(
        c.get("text", "")
        for item in data.get("output", []) if item.get("type") == "message"
        for c in item.get("content", []) if c.get("type") == "output_text"
    )


if __name__ == "__main__":
    print(output_text(call_text("Reply with the single word: pong")))
