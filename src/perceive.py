"""인식 (DESIGN §4.3). SAM 3.1 에 종류마다 한 번씩 물어 Scene 을 만든다."""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from meta_client import call_sam, output_text

# SAM 은 "player character" 에 화면의 모든 인물(NPC 포함 8개)을, "npc"·"dialog box" 에 0개를 돌려줬다 → 040.png 에서 "person" 6명·"house door" 3개
PROMPTS = ["person", "enemy", "health bar", "house door", "chest", "dialog box"]
MOVE_FRAC = 0.25  # 박스 중심이 자기 키의 이 비율보다 더 옮겨졌으면 "움직였다"
BOX_RE = re.compile(r"<\|box;([^|]*)\|>")


@dataclass
class Box:
    x1: int
    y1: int
    x2: int
    y2: int
    conf: float | None = None


    def center(self):
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2


@dataclass
class Scene:
    image: Path
    boxes: dict[str, list[Box]] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)
    player: Box | None = None  # track() 가 고른 person 박스 하나

    def summary(self):
        """decide 에 넘길 한 줄 요약. 플레이어를 알면 다른 박스를 플레이어 기준 방향·거리(px)로 적는다 — Spark 가 목표 쪽으로 걷게."""
        parts = [f"{len(v)} {k}" for k, v in self.boxes.items() if v]
        text = "detected: " + (", ".join(parts) if parts else "nothing")
        if self.player:
            px, py = self.player.center()
            text += f"; player (SAM-tracked) at x={px:.0f},y={py:.0f}"
            others = [b for b in self.boxes.get("person", []) if b is not self.player]
            rel = sorted(((bx - px, by - py) for bx, by in (b.center() for b in others)), key=lambda d: abs(d[0]) + abs(d[1]))
            if rel:
                text += "; other people from player: " + ", ".join(_direction(dx, dy) for dx, dy in rel[:5])
        return text


def _direction(dx, dy):
    h = f"{abs(dx):.0f}px {'right' if dx > 0 else 'left'}" if abs(dx) >= 8 else ""
    v = f"{abs(dy):.0f}px {'down' if dy > 0 else 'up'}" if abs(dy) >= 8 else ""
    return " ".join(x for x in (h, v) if x) or "same spot"


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


def track(prev, scene, moved):
    """scene.player 를 정한다. 이동 키(moved=True)를 누른 뒤 혼자 움직인 person 박스가 플레이어다(카메라 고정 탑다운 — NPC 는 제자리).
    못 정하면 지난 플레이어와 가장 가까운 박스를 잇는다."""
    people = scene.boxes.get("person") or []
    old = (prev.boxes.get("person") or []) if prev else []
    if not people or not old:
        return None

    def gap(b, others):
        bx, by = b.center()
        return min(abs(bx - ox) + abs(by - oy) for ox, oy in (o.center() for o in others))

    went = [b for b in people if gap(b, old) > (b.y2 - b.y1) * MOVE_FRAC]
    if moved and len(went) == 1:
        scene.player = went[0]
    elif prev.player:
        near = min(people, key=lambda b: gap(b, [prev.player]))
        if gap(near, [prev.player]) <= (near.y2 - near.y1) * 2:  # 너무 멀면 놓쳤다고 본다
            scene.player = near
    return scene.player


if __name__ == "__main__":
    sc = perceive(sys.argv[1])
    for k, v in sc.boxes.items():
        print(k, [(b.x1, b.y1, b.x2, b.y2, b.conf) for b in v], sc.errors.get(k, ""))
    print(sc.summary())
