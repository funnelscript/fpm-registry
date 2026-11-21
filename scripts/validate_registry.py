"""Validates that all packages in the registry have valid tarballs and matching SHA-256 integrity."""

import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    registry_root = Path(__file__).parent.parent
    index_dir = registry_root / "index"
    if not index_dir.exists():
        print(f"Error: index directory not found at {index_dir}")
        return 1

    errors = 0
    package_count = 0
    version_count = 0

    for json_file in sorted(index_dir.rglob("*.json")):
        package_count += 1
        data = json.loads(json_file.read_text(encoding="utf-8"))
        pkg_name = data.get("name")
        versions = data.get("versions", {})

        for ver_str, ver_info in sorted(versions.items()):
            version_count += 1
            tarball_rel = ver_info.get("tarball_url")
            expected_integrity = ver_info.get("integrity")

            tarball_path = registry_root / tarball_rel
            if not tarball_path.exists():
                print(f"[FAIL] {pkg_name}@{ver_str}: Tarball missing at {tarball_path}")
                errors += 1
                continue

            hasher = hashlib.sha256()
            with tarball_path.open("rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            actual_integrity = f"sha256-{hasher.hexdigest()}"

            if actual_integrity != expected_integrity:
                print(
                    f"[FAIL] {pkg_name}@{ver_str}: Hash mismatch.\n"
                    f"       Expected: {expected_integrity}\n"
                    f"       Actual:   {actual_integrity}"
                )
                errors += 1
            else:
                print(f"[OK] {pkg_name}@{ver_str} ({actual_integrity[:20]}...)")

    print("-" * 50)
    print(f"Validated {package_count} package(s), {version_count} version(s). Errors: {errors}")
    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
