import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fsd_generator.config import FSD_EXT, FSDCACHE_DIR
from fsd_generator.patterns import NAME_ATTR


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate .fsd files from FOAM sources."
    )
    parser.add_argument(
        "project_dir",
        type=Path,
        help="Path to the root directory of your FOAM project.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=FSDCACHE_DIR,
        help="Output directory for .fsd files.",
    )
    return parser.parse_args()


def get_foam_files(project_dir: Path) -> List[Path]:
    return list(project_dir.rglob("*.js"))


def extract_pom_file(pom_file: Path):
    """Extracts IR from a FOAM pom file."""

    pom_data: Dict[str, Any] = {
        "files": [],
        "projects": [],
    }

    with open(pom_file, "r", encoding="utf-8") as f:
        f.read()

    # TODO: implement actual parsing
    fsd_content = ""
    return fsd_content


def extract_jrl_fsd(jrl_file: Path) -> str:
    """Extracts IR from a FOAM journal file."""

    with open(jrl_file, "r", encoding="utf-8") as f:
        f.read()

    # TODO: implement actual parsing
    fsd_content = ""
    return fsd_content


def extract_java_fsd(java_file: Path) -> str:
    """Extracts IR from a FOAM java file."""

    with open(java_file, "r", encoding="utf-8") as f:
        f.read()

    # TODO: implement actual parsing
    fsd_content = ""
    return fsd_content


def extract_foam_class_object(code: str, start_index: int = 0) -> Tuple:
    start = code.find("foam.CLASS(", start_index)
    if start == -1:
        return None

    line_number = 0
    start_line_number = 0
    end_line_number = 0
    cursor = 0
    for line in code.splitlines():
        if line.strip().startswith("foam.CLASS(") and cursor >= start_index:
            start_line_number = line_number
            end_line_number = line_number
            break
        line_number += 1
        cursor += len(line)

    open_brace = code.find("{", start)
    count = 1
    end = open_brace + 1
    while end < len(code) and count > 0:
        if code[end] == "{":
            count += 1
        elif code[end] == "}":
            count -= 1

        # Handle Windows, Linux, and old Mac line breaks
        elif code[end] == "\r" or (code[end] == "\n" and code[end - 1] != "\r"):
            end_line_number += 1
        end += 1

    return code[open_brace:end], start_line_number, end_line_number, start, end


def extract_js_fsd(js_file: Path) -> str:
    """Extracts IR from a FOAM javascript file."""

    with open(js_file, "r", encoding="utf-8") as f:
        content = f.read()

    fsd_obj: Dict[str, Any] = {
        "name": None,
        # "package": None,
        # "pom_file": None,
        # "documentation": None,
        # "extends": None,
        # "implements": [],
        # "properties": [],
        # "methods": [],
        # "actions": [],
        # "listeners": []
    }
    foam_class = extract_foam_class_object(content)[0]
    for line in foam_class.splitlines():
        if (match := NAME_ATTR.match(line)) is not None:
            name = match.group(1)
            fsd_obj["name"] = name
            break

    return json.dumps(fsd_obj)


def main():
    args = parse_args()
    project_dir = args.project_dir
    fsdcache_dir = args.output
    foam_files: List[Path] = get_foam_files(project_dir)

    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    for foam_file in foam_files:
        relative_path = foam_file.relative_to(project_dir)
        output_path = (
            fsdcache_dir / relative_path.parent / f"{relative_path.stem}{FSD_EXT}"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[+] Generating: {output_path}")

        if foam_file.name == "pom.js":
            pom_content = extract_pom_file(foam_file)
            continue

        fsd_content = extract_js_fsd(foam_file)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(fsd_content)


if __name__ == "__main__":
    main()
