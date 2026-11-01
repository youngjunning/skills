#!/usr/bin/env python3
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    required = [
        SKILL,
        ROOT / "agents" / "openai.yaml",
        ROOT / "scripts" / "windows-ui.ps1",
        ROOT / "references" / "windows-uia.md",
        ROOT / "references" / "remote-sessions.md",
        ROOT / "references" / "playbooks.md",
        ROOT / "references" / "powershell-execution.md",
        ROOT / "references" / "verification-and-recovery.md",
        ROOT / "README.md",
        ROOT / "LICENSE",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    text = SKILL.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        fail("SKILL.md has no YAML frontmatter")
    metadata = frontmatter.group(1)
    if "name: windows-app-automation" not in metadata:
        fail("SKILL.md has the wrong skill name")
    if not re.search(r"^description:\s*\S", metadata, re.MULTILINE):
        fail("SKILL.md has no description")

    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    scaffold_marker = "[" + "TODO"
    if scaffold_marker in all_text:
        fail("unfinished scaffold placeholder found")

    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    local_links = [link for link in links if "://" not in link and not link.startswith("#")]
    broken = [link for link in local_links if not (ROOT / link).is_file()]
    if broken:
        fail(f"broken SKILL.md links: {', '.join(broken)}")

    print("Structure validation passed.")


if __name__ == "__main__":
    main()
