# -*- coding: utf-8 -*-
"""
Sinh file dich tieng Anh (django.po + django.mo) cho nut VIE/ENG.

Vi may Windows khong co 'msgfmt'/'xgettext' (bo gettext) nen 'manage.py
makemessages/compilemessages' khong chay duoc. Script nay tu lam ca 2 viec:

  1) TRICH msgid truc tiep tu cac template (nguon chuan):
       - {% trans "..." %}  /  {% trans '...' %}  /  _("...")
       - {% blocktrans %}...{% endblocktrans %}  (doi {{ bien }} -> %(bien)s
         dung dinh dang msgid cua Django)
  2) GHEP voi ban dich trong locale/translations_en.json roi sinh .po + .mo.

Cach dung:  python locale/build_translations.py
Sua/them ban dich: chinh locale/translations_en.json rồi chạy lại lệnh trên.
"""
import os
import re
import json
import glob
import struct

BASE = os.path.dirname(os.path.abspath(__file__))      # .../locale
PROJ = os.path.dirname(BASE)                            # .../vaccine_clinic
TPL_DIR = os.path.join(PROJ, "core", "templates")
JSON_PATH = os.path.join(BASE, "translations_en.json")
OUT_DIR = os.path.join(BASE, "en", "LC_MESSAGES")

HEADER = (
    "Project-Id-Version: vaccine_clinic\n"
    "Report-Msgid-Bugs-To: \n"
    "MIME-Version: 1.0\n"
    "Content-Type: text/plain; charset=UTF-8\n"
    "Content-Transfer-Encoding: 8bit\n"
    "Language: en\n"
    "Plural-Forms: nplurals=2; plural=(n != 1);\n"
)

# Cac mau bat chuoi dich trong template
RX_TRANS_D = re.compile(r'{%\s*(?:trans|translate)\s+"((?:[^"\\]|\\.)*)"\s*%}')
RX_TRANS_S = re.compile(r"{%\s*(?:trans|translate)\s+'((?:[^'\\]|\\.)*)'\s*%}")
RX_GETTEXT_D = re.compile(r'_\(\s*"((?:[^"\\]|\\.)*)"\s*\)')
RX_GETTEXT_S = re.compile(r"_\(\s*'((?:[^'\\]|\\.)*)'\s*\)")
RX_BLOCK = re.compile(r'{%\s*blocktrans\b[^%]*%}(.*?){%\s*endblocktrans\s*%}', re.DOTALL)
RX_VAR = re.compile(r'{{\s*([\w]+)\s*}}')


def normalize(text):
    """Doi {{ bien }} -> %(bien)s giong cach Django tao msgid cho blocktrans."""
    return RX_VAR.sub(r'%(\1)s', text)


def unescape(s):
    return s.replace('\\"', '"').replace("\\'", "'")


def extract_msgids():
    ids = set()
    for path in glob.glob(os.path.join(TPL_DIR, "**", "*.html"), recursive=True):
        with open(path, encoding="utf-8") as f:
            s = f.read()
        for rx in (RX_TRANS_D, RX_TRANS_S, RX_GETTEXT_D, RX_GETTEXT_S):
            for m in rx.finditer(s):
                ids.add(unescape(m.group(1)))
        for m in RX_BLOCK.finditer(s):
            ids.add(normalize(m.group(1)))
    # Quet them cac file Python (.py) trong core
    for path in glob.glob(os.path.join(PROJ, "core", "**", "*.py"), recursive=True):
        with open(path, encoding="utf-8") as f:
            s = f.read()
        for rx in (RX_GETTEXT_D, RX_GETTEXT_S):
            for m in rx.finditer(s):
                ids.add(unescape(m.group(1)))
    return ids


def po_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def write_po(path, mapping):
    lines = [
        "# Ban dich tieng Anh (sinh tu build_translations.py).",
        'msgid ""',
        'msgstr ""',
    ]
    for part in HEADER.split("\n"):
        if part:
            lines.append('"%s\\n"' % part)
    lines.append("")
    for src in sorted(mapping):
        lines.append('msgid "%s"' % po_escape(src))
        lines.append('msgstr "%s"' % po_escape(mapping[src]))
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_mo(path, mapping):
    items = [("", HEADER)] + sorted(mapping.items())
    keys = [k.encode("utf-8") for k, _ in items]
    vals = [v.encode("utf-8") for _, v in items]
    n = len(items)
    start = 28 + n * 8 + n * 8
    blob = b""
    off_k, off_v = [], []
    for k in keys:
        off_k.append((len(k), start + len(blob)))
        blob += k + b"\x00"
    for v in vals:
        off_v.append((len(v), start + len(blob)))
        blob += v + b"\x00"
    out = struct.pack("<Iiiiiii", 0x950412de, 0, n, 28, 28 + n * 8, 0, 0)
    for length, off in off_k:
        out += struct.pack("<ii", length, off)
    for length, off in off_v:
        out += struct.pack("<ii", length, off)
    out += blob
    with open(path, "wb") as f:
        f.write(out)


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    # Chuan hoa ca key lan value sang dang %(bien)s de khop msgid cua Django
    lookup = {normalize(k): normalize(v) for k, v in raw.items()}

    ids = extract_msgids()
    mapping = {}
    missing = []
    for mid in ids:
        if mid in lookup:
            mapping[mid] = lookup[mid]
        else:
            missing.append(mid)

    os.makedirs(OUT_DIR, exist_ok=True)
    write_po(os.path.join(OUT_DIR, "django.po"), mapping)
    write_mo(os.path.join(OUT_DIR, "django.mo"), mapping)

    print("Tong chuoi dich trong template : %d" % len(ids))
    print("Da co ban dich (vao .mo)        : %d" % len(mapping))
    print("Chua co ban dich (giu tieng Viet): %d" % len(missing))
    if missing:
        print("--- Mot so chuoi chua dich (toi da 100) ---")
        for s in sorted(missing)[:100]:
            print("  | " + s.replace("\n", " ")[:90])


if __name__ == "__main__":
    main()
