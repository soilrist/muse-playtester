"""3분 데모 영상 (D7, 대본 docs/specs/demo-script.md). 실측 run·리포트 + edge-tts 내레이션 → demo/playtester-demo.mp4
API 는 부르지 않는다 — SAM 박스·판단은 run 의 log.jsonl, 플레이 장면은 VM 녹화본(tools/demo/record.py → vm/rec/).
    .venv/bin/pip install edge-tts   # 한 번 (say 는 기계음이라 버림)
    .venv/bin/python tools/demo/make_video.py [runs/<시각>]
"""
import bisect
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "runs/20261102-150749")  # 녹화하며 돈 Godot 60수 실측
BUG = ROOT / "bugs/0058-same-screen-at-step-18/report.md"
REC = ROOT / "vm/rec"  # tools/demo/record.py 녹화본 (VM → 맥 복사)
SNARE = ROOT / "runs/20261102-152538"  # Snarehaven(UE5) Win64 실측
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


FPS = 30


def footage(rec, run, segs, head):
    """VM 에서 녹화한 실제 플레이(tools/demo/record.py) 를 구간마다 배속해 자막을 얹는다.
    segs: [(시작초, 끝초, 배속)] — 초는 1수 캡처부터. 자막은 log.jsonl 의 t(그 수를 결정한 시각)부터 그 수.
    (프레임 생성기, 프레임 수) 를 돌려준다 — main 이 ffmpeg 에 바로 흘린다."""
    shots = sorted(int(p.stem) / 1000 for p in rec.glob("*.jpg"))
    es = log(run)
    e0 = (run / "frames" / "001.png").stat().st_mtime  # 맥·VM 시계 차는 0.1초 (rec-clock.txt 로 잼)
    end = es[-1]["t"]

    def gen():
        cache = (None, None)
        for a, b, speed in segs:
            for i in range(int((b - a) * FPS / speed)):
                tt = a + i * speed / FPS
                k = min(bisect.bisect_left(shots, e0 + tt), len(shots) - 1)
                if cache[0] != k:
                    src = Image.open(rec / f"{round(shots[k] * 1000)}.jpg").convert("RGB")
                    s = min(W / src.width, 900 / src.height)
                    cache = (k, src.resize((round(src.width * s), round(src.height * s)), Image.BILINEAR))
                im, d = card()
                src = cache[1]
                gx, gy = (W - src.width) // 2, 50 + (900 - src.height) // 2
                im.paste(src, (gx, gy))
                d.text((60, 8), head, font=font(30, FB), fill=DIM)
                d.text((W - 380, 8), f"{tt // 60:.0f}:{tt % 60:04.1f} / {end // 60:.0f}:{end % 60:02.0f}  ×{speed}", font=font(30, MONO), fill=DIM)
                e = next((e for e in reversed(es) if e["t"] <= tt), None)
                if e is None:
                    d.text((60, 975), "capturing the screen, asking SAM 3.1 and Muse Spark…", font=font(36), fill=DIM)
                    yield im
                    continue
                a_ = e["args"]
                if e["tool"] == "click" and tt - e["t"] < 1.5:
                    x, y = gx + a_["x"] * src.width, gy + a_["y"] * src.height
                    d.ellipse((x - 30, y - 30, x + 30, y + 30), outline=RED, width=8)
                arg = (f"({a_['x']:.2f}, {a_['y']:.2f})" if e["tool"] == "click" else
                       " ".join(str(v) for k, v in a_.items() if k in ("key", "ms", "kind")))
                d.text((60, 960), f"step {e['step']:>2}  {e['tool']} {arg}", font=font(40, MONO), fill=ACC)
                d.text((60, 1018), e["why"][:115], font=font(30, KO), fill=FG)
                if e.get("findings") and tt - e["t"] < 4:
                    d.rounded_rectangle((W - 620, 960, W - 40, 1040), 14, fill=RED)
                    d.text((W - 595, 975), "bug flagged: " + ", ".join(e["findings"])[:24], font=font(38, FB), fill=FG)
                yield im
    return gen(), sum(int((b - a) * FPS / s) for a, b, s in segs)


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
    """VM 에서 녹화한 실제 플레이 — 타이틀부터 인트로 대화까지. 자막은 그 수의 키와 Spark 가 댄 이유."""
    return footage(REC / "godot", RUN, [(0, 136, 8)], "Real recording · Godot 4 game in a Windows VM · no human input"), (
        "This is a real recording, sped up eight times. Nobody is touching the keyboard. "
        "Every caption is one real key press and the reason Muse Spark chose it. "
        "It starts a new game and reads the intro. When Enter stops advancing the dialogue, it writes that down as UX feedback and tries other keys."), 0


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
    e = log()[14]  # 15수째: 사람 6·체력바 2, 플레이어 추적이 잡힌 첫 수
    colors = {"person": GRN, "health bar": RED}
    out = []
    for draw_boxes in (False, True):
        im, d = card()
        title(d, "SAM 3.1 segments the screen", f"step {e['step']} of the recorded run")
        src = frame(Path(e["capture"]).name)
        sd = ImageDraw.Draw(src)
        if draw_boxes:
            for k, bs in e["boxes"].items():
                for b in bs:
                    sd.rectangle(b, outline=ACC if b == e["player"] else colors.get(k, FG), width=6)
            sd.text((e["player"][0] - 10, e["player"][1] - 34), "player", font=font(30, FB), fill=ACC)
        paste(im, src, 80, 190, 1100)
        if draw_boxes:
            y = 260
            for k, bs in e["boxes"].items():
                d.text((1250, y), f"{len(bs)}  {k}", font=font(48, FB), fill=colors.get(k, DIM))
                y += 90
            wrap(d, (1250, y + 30), f"\"{e['scene']}\"", font(32, MONO), FG, 600)
        out.append((im, 1 if not draw_boxes else 4))
    return out, ("Meta's SAM 3.1 segments what is on screen: six people and two health bars. "
                 "The player is the box that moves after a move key. That becomes a short scene summary for the decision model."), 14


def s4():
    """녹화 영상: 촌장에게 걸어가다 좌우 키가 먹지 않아 judge 가 same_screen 을 띄우는 구간."""
    return footage(REC / "godot", RUN, [(140, 222, 5)], "Real recording · Muse Spark picks one tool call per step"), (
        "Muse Spark reads the scene summary and the screenshot, and picks one tool call per step: "
        "press a key, wait, report a bug, or write a note. Here it walks toward the village chief. "
        "Then pressing right does nothing, and the judge flags it."), 0


def s5():
    rows = re.findall(r"^\| (\w+) \| (바뀜|그대로) \|", BUG.read_text(encoding="utf-8"), re.M)
    im, d = card()
    title(d, "Judge: the screen stopped changing", "steps 16 → 18, still pressing right")
    for i, n in enumerate(("016.png", "018.png")):
        x = 80 + i * 900
        paste(im, frame(n), x, 210, 840)
        d.text((x, 860), f"step {int(n[:3])}", font=font(40, FB), fill=FG)
    d.rectangle((980, 210, 1820, 840), outline=RED, width=8)
    d.text((1180, 860), "same_screen for 22 s", font=font(40, FB), fill=RED)
    im2, d2 = card()
    title(d2, "Then it probes every key, one by one", "before/after capture for each key")
    paste(im2, frame("018.png"), 80, 210, 900)
    for i, (k, r) in enumerate(rows):
        y = 230 + i * 80
        ok = r == "바뀜"
        d2.text((1100, y), f"{k:<6}", font=font(46, MONO), fill=FG)
        d2.text((1320, y), "screen changed" if ok else "no response", font=font(46), fill=GRN if ok else RED)
    return [(im, 1), (im2, 1.2)], ("From step sixteen to eighteen the hero does not move while it keeps pressing right. "
                                   "The judge flags the stuck screen, then probes each key one by one: "
                                   "up and down still work, left and right do nothing."), 14


def s6():
    t = BUG.read_text(encoding="utf-8")
    steps = re.findall(r"^\d+\. (.+)$", t, re.M)
    im, d = card()
    title(d, "A bug report a human can reproduce", str(BUG.relative_to(ROOT)))
    d.text((80, 200), "Reproduce", font=font(40, FB), fill=ACC)
    for i, s in enumerate(steps):
        d.text((80 + (i // 10) * 420, 270 + (i % 10) * 56), f"{i + 1:>2}. {s}", font=font(32, MONO), fill=FG)
    x, y = 1000, 200
    for k, v, c in (
            ("Severity", "medium", FG),
            ("Expected", re.search(r"## 기대\n(.+)", t)[1], FG),
            ("Actual", re.search(r"## 실제\n(.+)", t)[1], FG),
            ("Evidence", "frames 016, 018  +  per-key probe table (8 keys)", FG)):
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


def s_snare():
    """같은 에이전트, UE5 게임 — VM 녹화본에 실제 클릭을 빨간 원으로."""
    return footage(REC / "snare", SNARE, [(0, 140, 8)], "Real recording · Unreal Engine 5 (Snarehaven) Win64 build in the VM · real mouse clicks"), (
        "Same agent, a different engine. Snarehaven is my Unreal Engine 5 game, packaged for Windows. "
        "No game-specific code: PlayTester reads the title screen, clicks Start, clears the tutorial, and walks into the world on its own."), 0


def s_snare_find():
    im, d = card()
    title(d, "What it found in the Unreal build", "runs/20261102-152538 step 19 · bugs/0059 from the game log · 0055 from an earlier run")
    src = frame("019.png", SNARE)
    sd = ImageDraw.Draw(src)
    for b in ((8, 8, 148, 60), (1046, 22, 1258, 61)):
        sd.rectangle(b, outline=RED, width=5)
    paste(im, src, 80, 190, 960)
    d.text((80, 750), "\"connecting to server...\" and \"server not connected\" at once", font=font(30), fill=RED)
    y = 200
    for head, body in (("Conflicting server status", "two indicators disagree in offline mode, no retry"),
                       ("8 sound packages missing from the build", "SFX_Amb_Rain/Ocean/Wind/Night/Swamp_02, SFX_Bird_07, SFX_Footstep_Grass_06, SFX_Swing_04"),
                       ("Intermittent startup crash", "Assertion failed: IsSet() — reported from the log, then PlayTester relaunches and keeps testing")):
        d.text((1100, y), head, font=font(38, FB), fill=ACC)
        y = wrap(d, (1100, y + 55), body, font(30), FG, 760) + 40
    wrap(d, (1100, y + 10), "VM note: black blobs are the virtual GPU dropping draws; Spark flagged them itself.", font(24), DIM, 760)
    return [(im, 1)], ("In the Unreal build it found two indicators that disagree: connecting, and not connected, at the same time. "
                       "Reading the game log on its own, PlayTester filed eight sound packages missing from the packaged build, "
                       "and an intermittent startup crash that it reports and survives by relaunching the game."), 14


def s8():
    summ = (RUN / "summary.md").read_text(encoding="utf-8")
    n = re.search(r"수: (\d+)", summ)[1]
    im, d = card()
    d.text((120, 120), "Godot 4  ·  Unreal Engine 5  ·  same agent", font=font(44), fill=GRN)
    m = log()[-1]["t"] / 60
    d.text((120, 220), f"{n} actions · {m:.0f} minutes · unattended", font=font(64, FB), fill=FG)
    d.text((120, 340), "SAM 3.1 sees  ·  Muse Spark decides  ·  real keys  ·  reproducible reports", font=font(40), fill=DIM)
    d.text((120, 560), "github.com/soilrist/muse-playtester", font=font(60, FB), fill=ACC)
    d.text((120, 650), "Open source  ·  Promptforge  ·  mindkiln.dev@gmail.com", font=font(40), fill=DIM)
    return [(im, 1)], f"Two engines, one agent, {n} actions with nobody at the keyboard. PlayTester is open source on GitHub.", 8


SCENES = (s1, s_play, s2, s3, s4, s5, s6, s7, s_snare, s_snare_find, s8)


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
        enc = ["-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "20", "-preset", "fast"]
        for si, scene in enumerate(SCENES, 1):
            pics, text, planned = scene()
            aiff = tmp / f"s{si}.mp3"
            sh(str(Path(sys.executable).parent / "edge-tts"), "--voice", VOICE, "--text", text, "--write-media", str(aiff))
            clip = isinstance(pics, tuple)  # (프레임 생성기, 수) — 녹화 영상
            if clip:
                planned = pics[1] / FPS
            length = max(planned, dur(aiff) + 1.5)  # 말이 끝나면 곧 다음 장면 — 빈 소리 구간을 안 만든다
            wav = tmp / f"s{si}.wav"
            sh("ffmpeg", "-y", "-i", str(aiff), "-af", f"adelay=400|400,apad", "-t", f"{length:.3f}", "-ar", "48000", "-ac", "2", str(wav))
            alist.append(f"file '{wav}'")
            seg = tmp / f"s{si}.mp4"
            if clip:  # 말이 영상보다 길면 마지막 장면을 붙잡아 둔다
                p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                      "-vf", f"tpad=stop_mode=clone:stop_duration={length:.3f},fps={FPS},format=yuv420p",
                                      "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-t", f"{length:.3f}", str(seg)],
                                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
                for im in pics[0]:
                    p.stdin.write(im.tobytes())
                p.stdin.close()
                assert p.wait() == 0, seg
            else:
                lst = []
                weight = sum(w for _, w in pics)
                for pi, (im, w) in enumerate(pics):
                    png = tmp / f"s{si}-{pi}.png"
                    im.save(png)
                    lst += [f"file '{png}'", f"duration {length * w / weight:.3f}"]
                lst.append(lst[-2])  # concat demuxer 는 마지막 그림의 duration 을 쓰려면 한 번 더 적어야 한다
                (tmp / f"s{si}.txt").write_text("\n".join(lst))
                sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / f"s{si}.txt"), *enc, "-t", f"{length:.3f}", str(seg))
            vlist.append(f"file '{seg}'")
            total += length
            print(f"scene {si} {scene.__name__}: {length:.1f}s")
        (tmp / "v.txt").write_text("\n".join(vlist))
        (tmp / "a.txt").write_text("\n".join(alist))
        sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "v.txt"), "-f", "concat", "-safe", "0", "-i", str(tmp / "a.txt"),
           "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(OUT))
        print(f"total {total:.1f}s → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
