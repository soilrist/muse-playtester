"""3분 데모 영상 (D7, 대본 docs/specs/demo-script.md). 실측 run·리포트 + edge-tts 내레이션 → demo/playtester-demo.mp4
API 는 부르지 않는다 — SAM 박스는 tools/demo/boxes013.json 에 한 번 받아 둔 값.
    .venv/bin/pip install edge-tts   # 한 번 (say 는 기계음이라 버림)
    .venv/bin/python tools/demo/make_video.py [runs/<시각>]
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "runs/20261029-172210")
BUG = ROOT / "bugs/0048-same-screen-at-step-19/report.md"
PLAY = ROOT / "runs/20261030-083029"  # SAM 플레이어 추적이 로그에 남은 실측
OUT = ROOT / "demo/playtester-demo.mp4"
W, H = 1920, 1080
BG, FG, DIM, ACC, RED, GRN = "#101418", "#f2f2f2", "#9aa4ad", "#4da3ff", "#ff5a5a", "#4cd17a"
F = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
VOICE = "en-US-AndrewNeural"
MONO = "/System/Library/Fonts/Menlo.ttc"
KO = "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # 한글이 섞인 문장(플레이 소감)


def font(size, path=F):
    return ImageFont.truetype(path, size)


def card():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def frame(name, run=None):
    return Image.open((run or RUN) / "frames" / name).convert("RGB")


def paste(im, src, x, y, w):
    src = src.resize((w, round(src.height * w / src.width)), Image.LANCZOS)
    im.paste(src, (x, y))
    return src.size


def wrap(d, xy, s, f, fill, width):
    """width(px) 안에서 단어 단위로 줄바꿈. 다음 y 를 돌려준다."""
    x, y = xy
    line = ""
    for word in s.split():
        if d.textlength(f"{line} {word}".strip(), font=f) > width and line:
            d.text((x, y), line, font=f, fill=fill)
            y += f.size * 1.3
            line = word
        else:
            line = f"{line} {word}".strip()
    d.text((x, y), line, font=f, fill=fill)
    return y + f.size * 1.3


def title(d, s, sub=None):
    d.text((80, 50), s, font=font(56, FB), fill=FG)
    if sub:
        d.text((80, 125), sub, font=font(30), fill=DIM)


def log(run=None):
    return [json.loads(l) for l in ((run or RUN) / "log.jsonl").read_text(encoding="utf-8").splitlines()]


# ── 장면들: (그림 목록[(이미지, 비중)], 내레이션, 최소 길이초 — 그림 읽을 시간) ──

def s1():
    im, d = card()
    paste(im, frame("001.png").filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 0.3), 0, 0, W)
    d.text((120, 330), "PlayTester", font=font(150, FB), fill=FG)
    d.text((126, 510), "An AI playtester that only sees the screen.", font=font(52), fill=FG)
    d.text((126, 600), "Meta SAM 3.1  +  Muse Spark", font=font(40), fill=ACC)
    return [(im, 1)], ("Every indie developer ships bugs nobody found, because nobody played the game long enough. "
                       "PlayTester plays it for you."), 8


def s_play():
    """실측 60수를 빠르게 넘긴다 — 사람 손 없이 실제로 플레이하는 장면."""
    pics, es = [], log(PLAY)
    end = f"{es[-1]['t'] // 60:.0f}:{es[-1]['t'] % 60:02.0f}"
    for e in es:
        im, d = card()
        src = frame(Path(e["capture"]).name, PLAY)
        k = 1440 / src.width
        paste(im, src, 240, 0, 1440)
        box = lambda b, c, w: d.rectangle((240 + b[0] * k, b[1] * k, 240 + b[2] * k, b[3] * k), outline=c, width=w)
        for b in e.get("boxes", {}).get("person", []):
            if b != e.get("player"):
                box(b, ACC, 3)
        if e.get("player"):
            box(e["player"], GRN, 6)
            d.text((240 + e["player"][0] * k, e["player"][1] * k - 44), "player", font=font(34, FB), fill=GRN)
        d.rectangle((0, 930, W, H), fill=BG)
        args = " ".join(f"{v}" for k, v in e["args"].items() if k != "hold_ms")[:40]
        d.text((60, 950), f"step {e['step']:>2}   {e['tool']} {args}", font=font(40, MONO), fill=ACC)
        d.text((60, 1010), e["why"][:110], font=font(30), fill=FG)
        d.text((1560, 950), f"{e['t'] // 60:.0f}:{e['t'] % 60:02.0f} / {end}", font=font(30, MONO), fill=DIM)
        pics.append((im, 1))
    return pics, ("Here it is playing on its own: eighteen minutes, sped up. The green box is the player, found by SAM and tracked by which box moves after a move key. Every line at the bottom is one real key press and the reason the model chose it. "
                  "It skips the intro, talks to the village chief, and keeps trying keys when the character stops responding."), 16


def s2():
    im, d = card()
    title(d, "No game code. No hooks. Just the screen and real keys.")
    paste(im, frame("003.png"), 80, 220, 640)
    d.text((80, 715), "Game running in a Windows VM", font=font(28), fill=DIM)
    steps = ["1  Capture the game window", "2  SAM 3.1: what is on screen?", "3  Muse Spark: pick one action",
             "4  Press a real key (pynput)", "5  Judge: did the game respond?"]
    for i, s in enumerate(steps):
        y = 240 + i * 120
        d.rounded_rectangle((820, y, 1800, y + 90), 18, outline=ACC, width=3)
        d.text((860, y + 22), s, font=font(42), fill=FG)
    d.text((820, 860), "repeat 60 times, fully unattended", font=font(34), fill=DIM)
    return [(im, 1)], ("It sees only the screen. No game code, no hooks. "
                       "The game runs in a Windows virtual machine; PlayTester captures each frame and presses real keys."), 10


def s3():
    boxes = json.loads((ROOT / "tools/demo/boxes013.json").read_text())
    colors = {"person": GRN, "health bar": RED, "house door": ACC}
    out = []
    for draw_boxes in (False, True):
        im, d = card()
        title(d, "SAM 3.1 segments the screen", "frame 13 of the real 60-step run")
        src = frame("013.png")
        sd = ImageDraw.Draw(src)
        if draw_boxes:
            for k, bs in boxes.items():
                for x1, y1, x2, y2, c in bs:
                    sd.rectangle((x1, y1, x2, y2), outline=colors.get(k, FG), width=4)
        paste(im, src, 80, 190, 1100)
        if draw_boxes:
            y = 260
            for k, bs in boxes.items():
                d.text((1250, y), f"{len(bs)}  {k}", font=font(48, FB), fill=colors.get(k, DIM) if bs else DIM)
                y += 90
            d.text((1250, y + 30), "→ \"detected: 6 person,", font=font(34, MONO), fill=FG)
            d.text((1250, y + 80), "   2 health bar, 3 house door\"", font=font(34, MONO), fill=FG)
        out.append((im, 1 if not draw_boxes else 4))
    return out, ("Meta's SAM 3.1 segments what is on screen. Here it finds six people, two health bars and three house doors. "
                 "That becomes a short scene summary for the decision model."), 14


def s4():
    out = []
    for e in log()[10:18]:
        im, d = card()
        title(d, "Muse Spark picks one tool call per step", "press · wait · report_bug · note · done")
        paste(im, frame(Path(e["capture"]).name), 80, 190, 1080)
        x = 1220
        d.text((x, 200), f"step {e['step']}", font=font(64, FB), fill=FG)
        d.text((x, 300), e["scene"], font=font(30, MONO), fill=DIM)
        a = e["args"]
        d.text((x, 370), f"{e['tool']}({a.get('key', '')}, {a.get('hold_ms', '')}ms)", font=font(44, MONO), fill=ACC)
        d.text((x, 460), "why", font=font(30, FB), fill=DIM)
        wrap(d, (x, 505), e["why"], font(36), FG, 620)
        out.append((im, 1))
    return out, ("Muse Spark reads the scene summary and the screenshot, and picks one tool call per step: "
                 "press a key, wait, report a bug, or write a note. Every decision is logged with its reason. "
                 "Here it walks toward the village chief to start the quest."), 17


def s5():
    rows = re.findall(r"^\| (\w+) \| (바뀜|그대로) \|", BUG.read_text(encoding="utf-8"), re.M)
    im, d = card()
    title(d, "Judge: the screen stopped changing", "step 18 → 19, still pressing left")
    for i, n in enumerate(("018.png", "019.png")):
        x = 80 + i * 900
        paste(im, frame(n), x, 210, 840)
        d.text((x, 860), f"step {int(n[:3])}", font=font(40, FB), fill=FG)
    d.rectangle((980, 210, 1820, 840), outline=RED, width=8)
    d.text((1180, 860), "same_screen for 13 s", font=font(40, FB), fill=RED)
    im2, d2 = card()
    title(d2, "Then it probes every key, one by one", "before/after capture for each key")
    paste(im2, frame("019.png"), 80, 210, 900)
    for i, (k, r) in enumerate(rows):
        y = 230 + i * 80
        ok = r == "바뀜"
        d2.text((1100, y), f"{k:<6}", font=font(46, MONO), fill=FG)
        d2.text((1320, y), "screen changed" if ok else "no response", font=font(46), fill=GRN if ok else RED)
    return [(im, 1), (im2, 1.2)], ("At step nineteen the hero stops moving while it keeps pressing left. "
                                   "The judge flags the stuck screen, then probes each key one by one: "
                                   "up and down still work, left and right do nothing."), 14


def s6():
    t = BUG.read_text(encoding="utf-8")
    steps = re.findall(r"^\d+\. (.+)$", t, re.M)
    im, d = card()
    title(d, "A bug report a human can reproduce", "bugs/0048-same-screen-at-step-19/report.md")
    d.text((80, 200), "Reproduce", font=font(40, FB), fill=ACC)
    for i, s in enumerate(steps):
        d.text((80 + (i // 10) * 420, 270 + (i % 10) * 56), f"{i + 1:>2}. {s}", font=font(32, MONO), fill=FG)
    x, y = 960, 14
    for k, v, c in (
            ("Severity", "medium", FG),
            ("Expected", re.search(r"## 기대\n(.+)", t)[1], FG),
            ("Actual", re.search(r"## 실제\n(.+)", t)[1], FG),
            ("Evidence", "frames 018, 019  +  per-key probe table (8 keys)", FG)):
        d.text((x, y), k, font=font(40, FB), fill=ACC)
        y = wrap(d, (x, y + 55), v, font(36), c, 880) + 30
    return [(im, 1)], ("It writes a report a human can reproduce: the exact key sequence, expected and actual behaviour, "
                       "evidence frames, and the per-key probe table."), 12


def s7():
    t = (RUN / "playtest_notes.md").read_text(encoding="utf-8")
    items = re.findall(r"^## \d+\. (.+?)\n\n- 근거 장면: (\d+)수째.*?\n- 장르 비교: .*?\n- 제안: (.+?)$", t, re.M | re.S)
    im, d = card()
    title(d, "Playtest notes: UX feedback, each backed by a scene")
    for i, (what, step, fix) in enumerate(items[:3]):
        y = 170 + i * 300
        paste(im, frame(f"{int(step):03d}.png"), 80, y, 340)
        d.text((460, y), f"step {step}", font=font(30, FB), fill=DIM)
        yy = wrap(d, (460, y + 45), what, font(34, KO), FG, 1360)
        wrap(d, (460, yy + 5), "Suggestion: " + fix, font(30, KO), ACC, 1360)
    return [(im, 1)], ("Notes become playtest feedback, each backed by a real scene and compared with what the genre usually does."), 10


def s8():
    summ = (RUN / "summary.md").read_text(encoding="utf-8")
    n = re.search(r"수: (\d+)", summ)[1]
    im, d = card()
    d.text((120, 220), f"{n} actions · unattended · ~$0.82 in API calls", font=font(64, FB), fill=FG)
    d.text((120, 340), "SAM 3.1 sees  ·  Muse Spark decides  ·  real keys  ·  reproducible reports", font=font(40), fill=DIM)
    d.text((120, 560), "github.com/soilrist/muse-playtester", font=font(60, FB), fill=ACC)
    d.text((120, 650), "Open source", font=font(40), fill=DIM)
    return [(im, 1)], f"{n} actions, about eighty cents. PlayTester is open source on GitHub.", 8


def sh(*a):
    subprocess.run(a, check=True, capture_output=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                check=True, capture_output=True, text=True).stdout)


def main():
    OUT.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        vlist, alist, total = [], [], 0.0
        for si, scene in enumerate((s1, s_play, s2, s3, s4, s5, s6, s7, s8), 1):
            pics, text, planned = scene()
            aiff = tmp / f"s{si}.mp3"
            sh(str(Path(sys.executable).parent / "edge-tts"), "--voice", VOICE, "--text", text, "--write-media", str(aiff))
            length = max(planned, dur(aiff) + 1.5)  # 말이 끝나면 곧 다음 장면 — 빈 소리 구간을 안 만든다
            wav = tmp / f"s{si}.wav"
            sh("ffmpeg", "-y", "-i", str(aiff), "-af", f"adelay=400|400,apad", "-t", f"{length:.3f}", "-ar", "48000", "-ac", "2", str(wav))
            alist.append(f"file '{wav}'")
            weight = sum(w for _, w in pics)
            for pi, (im, w) in enumerate(pics):
                png = tmp / f"s{si}-{pi}.png"
                im.save(png)
                vlist += [f"file '{png}'", f"duration {length * w / weight:.3f}"]
            total += length
            print(f"scene {si}: {length:.1f}s")
        vlist.append(vlist[-2])  # concat demuxer 는 마지막 그림의 duration 을 쓰려면 한 번 더 적어야 한다
        (tmp / "v.txt").write_text("\n".join(vlist))
        (tmp / "a.txt").write_text("\n".join(alist))
        sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "v.txt"), "-f", "concat", "-safe", "0", "-i", str(tmp / "a.txt"),
           "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", str(OUT))
        print(f"total {total:.1f}s → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
