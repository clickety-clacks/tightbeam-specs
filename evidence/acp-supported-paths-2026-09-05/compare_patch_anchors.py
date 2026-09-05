"""Read source literals and compare text only; do not execute adapter or Tightbeam code."""
import json
import pathlib
import sys

source = pathlib.Path(sys.argv[1]).read_text()
bundle = pathlib.Path(sys.argv[2]).read_text()
block = source.split("@adapter_replacements [", 1)[1].split("\n  ]", 1)[0]
literals = []
for line in block.splitlines():
    value = line.strip().removesuffix(",")
    if value.startswith('"'):
        literals.append(json.loads(value))
assert len(literals) % 2 == 0
print(json.dumps({
    "method": "static literal comparison; no product code executed",
    "source": sys.argv[1], "bundle": sys.argv[2],
    "replacements": [
        {"index": i // 2 + 1, "before_count": bundle.count(literals[i]),
         "after_count": bundle.count(literals[i + 1])}
        for i in range(0, len(literals), 2)
    ]
}, indent=2))
