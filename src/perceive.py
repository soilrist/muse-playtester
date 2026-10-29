"""인식 (DESIGN §4.3). SAM 3.1 에 종류마다 한 번씩 물어 Scene 을 만든다."""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from meta_client import call_sam, output_text

# SAM 은 "player character" 에 화면의 모든 인물(NPC 포함 8개)을, "npc"·"dialog box" 에 0개를 돌려줬다 → 040.png 에서 "person" 6명·"house door" 3개
PROMPTS = ["person", "enemy", "health bar", "house door", "chest", "dialog box"]
BOX_RE = re.compile(r"<\|box;([^|]*)\|>")


@dataclass
class Box:
    x1: int
    y1: int
    x2: int
    y2: int
    conf: float | None = None


@dataclass
class Scene:
    image: Path
    boxes: dict[str, list[Box]] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)

    def summary(self):
        """decide 에 넘길 한 줄 요약."""
        parts = [f"{len(v)} {k}" for k, v in self.boxes.items() if v]
        return "detected: " + (", ".join(parts) if parts else "nothing")


def parse_boxes(text):
    """SAM 출력 문자열에서 박스 목록을 뽑는다. 마스크 토큰은 쓰지 않는다."""
    boxes = []
    for body in BOX_RE.findall(text):
        f = dict(kv.split("=", 1) for kv in body.split(";") if "=" in kv)
        boxes.append(Box(int(float(f["x1"])), int(float(f["y1"])), int(float(f["x2"])), int(float(f["y2"])),
                         float(f["c"]) if "c" in f else None))
    return boxes


def perceive(png_path, prompts=PROMPTS):
    """캡처 1장을 종류별로 SAM 에 보낸다. 한 종류가 실패해도 나머지는 계속한다."""
    scene = Scene(Path(png_path))
    for p in prompts:
        try:
            scene.boxes[p] = parse_boxes(output_text(call_sam(p, png_path)))
        except Exception as e:  # 네트워크·예산 등. Spark 폴백은 D2-02 결과를 보고 정한다
            scene.boxes[p] = []
            scene.errors[p] = f"{type(e).__name__}: {e}"
    return scene


if __name__ == "__main__":
    sc = perceive(sys.argv[1])
    for k, v in sc.boxes.items():
        print(k, [(b.x1, b.y1, b.x2, b.y2, b.conf) for b in v], sc.errors.get(k, ""))
    print(sc.summary())
