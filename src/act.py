"""키 입력 (DESIGN §4.5). 게임 창을 앞으로 올린 뒤 pynput 으로 실제 키를 누른다. 게임 내부 함수는 부르지 않는다."""
import sys
import time

from pynput.keyboard import Controller, Key

from capture import OWNER, Interrupted, bring_to_front, find_game_window, frontmost_owner

# decide 가 주는 키 이름 → pynput 특수키. 한 글자 키는 그대로 누른다.
SPECIAL_KEYS = {
    "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right,
    "enter": Key.enter, "return": Key.enter, "space": Key.space,
    "esc": Key.esc, "escape": Key.esc, "tab": Key.tab, "shift": Key.shift,
}
MAX_HOLD_MS = 3000
FOCUS_TRIES = 3  # 활성화 요청이 한 번에 안 먹는 일이 있다

_keyboard = Controller()


def resolve_key(name):
    """키 이름을 pynput 키로 바꾼다. 모르는 이름이면 ValueError."""
    lowered = name.strip().lower()
    if lowered in SPECIAL_KEYS:
        return SPECIAL_KEYS[lowered]
    if len(lowered) == 1:
        return lowered
    raise ValueError(f"모르는 키 이름: {name!r}")


def focus_game():
    """게임 창을 맨 앞으로 올린다. FOCUS_TRIES 번 해도 못 올리면 RuntimeError (엉뚱한 앱에 키가 가지 않게)."""
    front = None
    for _ in range(FOCUS_TRIES):
        game = find_game_window()
        if game is None:
            raise RuntimeError("게임 창을 찾지 못했다")
        bring_to_front(game[0])
        front = frontmost_owner()
        if front == OWNER:
            return
    raise RuntimeError(f"게임 창이 가려져 있다 (맨 앞 창: {front}) — 키를 누르지 않는다")


def press(key_name, hold_ms, raise_to_front=False):
    """key_name 을 hold_ms(상한 MAX_HOLD_MS) 동안 누른다. 키 전·후에 게임이 맨 앞이 아니면 Interrupted (창을 다시 빼앗지 않는다)."""
    key = resolve_key(key_name)
    if raise_to_front:
        focus_game()
    elif frontmost_owner() != OWNER:
        raise Interrupted("키를 누르기 전에 다른 앱이 앞으로 왔다")
    _keyboard.press(key)
    time.sleep(min(max(hold_ms, 30), MAX_HOLD_MS) / 1000)
    _keyboard.release(key)
    if frontmost_owner() != OWNER:
        raise Interrupted("키를 누르는 사이 다른 앱이 앞으로 왔다")


def wait(ms):
    """입력 없이 ms 만큼 기다린다."""
    time.sleep(max(ms, 0) / 1000)


if __name__ == "__main__":
    press(sys.argv[1] if len(sys.argv) > 1 else "down", int(sys.argv[2]) if len(sys.argv) > 2 else 120, raise_to_front=True)
    print("pressed")
