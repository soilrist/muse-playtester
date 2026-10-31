"""게임 창 캡처 — Quartz 로 창을 찾고 mss 로 그 영역을 PNG 로 저장한다 (DESIGN §4.2)."""
import os
import sys
import time
from pathlib import Path

import mss
from PIL import Image

WIN = sys.platform == "win32"
if WIN:  # Windows VM 안에서 돌 때 — 사람 화면에 안 보이게 (INBOX 2026-10-28 21:08)
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # 창 사각형과 mss 가 같은 물리 픽셀을 쓰게
else:
    import Quartz
    from AppKit import NSRunningApplication

SNARE = os.environ.get("PT_GAME") == "snarehaven"  # 두 번째 대상: 언리얼 모바일 게임 Snarehaven 의 Win64 패키지 빌드
OWNER = "Snarehaven" if SNARE else "Godot"
TITLE_HINT = "Snarehaven" if SNARE else "심연의 숨결"
MAX_WIDTH = 1280
FOCUS_WAIT = 0.6
ROOT = Path(__file__).resolve().parent.parent


class Interrupted(RuntimeError):
    """사람이 맥을 쓰러 돌아와 다른 앱이 게임 창 앞으로 왔다. 창을 다시 빼앗지 않고 세션을 끝낸다."""


def _win_title(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, buf, 256)
    return buf.value


def _win_game_hwnd():
    """제목에 TITLE_HINT 가 든 보이는 최상위 창의 핸들. 없으면 None."""
    hits = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def each(hwnd, _):
        if user32.IsWindowVisible(hwnd) and TITLE_HINT in _win_title(hwnd):
            hits.append(hwnd)
        return True
    user32.EnumWindows(each, 0)
    return hits[0] if hits else None


def _win_client_rect(hwnd):
    """창 안쪽(제목줄·테두리 제외) 사각형을 화면 좌표 (x, y, w, h) 로."""
    r = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(r))
    pt = wintypes.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(pt))
    return (pt.x, pt.y, r.right - r.left, r.bottom - r.top)


def _layer0_windows():
    """화면에 보이는 일반(layer 0) 창을 앞에서 뒤 순서로 돌려준다."""
    opts = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    return [w for w in Quartz.CGWindowListCopyWindowInfo(opts, Quartz.kCGNullWindowID)
            if w.get("kCGWindowLayer") == 0]


def find_game_window():
    """게임 창을 (pid, (x, y, w, h)) 로 돌려준다. 없으면 None. 제목이 일치하는 창을 우선한다."""
    if WIN:
        hwnd = _win_game_hwnd()
        return (hwnd, _win_client_rect(hwnd)) if hwnd else None
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
    if WIN:
        user32.keybd_event(0x12, 0, 0, 0)  # ALT 를 한 번 눌러야 SetForegroundWindow 가 막히지 않는다
        user32.keybd_event(0x12, 0, 2, 0)
        user32.ShowWindow(pid, 9)  # SW_RESTORE
        user32.SetForegroundWindow(pid)
        time.sleep(FOCUS_WAIT)
        return
    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
    if app is not None:
        app.activateWithOptions_(1 << 1)  # NSApplicationActivateIgnoringOtherApps
    time.sleep(FOCUS_WAIT)


def frontmost_owner():
    """맨 앞 일반 창의 소유 앱 이름. 창이 없으면 None."""
    if WIN:
        hwnd = user32.GetForegroundWindow()
        return OWNER if hwnd and hwnd == _win_game_hwnd() else (_win_title(hwnd) or None)
    wins = [w for w in _layer0_windows() if w["kCGWindowBounds"]["Width"] >= 200]
    return wins[0].get("kCGWindowOwnerName") if wins else None


def human_idle_seconds():
    """사람이 키보드·마우스를 만진 지 몇 초 지났나 (ioreg HIDIdleTime, ns). 읽지 못하면 None."""
    if WIN:
        return None  # VM 안에는 사람이 없다 — 유휴 확인을 건너뛴다
    import re
    import subprocess
    out = subprocess.run(["ioreg", "-c", "IOHIDSystem"], capture_output=True, text=True).stdout
    m = re.search(r'"HIDIdleTime" = (\d+)', out)
    return int(m.group(1)) / 1e9 if m else None


def capture(path, raise_to_front=False):
    """게임 창을 path 에 PNG 로 저장하고 Path 를 돌려준다. 창이 없으면 RuntimeError, 다른 앱이 앞이면 Interrupted (raise_to_front 면 대신 올린다)."""
    game = find_game_window()
    if game is None:
        raise RuntimeError("게임 창을 찾지 못했다 (Godot 창이 떠 있는지, 화면 기록 권한이 있는지 확인)")
    pid, (x, y, w, h) = game
    if raise_to_front:
        bring_to_front(pid)
    front = frontmost_owner()
    if front != OWNER:
        raise Interrupted(f"게임 창이 가려져 있다 (맨 앞 창: {front}) — 틀린 그림은 저장하지 않는다")
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
    p = capture(out, raise_to_front=True)
    with Image.open(p) as im:
        print(f"saved {p} {im.size[0]}x{im.size[1]}")
