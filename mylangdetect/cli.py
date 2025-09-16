#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for MyLangDetect.

Examples:
  # Single text
  mylang-detect "Hello, how are you?"

  # Top-3 with JSON
  mylang-detect -k 3 -j "Привет, как дела?"

  # From file
  mylang-detect -f path/to/text.txt

  # Interactive mode (no args)
  mylang-detect
"""

from __future__ import annotations

import argparse
import sys
import os
import json
from typing import List

from . import (
    __version__,
    detect_language,
    detect_language_detailed,
    get_supported_languages,
    TfidfLangID,
)


def _read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog='mylang-detect',
        description='Language detection using TF-IDF model (MyLangDetect)'
    )
    p.add_argument('text', nargs='?', help='Text to analyze (optional if --file or interactive)')
    p.add_argument('-f', '--file', action='append', default=[], help='Path to a text file (can be repeated)')
    p.add_argument('-k', '--top-k', type=int, default=1, help='Number of top predictions (default: 1)')
    p.add_argument('-j', '--json', action='store_true', help='Output JSON')
    p.add_argument('-l', '--list-langs', action='store_true', help='List supported language codes and exit')
    p.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    return p.parse_args()


def _format_result(res: dict, top_k: int) -> str:
    lang = res.get('language', '')
    conf = res.get('confidence', 0.0)
    out = [f"{lang} ({conf*100:.1f}%)"]
    if top_k and res.get('top_k'):
        out.append('Top: ' + ', '.join(f"{l}:{c*100:.1f}%" for l, c in res['top_k'][:top_k]))
    return ' | '.join(out)


def _detect_texts(texts: List[str], top_k: int) -> List[dict]:
    # Use class directly to avoid reinitializing global detector for batch
    detector = TfidfLangID.load_from_package()
    return detector.predict(texts, top_k=max(1, top_k))


def main() -> None:
    args = parse_args()

    # List languages
    if args.list_langs:
        langs = get_supported_languages()
        if args.json:
            print(json.dumps({'languages': langs}, ensure_ascii=False))
        else:
            print(' '.join(langs))
        return

    inputs: List[str] = []
    if args.text:
        inputs.append(args.text)
    if args.file:
        for p in args.file:
            if not os.path.exists(p):
                print(f"File not found: {p}", file=sys.stderr)
                sys.exit(2)
            inputs.append(_read_file(p))

    # Interactive mode
    if not inputs:
        print('MyLangDetect interactive mode. Type text or "quit" to exit.')
        detector = TfidfLangID.load_from_package()
        while True:
            try:
                line = input('> ').strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                continue
            if line.lower() in {'q', 'quit', 'exit'}:
                break
            res = detector.predict_one(line, top_k=max(1, args.top_k))
            if args.json:
                print(json.dumps(res, ensure_ascii=False))
            else:
                print(_format_result(res, args.top_k))
        return

    # Batch or single input
    results = _detect_texts(inputs, top_k=args.top_k)
    if args.json:
        # If single input, print single object; else list
        if len(results) == 1:
            print(json.dumps(results[0], ensure_ascii=False))
        else:
            print(json.dumps(results, ensure_ascii=False))
    else:
        for i, res in enumerate(results, 1):
            prefix = '' if len(results) == 1 else f'[{i}] '
            print(prefix + _format_result(res, args.top_k))


if __name__ == '__main__':
    main()

