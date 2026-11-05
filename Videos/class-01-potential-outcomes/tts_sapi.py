"""Stand-in narration with the offline Windows voice (System.Speech), until Speechify has credits.

Same contract as `speechify-tts --script`: one clip per beat in audio/, duration MEASURED with
ffprobe and written to beats.json. A beat whose text is unchanged keeps its clip (text hash).
Paragraph breaks become a 600 ms pause. Swap back with `speechify-tts --script beats.json`
(the scenes then need re-rendering, because every duration changes).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
VOICE = "Microsoft Zira Desktop"
RATE = 0  # -10..10

PS = r"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('{voice}')
$s.Rate = {rate}
$p = New-Object System.Speech.Synthesis.PromptBuilder
$paras = (Get-Content -Raw -Encoding UTF8 '{txt}') -split "`n`n"
foreach ($para in $paras) {{ $p.AppendText($para.Trim()); $p.AppendBreak([TimeSpan]::FromMilliseconds(600)) }}
$s.SetOutputToWaveFile('{wav}')
$s.Speak($p)
$s.Dispose()
"""


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(out.stdout.strip())


def main():
    manifest_path = HERE / "beats.json"
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    audio = HERE / "audio"
    audio.mkdir(exist_ok=True)
    for b in m["beats"]:
        sha = hashlib.sha256(f"{VOICE}|{RATE}|{b['text']}".encode()).hexdigest()[:16]
        wav = audio / f"{b['id']}.wav"
        if b.get("sha") == sha and wav.exists():
            print(f"  = {b['id']:<22} unchanged {b['seconds']:.3f}s")
            continue
        txt = audio / f"{b['id']}.txt"
        txt.write_text(b["text"], encoding="utf-8")
        script = PS.format(voice=VOICE, rate=RATE, txt=txt.resolve(), wav=wav.resolve())
        subprocess.run(["powershell", "-NoProfile", "-Command", script], check=True)
        txt.unlink()
        b.update(audio=f"audio/{wav.name}", seconds=round(probe(wav), 3), sha=sha)
        print(f"  + {b['id']:<22} {b['seconds']:>8.3f}s")
    m["voice"] = f"windows-sapi:{VOICE}"
    m["model"] = "System.Speech"
    m["total_seconds"] = round(sum(b["seconds"] for b in m["beats"]), 3)
    manifest_path.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"total {m['total_seconds'] / 60:.1f} min")


if __name__ == "__main__":
    sys.exit(main())
