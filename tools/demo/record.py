"""데모용 실제 플레이 녹화 — VM 안에서 세션과 나란히 돌며 게임 창만 초당 FPS 장 JPEG 로 남긴다.
파일 이름은 epoch 밀리초 → 맥에서 runs/<시각>/frames/NNN.png 의 mtime 과 맞춰 수(step)마다 자막을 붙인다.
stop 파일이 생기면 끝난다. 창이 아직 없거나 사라졌으면 기다린다 (부팅 재시도 중에도).
    python tools/demo/record.py C:\\pt\\rec\\godot      (PT_GAME=snarehaven 이면 언리얼 창)
"""
import sys
import time
from pathlib import Path

import mss
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from capture import MAX_WIDTH, find_game_window  # noqa: E402

FPS = 5


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    stop, n = out / "stop", 0
    with mss.mss() as sct:
        while not stop.exists():
            t = time.time()
            game = find_game_window()
            if game:
                x, y, w, h = game[1]
                if w > 0 and h > 0:
                    shot = sct.grab({"left": x, "top": y, "width": w, "height": h})
                    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
                    if img.width > MAX_WIDTH:
                        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.BILINEAR)
                    img.save(out / f"{int(t * 1000)}.jpg", quality=85)
                    n += 1
            time.sleep(max(0, 1 / FPS - (time.time() - t)))
    print(f"recorded {n} frames -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
