#!/usr/bin/env python3
"""
Council Genius V10 — Fidelity Protocol Layer 1 (Burwood Council)
Canonical test-suite runner.

Usage:
    # Against a live /chat endpoint (post-Phase-9 deploy):
    python3 run_tests.py --endpoint https://<burwood-deploy>/chat \
                         --health   https://<burwood-deploy>/health

    # Local dry-run against knowledge.txt (no endpoint required):
    python3 run_tests.py --local

    # Filter to a few tests, write a markdown report:
    python3 run_tests.py --local --only T-004,T-025 --out report_local.md

Modes:
  (default) Fires each query at the live /chat endpoint and checks
            must_include / must_include_any_of / should_include /
            must_not_include patterns against the JSON `reply` field.

  --local   No endpoint required. Scans the council's knowledge.txt
            (relative path in meta.knowledge_base) for each required
            pattern. Useful for validating the knowledge base itself
            before Phase 9 deploy.

Exit code:
    0 = all tests passed
    1 = at least one test failed
    2 = endpoint / knowledge base unreachable or misconfigured

No dependencies beyond the Python standard library.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def http_post_json(url: str, payload: dict, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get_json(url: str, timeout: int = 15) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_test(test: dict, reply: str) -> tuple:
    """Return (passed, reasons_for_failure)."""
    low = reply.lower()
    failures = []

    must_include = test.get("must_include", [])
    match_any = test.get("match_any", False)

    if must_include:
        if match_any:
            if not any(tok.lower() in low for tok in must_include):
                failures.append(
                    "match_any must_include: none of "
                    f"{must_include} found"
                )
        else:
            missing = [t for t in must_include if t.lower() not in low]
            if missing:
                failures.append(f"must_include missing: {missing}")

    must_include_any_of = test.get("must_include_any_of", [])
    if must_include_any_of:
        if not any(tok.lower() in low for tok in must_include_any_of):
            failures.append(
                "must_include_any_of: none of "
                f"{must_include_any_of} found"
            )

    must_not_include = test.get("must_not_include", [])
    present_forbidden = [t for t in must_not_include if t.lower() in low]
    if present_forbidden:
        failures.append(f"must_not_include found: {present_forbidden}")

    return (len(failures) == 0, failures)


def score_should(test: dict, reply: str) -> tuple:
    """Return (hits, total) for soft 'should_include' patterns."""
    should = test.get("should_include", [])
    if not should:
        return (0, 0)
    low = reply.lower()
    hits = sum(1 for tok in should if tok.lower() in low)
    return (hits, len(should))


def run_live(tests, endpoint, health, throttle, stop_on_fail):
    """Run tests against the live /chat endpoint."""
    print(f"[health] {health}")
    try:
        h = http_get_json(health)
        print(
            f"[health] OK — council={h.get('council')!r} "
            f"knowledge_lines={h.get('knowledge_lines')} "
            f"knowledge_hash={h.get('knowledge_hash')} "
            f"uptime={h.get('uptime_seconds')}s"
        )
    except Exception as e:
        print(f"[health] FAILED: {e}", file=sys.stderr)
        return None, 2

    total = len(tests)
    passed = 0
    failed = 0
    results = []

    for idx, test in enumerate(tests, 1):
        tid = test.get("id", f"T-{idx:03d}")
        query = test["query"]
        print(f"\n[{idx}/{total}] {tid} ({test.get('category','-')}): {query!r}")

        try:
            response = http_post_json(
                endpoint,
                {"messages": [{"role": "user", "content": query}]},
                timeout=60,
            )
        except Exception as e:
            print(f"  ERROR: request failed: {e}")
            results.append({
                "id": tid,
                "query": query,
                "category": test.get("category", ""),
                "pass": False,
                "error": str(e),
                "reply": "",
                "must_fail_reasons": ["request failed"],
                "should_hits": 0,
                "should_total": 0,
            })
            failed += 1
            if stop_on_fail:
                break
            time.sleep(throttle)
            continue

        reply = response.get("reply", "") or ""
        ok, reasons = check_test(test, reply)
        should_hits, should_total = score_should(test, reply)

        summary = ("PASS" if ok else "FAIL") + f"  should={should_hits}/{should_total}"
        print(f"  {summary}")
        if reasons:
            for r in reasons:
                print(f"    - {r}")

        results.append({
            "id": tid,
            "query": query,
            "category": test.get("category", ""),
            "pass": ok,
            "reply": reply,
            "must_fail_reasons": reasons,
            "should_hits": should_hits,
            "should_total": should_total,
        })

        if ok:
            passed += 1
        else:
            failed += 1
            if stop_on_fail:
                break

        time.sleep(throttle)

    return (results, passed, failed, total), (0 if failed == 0 else 1)


def run_local(tests, knowledge_path, stop_on_fail):
    """Run tests against knowledge.txt directly (no endpoint)."""
    kpath = Path(knowledge_path)
    if not kpath.exists():
        print(f"ERROR: knowledge base not found: {kpath}", file=sys.stderr)
        return None, 2

    print(f"[local] knowledge base: {kpath} ({kpath.stat().st_size:,} bytes)")
    corpus = kpath.read_text(encoding="utf-8")
    print(f"[local] lines: {corpus.count(chr(10)):,}")

    total = len(tests)
    passed = 0
    failed = 0
    results = []

    for idx, test in enumerate(tests, 1):
        tid = test.get("id", f"T-{idx:03d}")
        query = test["query"]
        print(f"\n[{idx}/{total}] {tid} ({test.get('category','-')}): {query!r}")

        ok, reasons = check_test(test, corpus)
        should_hits, should_total = score_should(test, corpus)

        summary = ("PASS" if ok else "FAIL") + f"  should={should_hits}/{should_total}"
        print(f"  {summary}")
        if reasons:
            for r in reasons:
                print(f"    - {r}")

        results.append({
            "id": tid,
            "query": query,
            "category": test.get("category", ""),
            "pass": ok,
            "reply": "(local mode — matched against knowledge.txt)",
            "must_fail_reasons": reasons,
            "should_hits": should_hits,
            "should_total": should_total,
        })

        if ok:
            passed += 1
        else:
            failed += 1
            if stop_on_fail:
                break

    return (results, passed, failed, total), (0 if failed == 0 else 1)


def write_report(out_path, endpoint_or_mode, suite_path, meta, results, passed, failed, total):
    lines = [
        "# Council Genius V10 — Fidelity Protocol Layer 1 Report (Burwood Council)",
        "",
        f"- Mode/Endpoint: `{endpoint_or_mode}`",
        f"- Suite: `{suite_path.name}` ({meta.get('version', '?')})",
        f"- Council: {meta.get('council', '-')}",
        f"- Tests: {total}",
        f"- **Passed: {passed}**",
        f"- **Failed: {failed}**",
        "",
        "## Results",
        "",
        "| ID | Category | Pass | Should (soft) | Failure reasons |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        reason_str = "; ".join(r["must_fail_reasons"]) if r["must_fail_reasons"] else "-"
        lines.append(
            f"| {r['id']} | {r.get('category', '-')} | "
            f"{'PASS' if r['pass'] else 'FAIL'} | "
            f"{r['should_hits']}/{r['should_total']} | {reason_str} |"
        )
    lines.append("")
    lines.append("## Failing tests (detail)")
    lines.append("")
    any_fail = False
    for r in results:
        if r["pass"]:
            continue
        any_fail = True
        lines.append(f"### {r['id']} — {r['query']}")
        lines.append("")
        lines.append("Failure reasons:")
        for fr in r["must_fail_reasons"]:
            lines.append(f"- {fr}")
        lines.append("")
        lines.append("```")
        lines.append((r["reply"] or "<no reply>")[:1500])
        lines.append("```")
        lines.append("")
    if not any_fail:
        lines.append("_All tests passed._")
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"Report written to {out_path}")


def main() -> int:
    p = argparse.ArgumentParser(description="Fidelity Protocol Layer 1 runner — Burwood Council")
    p.add_argument("--suite", default=str(Path(__file__).parent / "test_suite.json"))
    p.add_argument("--endpoint", default=None)
    p.add_argument("--health", default=None)
    p.add_argument("--local", action="store_true")
    p.add_argument("--knowledge", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--stop-on-fail", action="store_true")
    p.add_argument("--only", default=None)
    p.add_argument("--throttle", type=float, default=1.0)
    args = p.parse_args()

    suite_path = Path(args.suite)
    if not suite_path.exists():
        print(f"ERROR: test suite not found: {suite_path}", file=sys.stderr)
        return 2

    suite = json.loads(suite_path.read_text())
    meta = suite.get("meta", {})

    tests = suite.get("tests", [])
    if args.only:
        only = set(x.strip() for x in args.only.split(","))
        tests = [t for t in tests if t.get("id") in only]

    if args.local:
        kb = args.knowledge or meta.get("knowledge_base")
        if not kb:
            print("ERROR: --local given but no --knowledge or meta.knowledge_base", file=sys.stderr)
            return 2
        kpath = Path(kb)
        if not kpath.is_absolute():
            kpath = (suite_path.parent / kb).resolve()
        bundle, rc = run_local(tests, kpath, args.stop_on_fail)
        if bundle is None:
            return rc
        results, passed, failed, total = bundle
        mode_label = f"local:{kpath}"
    else:
        endpoint = args.endpoint or meta.get("endpoint")
        health = args.health or meta.get("health_endpoint")
        if not endpoint or endpoint.startswith("TBC"):
            print(
                "ERROR: no live /chat endpoint configured. "
                "Use --endpoint <URL> or run with --local for a KB dry-run.",
                file=sys.stderr,
            )
            return 2
        bundle, rc = run_live(tests, endpoint, health, args.throttle, args.stop_on_fail)
        if bundle is None:
            return rc
        results, passed, failed, total = bundle
        mode_label = endpoint

    print(f"\n=== SUMMARY: {passed} passed / {failed} failed / {total} total ===")

    if args.out:
        write_report(Path(args.out), mode_label, suite_path, meta, results, passed, failed, total)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
