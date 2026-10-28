"""VM 실측 가능성 확인 — 게임을 띄우고 실제 키를 눌러 화면이 바뀌는지 본다. VM 안에서: C:\\pt\\python\\python.exe probe.py <출력폴더>"""
import subprocess, sys, time
from pathlib import Path

import mss
from PIL import Image, ImageChops
from pynput.keyboard import Controller, Key

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
game = subprocess.Popen([r"C:\pt\godot\godot.exe", "--path", r"C:\pt\game"])
time.sleep(15)

def shot(name):
    with mss.mss() as s:
        g = s.grab(s.monitors[1])
    img = Image.frombytes("RGB", g.size, g.rgb); img.save(out / f"{name}.png"); return img

kb = Controller()
before = shot("0-before")
for k in (Key.down, Key.down, Key.up):
    kb.press(k); time.sleep(0.15); kb.release(k); time.sleep(0.6)
after = shot("1-after")
diff = ImageChops.difference(before, after).convert("L").point(lambda v: 255 if v > 30 else 0)
print("changed_px", sum(1 for v in diff.getdata() if v), "bbox", diff.getbbox())
game.terminate()
