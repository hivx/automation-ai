#!/usr/bin/env python3
"""Checks JSON files against a JSON Schema (draft-07 subset, standard library only).

Supported: type (including a list of types), enum, required, properties, additionalProperties
(bool or schema), items, minimum, minLength, pattern.
Usage: scripts/check-profile.py <schema.json> <file.json> [<file.json> ...]
Prints one line per problem `<file>: <JSON path>: <problem>`; exit code 1 when there are problems.
"""
import json
import re
import sys

TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def check(value, schema, path, problems):
    types = schema.get("type")
    if types is not None:
        types = types if isinstance(types, list) else [types]
        if not any(TYPES[t](value) for t in types):
            problems.append(f"{path}: expected {'|'.join(types)}, got {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        problems.append(f"{path}: {json.dumps(value, ensure_ascii=False)} not in {schema['enum']}")
    if "minimum" in schema and TYPES["number"](value) and value < schema["minimum"]:
        problems.append(f"{path}: {value} < minimum {schema['minimum']}")
    if "pattern" in schema and isinstance(value, str) and not re.search(schema["pattern"], value):
        problems.append(f"{path}: {json.dumps(value, ensure_ascii=False)} does not match pattern {schema['pattern']}"
                        + (f" ({schema['description']})" if schema.get("description") else ""))
    if "minLength" in schema and isinstance(value, str) and len(value) < schema["minLength"]:
        problems.append(f"{path}: shorter than {schema['minLength']}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                problems.append(f"{path}: missing required '{key}'")
        addl = schema.get("additionalProperties", True)
        for key, sub in value.items():
            child = f"{path}.{key}"
            if key in props:
                check(sub, props[key], child, problems)
            elif addl is False:
                problems.append(f"{path}: unknown key '{key}'")
            elif isinstance(addl, dict):
                check(sub, addl, child, problems)
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(value):
            check(item, schema["items"], f"{path}[{i}]", problems)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    if len(argv) < 2:
        print(__doc__.strip().split("\n")[3], file=sys.stderr)
        return 64
    schema = load(argv[0])
    bad = 0
    for path in argv[1:]:
        try:
            data = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{path}: $: cannot read JSON: {exc}")
            bad += 1
            continue
        problems = []
        check(data, schema, "$", problems)
        for p in problems:
            print(f"{path}: {p}")
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
