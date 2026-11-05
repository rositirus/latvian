"""Generate one MP3 per word/sentence into audio/ (skips existing files).

Uses Microsoft's Latvian neural voice (lv-LV-EveritaNeural) via the `edge-tts` package.
Usage:  pip install edge-tts  &&  python scripts/generate_audio.py
"""
import asyncio, os, sys
import edge_tts
from build import ROOT, parse, items, audio_id

VOICE = "lv-LV-EveritaNeural"
OUT = ROOT / "audio"


async def one(sem, text, spoken, rate, failed):
    path = OUT / f"{audio_id(text)}.mp3"
    if path.exists() and path.stat().st_size > 800:
        return
    spoken = spoken.replace("…", "").replace(" / ", ", ")
    async with sem:
        for _ in range(4):
            try:
                await edge_tts.Communicate(spoken, VOICE, rate=rate).save(str(path))
                return
            except Exception:
                await asyncio.sleep(3)
    failed.append(text)


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clips = {t: (s, r) for t, s, r in items(parse())}
    sem, failed = asyncio.Semaphore(8), []
    await asyncio.gather(*(one(sem, t, s, r, failed) for t, (s, r) in clips.items()))
    used = {f"{audio_id(t)}.mp3" for t in clips}
    unused = [p.name for p in OUT.glob("*.mp3") if p.name not in used]
    print(f"{len(clips)} clips, {len(failed)} failed, {len(unused)} unused files")
    if failed:
        print("Failed:", failed)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
