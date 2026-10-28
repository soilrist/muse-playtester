"""이상 감지 (DESIGN §4.6). 규칙만 쓰고 모델은 부르지 않는다. 임계값은 DESIGN §6.4."""
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

SAME_SCREEN_SEC = 10
BLACK_MEAN = 8
PIXEL_DIFF = 24  # 픽셀 밝기 차이(0~255)가 이보다 크면 "바뀐 픽셀"
SAME_PIXELS = 50  # 바뀐 픽셀이 이 이하면 같은 화면 (작은 스프라이트 하나 이동은 수천 개 — 평균으로는 안 보임)
MOVE_KEYS = {"up", "down", "left", "right", "w", "a", "s", "d"}


@dataclass
class Step:
    """한 수의 판단 재료. keys 는 이 수에서 누른 키, scene 은 perceive.Scene (없으면 None)."""
    t: float
    image: Path
    keys: tuple = ()
    scene: object = None


@dataclass
class Finding:
    rule: str
    why: str
    frames: list = field(default_factory=list)


def mean_brightness(path):
    return ImageStat.Stat(Image.open(path).convert("L")).mean[0]


def frames_same(a, b):
    """같은 크기의 두 그림이 사실상 같은지. 크기가 다르면 다른 화면."""
    ia, ib = Image.open(a).convert("L"), Image.open(b).convert("L")
    if ia.size != ib.size:
        return False
    diff = ImageChops.difference(ia, ib).point(lambda v: 255 if v > PIXEL_DIFF else 0)
    return ImageStat.Stat(diff).sum[0] / 255 <= SAME_PIXELS


def _count(step, kind):
    """kind 박스 수. 인식이 실패했거나 scene 이 없으면 None(모름)."""
    sc = step.scene
    if sc is None or kind in sc.errors or kind not in sc.boxes:
        return None
    return len(sc.boxes[kind])


class Judge:
    def __init__(self):
        self.steps = []
        self._reported_from = None  # 이미 리포트한 같은 화면 구간의 첫 수
        self._responded = False  # 이동 키를 누른 뒤 화면이 바뀐 적이 있는가 (없으면 아직 타이틀·메뉴)

    def check(self, step):
        """새 수를 넣고 이번에 걸린 이상 목록을 돌려준다."""
        prev = self.steps[-1] if self.steps else None
        self.steps.append(step)
        if prev and set(k.lower() for k in prev.keys) & MOVE_KEYS and not frames_same(prev.image, step.image):
            self._responded = True
        found = []
        if prev and mean_brightness(step.image) <= BLACK_MEAN and mean_brightness(prev.image) <= BLACK_MEAN:
            found.append(Finding("black_screen", f"mean brightness <= {BLACK_MEAN} on 2 consecutive steps",
                                 [str(prev.image), str(step.image)]))
        found += self._same_screen(step)
        if prev:
            for rule, kind in (("hp_bar_lost", "health bar"), ("player_lost", "player character")):
                before, now = _count(prev, kind), _count(step, kind)
                if before and now == 0:
                    found.append(Finding(rule, f"'{kind}' was seen on the previous step but not now",
                                         [str(prev.image), str(step.image)]))
        return found

    def _same_screen(self, step):
        """이동 키를 눌렀는데 SAME_SCREEN_SEC 초 넘게 화면이 같으면 끼임. 구간마다 한 번만, 이동 키에 화면이 한 번도 안 반응한 세션(타이틀·메뉴)에서는 안 쏜다."""
        if not self._responded:
            return []
        run = [step]
        for s in reversed(self.steps[:-1]):
            if not frames_same(s.image, step.image):
                break
            run.append(s)
        run.reverse()
        if len(run) < 2 or run[-1].t - run[0].t < SAME_SCREEN_SEC:
            return []
        if not any(set(k.lower() for k in s.keys) & MOVE_KEYS for s in run[1:]):
            return []
        if run[0] is self._reported_from:
            return []
        self._reported_from = run[0]
        return [Finding("same_screen", f"screen unchanged for {run[-1].t - run[0].t:.0f}s while move keys were pressed",
                        [str(run[0].image), str(run[-1].image)])]


def selftest():
    root = Path(__file__).resolve().parent.parent
    from perceive import Box, Scene
    real = root / "captures" / "sample-d1-03.png"  # 저장된 실제 캡처
    other = root / "captures" / "priv-b0.png"
    moved = root / "captures" / "same-test"  # VM 실측 캡처 일부 (012/020 은 캐릭터 이동, 013/014 는 픽셀 동일)
    assert not frames_same(moved / "012.png", moved / "020.png"), "작은 스프라이트 이동도 다른 화면"
    assert frames_same(moved / "013.png", moved / "014.png"), "픽셀 동일은 같은 화면"
    with tempfile.TemporaryDirectory() as d:
        black = Path(d) / "black.png"
        Image.new("RGB", (64, 64), (0, 0, 0)).save(black)

        def rules(steps):
            j, out = Judge(), []
            for s in steps:
                out += [f.rule for f in j.check(s)]
            return out

        assert rules([Step(0, real), Step(1, other)]) == [], "다른 화면 두 장은 이상 아님"
        assert rules([Step(0, black), Step(1, black)]) == ["black_screen"], "검은 화면 2수 연속"
        assert rules([Step(0, real), Step(1, black)]) == [], "검은 화면 1수는 페이드로 본다"
        w = [Step(-2, other, ("down",)), Step(-1, real, ("down",))]
        assert rules(w + [Step(0, real, ("down",)), Step(5, real, ("down",))]) == [], "10초 미만"
        assert rules(w + [Step(0, real, ("down",)), Step(6, real, ("down",)), Step(11, real, ("down",))]) == ["same_screen"]
        assert rules(w + [Step(0, real, ("e",)), Step(11, real, ("e",))]) == [], "이동 키가 아니면 끼임 아님"
        walk = [Step(0, other, ("down",)), Step(1, real, ("down",))]  # 이동 키에 화면이 반응했다
        stuck = walk + [Step(t, real, ("down",)) for t in (7, 12, 18, 24)]
        assert rules(stuck) == ["same_screen"], "같은 구간은 리포트 1개만"
        assert rules(stuck + [Step(30, other, ("down",))] + [Step(t, real, ("down",)) for t in (36, 42, 48)]) == ["same_screen", "same_screen"], "구간이 끊긴 뒤 새 끼임은 새 리포트"
        assert rules([Step(t, real, ("down",)) for t in (0, 6, 11, 17)]) == [], "이동 키에 한 번도 반응 안 한 타이틀·메뉴는 끼임 아님"
        sc = lambda **k: Scene(real, boxes=k)
        pb = [Box(0, 0, 1, 1)]
        assert rules([Step(0, real, scene=sc(**{"player character": pb, "health bar": pb})),
                      Step(1, other, scene=sc(**{"player character": [], "health bar": []}))]) == ["hp_bar_lost", "player_lost"]
        bad = Scene(real, boxes={"player character": []}, errors={"player character": "x"})
        assert rules([Step(0, real, scene=sc(**{"player character": pb})), Step(1, other, scene=bad)]) == [], "인식 실패는 소실이 아님"
    print("judge selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        print("usage: judge.py selftest")
