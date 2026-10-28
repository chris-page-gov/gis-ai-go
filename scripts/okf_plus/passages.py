"""Offline, private, lossless Markdown evidence passages; never execute source text.

Offsets are zero-based and end-exclusive; line numbers are one-based. Every
passage contains part of exactly one source line, including its original newline.
The manifest is an index and is not subject to the individual passage byte limit.
"""
from __future__ import annotations

import argparse
import ctypes
import os
import shutil
import tempfile
import hashlib
import re
from pathlib import Path

try:
    from .documentation import document_url
    from .model import PREFIXES, canonical, load_json
except ImportError:
    from documentation import document_url
    from model import PREFIXES, canonical, load_json

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAX_BYTES = 16 * 1024
CONTEXT = {**PREFIXES, **{key: {'@id': 'okfp:' + key, '@type': '@json'} for key in
    ('source', 'position', 'headingBreadcrumb', 'part', 'text', 'trust', 'distribution',
     'segments', 'reconstruction', 'maxPassageBytes')}}
TRUST = {'status': 'untrusted-source-evidence', 'executionAdmitted': False}
DISTRIBUTION = {'audience': 'private', 'publicationAdmitted': False}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def no_symlinks(path):
    path = Path(path).absolute()
    if '..' in path.parts:
        raise ValueError('Parent traversal paths are not admitted')
    if any(item.is_symlink() for item in (path, *path.parents)):
        raise ValueError('Symbolic link paths are not admitted')
    return path


def split_document(raw, url, *, max_bytes=DEFAULT_MAX_BYTES):
    """Return manifest and serialised passages without modifying the source."""
    document_url(url, prefix=('/osngd/', '/os-downloads/', '/os-apis/'))
    if type(max_bytes) is not int or max_bytes < 1:
        raise ValueError('Passage byte limit must be a positive integer')
    if not isinstance(raw, bytes):
        raise ValueError('Source must be original bytes')
    text = raw.decode('utf-8', errors='strict')
    source = {'url': url, 'sha256': sha256(raw), 'bytes': len(raw), 'encoding': 'UTF-8'}
    base = 'urn:sha256:' + sha256(url.encode() + b'\0' + raw)
    passages, segments, breadcrumbs = [], [], []
    byte_offset = char_offset = 0
    fence = None
    # splitlines keeps CRLF, LF, CR and other Unicode line delimiters intact.
    for line_number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0], len(marker[1])
            elif marker[1][0] == fence[0] and len(marker[1]) >= fence[1]:
                fence = None
        heading = re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if heading and fence is None:
            level = len(heading[1])
            breadcrumbs = [h for h in breadcrumbs if h['level'] < level]
            breadcrumbs.append({'level': level, 'text': heading[2], 'line': line_number})
        start = 0
        line_byte = 0
        while start < len(line):
            number = len(passages) + 1
            def candidate(end):
                chunk = line[start:end]
                return {'@context': CONTEXT, '@id': base + ':part:' + str(number),
                    '@type': 'okfp:PrivateEvidencePassage', 'source': source,
                    'position': {'lineStart': line_number, 'lineEnd': line_number,
                        'byteStart': byte_offset + line_byte,
                        'byteEnd': byte_offset + line_byte + len(chunk.encode()),
                        'characterStart': char_offset + start, 'characterEnd': char_offset + end,
                        'lineCharacterStart': start, 'lineCharacterEnd': end,
                        'lineByteStart': line_byte, 'lineByteEnd': line_byte + len(chunk.encode())},
                    'headingBreadcrumb': breadcrumbs.copy(), 'part': number, 'text': chunk,
                    'trust': TRUST, 'distribution': DISTRIBUTION}
            low, high, best = start + 1, len(line), None
            while low <= high:
                mid = (low + high) // 2
                encoded = canonical(candidate(mid))
                if len(encoded) <= max_bytes:
                    best = mid, encoded
                    low = mid + 1
                else:
                    high = mid - 1
            if best is None:
                raise ValueError('Passage metadata and one character exceed byte limit')
            end, encoded = best
            name = f'part-{number:08d}.jsonld'
            segments.append({'file': name, 'part': number, 'sha256': sha256(encoded),
                             'bytes': len(encoded), 'position': candidate(end)['position']})
            passages.append(encoded)
            line_byte += len(line[start:end].encode())
            start = end
        byte_offset += len(line.encode())
        char_offset += len(line)
    rebuilt = b''.join(load_json(p.decode())['text'].encode() for p in passages)
    if rebuilt != raw:
        raise ValueError('Source reconstruction failed')
    manifest = {'@context': CONTEXT, '@id': base, '@type': 'okfp:PrivateEvidenceManifest',
        'source': source, 'trust': TRUST, 'distribution': DISTRIBUTION,
        'maxPassageBytes': max_bytes, 'segments': segments,
        'reconstruction': {'verified': True, 'sha256': sha256(rebuilt), 'bytes': len(rebuilt),
                           'rule': 'Concatenate UTF-8 encoded text in segment order; no delimiter added.'}}
    return manifest, passages


def write_document(source_path, url, output, *, max_bytes=DEFAULT_MAX_BYTES):
    source_path, output = no_symlinks(source_path), no_symlinks(output)
    # CLI and library writes stay inside the repository's ignored private artefacts.
    if not output.is_relative_to(ROOT / 'artifacts') or output == ROOT / 'artifacts':
        raise ValueError('Output must be a new directory beneath ignored artifacts/')
    if not source_path.is_file():
        raise ValueError('Source must be a regular file')
    if output.exists():
        raise ValueError('Output already exists; preserve the previous evidence')
    manifest, passages = split_document(source_path.read_bytes(), url, max_bytes=max_bytes)
    output.parent.mkdir(parents=True, exist_ok=True)
    no_symlinks(output.parent)
    stage = Path(tempfile.mkdtemp(prefix='.' + output.name + '-staging-', dir=output.parent))
    try:
        for segment, payload in zip(manifest['segments'], passages):
            (stage / segment['file']).write_bytes(payload)
        (stage / 'manifest.jsonld').write_bytes(canonical(manifest))
        # Verify persisted bytes before publishing the complete directory.
        persisted = load_json((stage / 'manifest.jsonld').read_text(encoding='utf-8'))
        restored = []
        for segment in persisted['segments']:
            payload = (stage / segment['file']).read_bytes()
            if sha256(payload) != segment['sha256'] or len(payload) != segment['bytes']:
                raise ValueError('Staged passage checksum mismatch')
            restored.append(load_json(payload.decode())['text'].encode())
        if sha256(b''.join(restored)) != persisted['source']['sha256']:
            raise ValueError('Staged source reconstruction mismatch')
        no_symlinks(output)
        # Linux renameat2 provides atomic publication with a kernel-enforced
        # no-replace condition, including a concurrently created empty directory.
        # Fail closed if unavailable; ordinary rename can overwrite that directory.
        libc = ctypes.CDLL(None, use_errno=True)
        rename = getattr(libc, 'renameat2', None)
        if rename is None:
            raise OSError('Atomic no-replace directory publication requires renameat2')
        rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        if rename(-100, os.fsencode(stage), -100, os.fsencode(output), 1):
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error), str(output))
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--url', required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--max-bytes', type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args()
    write_document(args.source, args.url, args.output, max_bytes=args.max_bytes)


if __name__ == '__main__':
    main()
