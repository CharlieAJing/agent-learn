"""格式化一张 Obsidian Markdown 表格并输出到标准输出。

第一行是表头，每行首尾带 |。分隔行可省略。输入有误时，根据错误提示修正后重试。

从项目根目录运行，任选一种输入方式：
  python3 skills/scripts/format_table.py "$table"
  python3 skills/scripts/format_table.py < table.md
"""

import argparse
import re
import sys


def split_row(line, number):
    if not (line.startswith("|") and line.endswith("|") and len(line) >= 2):
        raise ValueError(f"第 {number} 行需要用 | 标出首尾，每格内容写在同一行")

    cells = []
    cell = []
    # Escapes, wikilinks and inline code can contain literal table delimiters.
    tokens = re.findall(r"\\.|\[\[|\]\]|`+|.", line[1:-1])
    in_link = False
    code_fence = ""
    for token in tokens:
        if token.startswith("`"):
            if token == code_fence:
                code_fence = ""
            elif not code_fence and not in_link:
                code_fence = token
        elif token == "[[" and not code_fence:
            in_link = True
        elif token == "]]" and not code_fence:
            in_link = False
        elif token == "|":
            if in_link or code_fence:
                token = r"\|"
            else:
                cells.append("".join(cell).strip())
                cell = []
                continue
        cell.append(token)
    if in_link or code_fence:
        raise ValueError(f"第 {number} 行的双链或行内代码未闭合")
    cells.append("".join(cell).strip())
    return cells


def format_table(markdown):
    rows = []
    for number, line in enumerate(markdown.splitlines(), 1):
        if not line.strip():
            continue
        cells = split_row(line.strip(), number)
        if not rows and not all(cells):
            raise ValueError(f"第 {number} 行有空表头")
        if rows and len(cells) != len(rows[0]):
            raise ValueError(f"第 {number} 行有 {len(cells)} 列，表头有 {len(rows[0])} 列")
        rows.append(cells)
    if not rows:
        raise ValueError("请输入一张表格")

    if len(rows) > 1 and all(re.fullmatch(r":?-+:?", c) for c in rows[1]):
        rows[1] = [re.sub("-+", "---", c) for c in rows[1]]
    else:
        rows.insert(1, ["---"] * len(rows[0]))
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("markdown", nargs="?", help="单张表格文本，省略时从标准输入读取")
    args = parser.parse_args()
    try:
        result = format_table(args.markdown if args.markdown is not None else sys.stdin.read())
    except ValueError as error:
        parser.exit(2, f"{error}\n")
    print(result)


if __name__ == "__main__":
    main()
