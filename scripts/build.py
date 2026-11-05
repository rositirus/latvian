"""Build index.html from content/curriculum.txt and scripts/template.html."""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUP_ORDER_FIRST = ["Basics", "Settling in"]


def audio_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:10]


def parse(path=ROOT / "content" / "curriculum.txt"):
    modules, group = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("# Latvian curriculum") or line.startswith("# Format:"):
            continue
        if line.startswith("## "):
            group = line[3:]
            continue
        if line.startswith("# "):
            modules.append({"t": line[2:], "g": group, "w": [], "s": []})
            continue
        sentence = line.startswith("> ")
        if sentence:
            line = line[2:]
        say = None
        m = re.search(r"\s*\{say:\s*(.+?)\}\s*$", line)
        if m:
            say, line = m.group(1), line[: m.start()]
        lv, en = [x.strip() for x in line.split(" = ", 1)]
        modules[-1]["s" if sentence else "w"].append([lv, en])
        if say:
            modules[-1].setdefault("say", {})[lv] = say
    order = []
    for mod in modules:
        if mod["g"] not in order:
            order.append(mod["g"])
    for g in reversed(GROUP_ORDER_FIRST):
        if g in order:
            order.remove(g)
            order.insert(0, g)
    modules.sort(key=lambda mod: order.index(mod["g"]))  # stable
    return modules


def items(modules):
    """Yield (display_text, spoken_text, rate) for every clip."""
    for mod in modules:
        for lv, _ in mod["w"] + mod["s"]:
            spoken = mod.get("say", {}).get(lv)
            yield lv, spoken or lv, "-25%" if spoken else "-10%"


def main():
    modules = parse()
    aid = {lv: audio_id(lv) for lv, _, _ in items(modules)}
    data = [{k: v for k, v in mod.items() if k != "say"} for mod in modules]
    html = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__AID__", json.dumps(aid))
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    words = sum(len(m["w"]) for m in modules)
    sents = sum(len(m["s"]) for m in modules)
    print(f"Built {out.relative_to(ROOT)}: {len(modules)} modules, {words} words, {sents} sentences, {len(aid)} audio clips")


if __name__ == "__main__":
    main()
