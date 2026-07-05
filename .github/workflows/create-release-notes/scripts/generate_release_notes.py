#!/usr/bin/env python3
"""
数据驱动的 Release Notes 生成器。
配置加载顺序：
1. 调用者仓库的 .github/release-notes-config.yml
2. --default-config 指定的公共默认配置
3. 若两者都不可用，直接报错退出
"""
import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
import yaml


def load_config(default_config_path):
    """加载配置，失败时直接退出"""
    # 1) 调用者仓库的覆盖配置
    caller_config = ".github/release-notes-config.yml"
    if os.path.exists(caller_config):
        print(f"::notice::Using caller config: {caller_config}")
        with open(caller_config) as f:
            return yaml.safe_load(f)

    # 2) 公共默认配置
    if default_config_path and os.path.exists(default_config_path):
        print(f"::notice::Using shared default config: {default_config_path}")
        with open(default_config_path) as f:
            return yaml.safe_load(f)

    # 3) 都没有 → 终止
    sys.exit(
        "::error::No release config found. "
        "Provide either .github/release-notes-config.yml in the caller repo "
        "or a valid --default-config path."
    )


def get_tag_message(tag):
    """返回 annotated tag 的完整消息，轻量标签返回空"""
    try:
        # 先检查标签类型：commit 表示轻量标签，tag 表示 annotated
        object_type = subprocess.check_output(
            ["git", "tag", "-l", "--format=%(objecttype)", tag],
            text=True
        ).strip()
        if object_type == "commit":
            return ""   # 轻量标签直接视为无消息
        elif object_type == "tag":
            # annotated 标签，返回完整内容
            return subprocess.check_output(
                ["git", "tag", "-l", "--format=%(contents)", tag],
                text=True
            ).strip()
        return ""
    except subprocess.CalledProcessError:
        return ""


def get_previous_tag(current_tag):
    """获取按版本排序的前一个 tag"""
    try:
        all_tags = subprocess.check_output(
            ["git", "tag", "--sort=-v:refname"], text=True
        ).strip().split("\n")
        for t in all_tags:
            if t and t != current_tag:
                return t
    except subprocess.CalledProcessError:
        pass
    return ""


def get_commits(prev_tag):
    """获取自 prev_tag 以来的所有提交 (short_hash, full_hash, title)"""
    if prev_tag:
        cmd = ["git", "log", "--pretty=format:%h %H %s", f"{prev_tag}..HEAD"]
    else:
        cmd = ["git", "log", "--pretty=format:%h %H %s"]
    output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    commits = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 2)
        if len(parts) == 3:
            short_hash, full_hash, title = parts
            commits.append((short_hash, full_hash, title))
    return commits


def generate_notes(commits, categories, default_cat, order, repo):
    """根据提交和分类映射生成带哈希链接的 markdown 分组文本"""
    type_map = {k.lower(): v for k, v in categories.items()}
    groups = defaultdict(list)

    for short_hash, full_hash, msg in commits:
        match = re.match(r"^(\w+):\s*(.*)", msg)
        if match:
            prefix = match.group(1).lower()
            desc = match.group(2)
            cat = type_map.get(prefix, default_cat)
        else:
            desc = msg
            cat = default_cat

        commit_link = f"https://github.com/{repo}/commit/{full_hash}"
        item = f"- {desc} ([`{short_hash}`]({commit_link}))"
        groups[cat].append(item)

    lines = []
    # 按 order 指定顺序输出
    for cat in order:
        if cat in groups:
            lines.append(f"## {cat}")
            lines.extend(groups[cat])
            lines.append("")
    # 输出 order 中没有的分类（防御）
    for cat, descs in groups.items():
        if cat not in order:
            lines.append(f"## {cat}")
            lines.extend(descs)
            lines.append("")
    return "\n".join(lines).strip()


def build_changelog_link(current_tag, prev_tag, repo):
    """构造 Full Changelog 或 Commit 链接"""
    commit_sha = subprocess.check_output(
        ["git", "rev-list", "-n", "1", current_tag], text=True
    ).strip()
    if prev_tag:
        return (
            f"**Full Changelog**: "
            f"https://github.com/{repo}/compare/{prev_tag}...{current_tag}"
        )
    return (
        f"**Commit**: "
        f"https://github.com/{repo}/commit/{commit_sha}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--default-config",
        required=True,
        help="Path to shared default release-notes-config.yml"
    )
    args = parser.parse_args()

    tag = os.environ["TAG"]
    repo = os.environ["GITHUB_REPOSITORY"]

    # 1. 手动编写的 tag 消息优先（轻量标签会返回空，走自动生成）
    tag_msg = get_tag_message(tag)

    config = load_config(args.default_config)
    title_template = config.get("title", "{version}")

    # 2. 前一个 tag（手动、自动都要用）
    prev_tag = get_previous_tag(tag)

    # 3. 生成正文
    if tag_msg:
        notes = tag_msg
    else:
        categories = config.get("categories")
        default_cat = config.get("default_category")
        order = config.get("order")

        if not categories:
            sys.exit("::error::Config must contain 'categories' mapping.")
        if not default_cat:
            sys.exit("::error::Config must contain 'default_category'.")

        # 如果没有提供 order，自动生成：所有分类值 + 默认分类
        if not order:
            order = list(categories.values()) + [default_cat]

        commits = get_commits(prev_tag)
        if not commits:
            notes = ""
        else:
            notes = generate_notes(commits, categories, default_cat, order, repo)

    # 4. 尾部链接
    link = build_changelog_link(tag, prev_tag, repo)

    # 5. 完整说明
    full_notes = f"{notes}\n\n{link}" if notes else link

    # 6. 创建 Release
    version = tag.lstrip("v")
    release_title = title_template.format(version=version)
    subprocess.run([
        "gh", "release", "create", tag,
        "--title", release_title,
        "--notes", full_notes
    ], check=True)


if __name__ == "__main__":
    main()
