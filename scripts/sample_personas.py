#!/usr/bin/env python3
"""Sample random "ordinary" personas for the diverse-opinions skill.

The personas come from PersonaHub (Ge et al. 2024), the same public dataset the
paper "A Cognitive Framework for Idea Diversity in Large Language Models" drew
its ordinary personas from. The file is downloaded once into a local cache and
is never copied into a repository. Its license is CC BY-NC-SA 4.0.

Usage: sample_personas.py [--n 8] [--seed 123] [--source PATH_OR_URL]
Prints one JSON object: {"seed": ..., "source": ..., "personas": [...]}
Exits with status 2 and a message on stderr if the file cannot be read, so the
caller can fall back to another way of getting personas.
"""
import argparse
import json
import os
import random
import sys
import tempfile
import urllib.request

URL = "https://huggingface.co/datasets/proj-persona/PersonaHub/resolve/main/persona.jsonl"
CACHE = os.path.expanduser("~/.cache/diverse-opinions/persona.jsonl")
MIN_BYTES = 1_000_000  # the real file is about 21 MB; anything tiny is an error page


def fetch(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dest), suffix=".part")
    try:
        with os.fdopen(fd, "wb") as out, urllib.request.urlopen(url, timeout=60) as resp:
            while chunk := resp.read(1 << 20):
                out.write(chunk)
        if os.path.getsize(tmp) < MIN_BYTES:
            raise RuntimeError("downloaded file is too small to be the persona list")
        os.replace(tmp, dest)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def read_personas(path: str) -> list[str]:
    personas = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                text = json.loads(line).get("persona", "").strip()
            except (json.JSONDecodeError, AttributeError):
                continue
            if text:
                personas.append(text)
    return personas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--source", default=None, help="local file path or URL; default is the cached PersonaHub file")
    args = ap.parse_args()

    try:
        path = args.source or CACHE
        if path.startswith("http"):
            fetch(path, CACHE)
            path = CACHE
        elif not os.path.exists(path):
            if args.source:
                raise FileNotFoundError(path)
            fetch(URL, CACHE)  # first run: download into the cache
        personas = read_personas(path)
    except Exception as e:  # network, disk or format problems all mean "fall back"
        print(f"could not load personas: {e}", file=sys.stderr)
        return 2

    if len(personas) < args.n:
        print(f"only {len(personas)} personas available, need {args.n}", file=sys.stderr)
        return 2

    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**32)
    chosen = random.Random(seed).sample(personas, args.n)
    print(json.dumps({"seed": seed, "source": path, "personas": chosen}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
