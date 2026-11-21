"""读取审稿采样记录，列出本轮首次待提醒的问题。"""

import argparse
import re
from pathlib import Path

from format_table import split_row


DEFAULT_RECORD = Path(__file__).resolve().parents[1] / "review-samples.md"
ISSUE_COLUMNS = ["问题编号", "可复现的问题", "适用条件", "当前轮次", "提醒状态", "最近清零日期及原因"]
SAMPLE_COLUMNS = ["完成日期", "任务标识", "问题编号", "轮次", "结果（命中／未命中）", "稿件位置及现象"]


def table_rows(markdown, title, columns):
    rows = []
    section = ""
    for number, line in enumerate(markdown.splitlines(), 1):
        line = line.strip()
        if line.startswith("## "):
            section = line[3:]
        elif section == title and line.startswith("|"):
            cells = split_row(line, number)
            if len(cells) != len(columns):
                raise ValueError(f"第 {number} 行应有 {len(columns)} 列")
            rows.append(cells)
    if len(rows) < 2 or rows[0] != columns or not all(re.fullmatch(r":?-+:?", c) for c in rows[1]):
        raise ValueError(f"请核对「{title}」表头和分隔行")
    return rows[2:]


def round_number(value):
    if not value.isdecimal() or int(value) < 1:
        raise ValueError(f"轮次应为正整数，当前为 {value!r}")
    return int(value)


def pending_reminders(markdown):
    issues = {}
    for issue_id, name, _, current_round, status, _ in table_rows(markdown, "问题清单", ISSUE_COLUMNS):
        if not issue_id or issue_id in issues or status not in {"观察中", "已提醒"}:
            raise ValueError(f"请核对问题编号 {issue_id!r}、重复登记和提醒状态")
        issues[issue_id] = (name, round_number(current_round), status)

    seen = set()
    outcomes = {issue_id: [] for issue_id in issues}
    for _, task, issue_id, sample_round, result, _ in table_rows(markdown, "任务样本", SAMPLE_COLUMNS):
        if issue_id not in issues or not task or result not in {"命中", "未命中"}:
            raise ValueError(f"请核对样本的问题编号、任务和结果：{issue_id!r} / {task!r} / {result!r}")
        key = (issue_id, task)
        if key in seen:
            raise ValueError(f"{issue_id} 的任务 {task!r} 重复，请合并为一行")
        seen.add(key)
        current_round = issues[issue_id][1]
        number = round_number(sample_round)
        if number > current_round:
            raise ValueError(f"{issue_id} 的样本轮次 {number} 超过当前轮次 {current_round}")
        if number == current_round:
            outcomes[issue_id].append(result == "命中")

    for issue_id, (name, current_round, status) in issues.items():
        if status == "已提醒":
            continue
        samples = outcomes[issue_id]
        hits = sum(samples)
        recent = samples[-5:]
        reasons = []
        if hits >= 3:
            reasons.append(f"累计 {hits} 次命中")
        if len(recent) == 5 and sum(recent) >= 2:
            reasons.append(f"最近 5 个样本命中 {sum(recent)} 次")
        if reasons:
            yield f"{issue_id} {name}（第 {current_round} 轮）：{'，'.join(reasons)}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", nargs="?", type=Path, default=DEFAULT_RECORD, help="采样文件路径")
    args = parser.parse_args()
    try:
        reminders = list(pending_reminders(args.record.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    print("\n".join(reminders) if reminders else "无待提醒问题。")


if __name__ == "__main__":
    main()
