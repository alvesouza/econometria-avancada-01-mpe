"""Parse script.md into beats.json (the timing contract).

Spoken text = everything under a `## <BeatId>` heading, minus `>` note lines.
Seconds are estimated at 150 wpm until speechify-tts replaces them with measured values;
an existing measured duration is kept when the beat's text is unchanged.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
WPM = 150


def parse(md):
    beats, cur = [], None
    for line in md.splitlines():
        m = re.match(r"^## (\w+)\s*$", line)
        if m:
            cur = {"id": m.group(1), "lines": []}
            beats.append(cur)
        elif cur is not None and not line.startswith(">"):
            cur["lines"].append(line)
    out = []
    for b in beats:
        paras = [" ".join(p.split()) for p in "\n".join(b["lines"]).split("\n\n")]
        out.append({"id": b["id"], "text": "\n\n".join(p for p in paras if p)})
    return out


def main():
    new = parse((HERE / "script.md").read_text(encoding="utf-8"))
    path = HERE / "beats.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"voice": None}
    prev = {b["id"]: b for b in old.get("beats", [])}
    for b in new:
        p = prev.get(b["id"])
        if p and p.get("text") == b["text"] and p.get("audio"):
            b.update(audio=p["audio"], seconds=p["seconds"])
        else:
            b.update(audio="", seconds=round(len(b["text"].split()) / WPM * 60, 3))
    manifest = {"voice": old.get("voice"), "model": old.get("model"),
                "total_seconds": round(sum(b["seconds"] for b in new), 3), "beats": new}
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    for b in new:
        print(f"{b['id']:<22}{len(b['text'].split()):>5} words {b['seconds']:>8.1f}s")
    print(f"total {manifest['total_seconds'] / 60:.1f} min, voice={manifest['voice']}")


if __name__ == "__main__":
    sys.exit(main())
