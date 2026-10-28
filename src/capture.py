"""게임 창 캡처 — Quartz 로 창을 찾고 mss 로 그 영역을 PNG 로 저장한다 (DESIGN §4.2)."""
import sys
import time
from pathlib import Path

import mss
import Quartz
from PIL import Image

OWNER = "Godot"
TITLE_HINT = "심연의 숨결"
MAX_WIDTH = 1280
ROOT = Path(__file__).resolve().parent.parent


def find_game_window():
    """게임 창의 (x, y, w, h) 를 돌려준다. 없으면 None. 제목이 일치하는 창을 우선한다."""
    opts = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    found = []
    for w in Quartz.CGWindowListCopyWindowInfo(opts, Quartz.kCGNullWindowID):
        if w.get("kCGWindowOwnerName") != OWNER or w.get("kCGWindowLayer") != 0:
            continue
        b = w["kCGWindowBounds"]
        if b["Width"] < 200 or b["Height"] < 200:
            continue
        found.append((TITLE_HINT in (w.get("kCGWindowName") or ""),
                      (int(b["X"]), int(b["Y"]), int(b["Width"]), int(b["Height"]))))
    found.sort(key=lambda f: not f[0])
    return found[0][1] if found else None


def capture(path):
    """게임 창을 path 에 PNG 로 저장하고 Path 를 돌려준다. 창이 없으면 RuntimeError."""
    rect = find_game_window()
    if rect is None:
        raise RuntimeError("게임 창을 찾지 못했다 (Godot 창이 떠 있는지, 화면 기록 권한이 있는지 확인)")
    x, y, w, h = rect
    with mss.mss() as sct:
        shot = sct.grab({"left": x, "top": y, "width": w, "height": h})
    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.NEAREST)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT / "captures" / f"capture-{time.strftime('%Y%m%d-%H%M%S')}.png"
    p = capture(out)
    with Image.open(p) as im:
        print(f"saved {p} {im.size[0]}x{im.size[1]}")
