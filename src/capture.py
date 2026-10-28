"""게임 창 캡처 — Quartz 로 창을 찾고 mss 로 그 영역을 PNG 로 저장한다 (DESIGN §4.2)."""
import sys
import time
from pathlib import Path

import mss
import Quartz
from AppKit import NSRunningApplication
from PIL import Image

OWNER = "Godot"
TITLE_HINT = "심연의 숨결"
MAX_WIDTH = 1280
FOCUS_WAIT = 0.6
ROOT = Path(__file__).resolve().parent.parent


def _layer0_windows():
    """화면에 보이는 일반(layer 0) 창을 앞에서 뒤 순서로 돌려준다."""
    opts = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    return [w for w in Quartz.CGWindowListCopyWindowInfo(opts, Quartz.kCGNullWindowID)
            if w.get("kCGWindowLayer") == 0]


def find_game_window():
    """게임 창을 (pid, (x, y, w, h)) 로 돌려준다. 없으면 None. 제목이 일치하는 창을 우선한다."""
    found = []
    for w in _layer0_windows():
        if w.get("kCGWindowOwnerName") != OWNER:
            continue
        b = w["kCGWindowBounds"]
        if b["Width"] < 200 or b["Height"] < 200:
            continue
        found.append((TITLE_HINT in (w.get("kCGWindowName") or ""), w["kCGWindowOwnerPID"],
                      (int(b["X"]), int(b["Y"]), int(b["Width"]), int(b["Height"]))))
    found.sort(key=lambda f: not f[0])
    return (found[0][1], found[0][2]) if found else None


def bring_to_front(pid):
    """pid 의 앱을 맨 앞으로 올리고 화면에 반영될 때까지 잠깐 기다린다."""
    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
    if app is not None:
        app.activateWithOptions_(1 << 1)  # NSApplicationActivateIgnoringOtherApps
    time.sleep(FOCUS_WAIT)


def frontmost_owner():
    """맨 앞 일반 창의 소유 앱 이름. 창이 없으면 None."""
    wins = [w for w in _layer0_windows() if w["kCGWindowBounds"]["Width"] >= 200]
    return wins[0].get("kCGWindowOwnerName") if wins else None


def capture(path):
    """게임 창을 path 에 PNG 로 저장하고 Path 를 돌려준다. 창이 없으면 RuntimeError."""
    game = find_game_window()
    if game is None:
        raise RuntimeError("게임 창을 찾지 못했다 (Godot 창이 떠 있는지, 화면 기록 권한이 있는지 확인)")
    pid, (x, y, w, h) = game
    bring_to_front(pid)
    front = frontmost_owner()
    if front != OWNER:
        raise RuntimeError(f"게임 창이 가려져 있다 (맨 앞 창: {front}) — 틀린 그림은 저장하지 않는다")
    x, y, w, h = find_game_window()[1]
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
