"""판단 (DESIGN §4.4). Muse Spark 툴 호출로 다음 행동 하나를 받는다."""
import json

from meta_client import call_text, function_calls

WHY = {"type": "string", "description": "One short sentence: what you see on screen and why you chose this action."}
TOOLS = [
    {"type": "function", "name": "press", "description": "Press one game key for hold_ms milliseconds.",
     "parameters": {"type": "object", "properties": {"key": {"type": "string", "description": "One of: up, down, left, right, enter, esc, space, tab, shift, or a single letter."}, "hold_ms": {"type": "integer"}, "why": WHY}, "required": ["key", "hold_ms", "why"]}},
    {"type": "function", "name": "wait", "description": "Do nothing for ms milliseconds.",
     "parameters": {"type": "object", "properties": {"ms": {"type": "integer"}, "why": WHY}, "required": ["ms", "why"]}},
    {"type": "function", "name": "report_bug", "description": "Report a bug you observed.",
     "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "severity": {"type": "string", "enum": ["low", "medium", "high"]}, "why": {"type": "string"}}, "required": ["title", "severity", "why"]}},
    {"type": "function", "name": "note", "description": "Note anything odd, uncomfortable or unclear you noticed (a dead key, a confusing screen, a missing hint, a pacing or difficulty impression).",
     "parameters": {"type": "object", "properties": {"kind": {"type": "string", "enum": ["ux", "fun", "balance"]}, "what": {"type": "string"}, "why": {"type": "string"}}, "required": ["kind", "what", "why"]}},
    {"type": "function", "name": "done", "description": "End the session.",
     "parameters": {"type": "object", "properties": {"reason": {"type": "string"}, "why": WHY}, "required": ["reason", "why"]}},
]


def decide(scene_text, recent, goal, image=None, only_note=False):
    """(tool_name, args) 하나를 반환. recent 는 최근 5수 문자열 목록. image 는 현재 화면 캡처 경로. only_note 면 note 툴만 준다(막힘 직후 소감을 반드시 받으려고)."""
    prompt = (
        "You are a game playtester. Choose exactly ONE tool call as your next action.\n"
        "Rules: (1) First read any control hints printed on the screen and use exactly those keys "
        "(menus usually take arrow keys + Enter). (2) If a dialog asks to delete, erase or overwrite "
        "(delete / overwrite / 지운다 / 삭제 / 덮어쓰기), NEVER confirm it. Any on-screen warning about erasing a save or 'press once more to proceed' means a destructive confirmation is pending: press esc to cancel it right away. "
        "(3) If an on-screen objective says to talk to, open or inspect something, walk next to it, face it, then press enter; "
        "if the screen does not change, try space, z, e, x one at a time before walking away. "
        "(4) Scene counts people (NPCs and the player together) — find the player in the screenshot yourself and judge directions from the player, not from an NPC. "
        "(5) If you see anything odd or uncomfortable (a key that does nothing, a popup that appears suddenly, unreadable text), call note with it instead of ignoring it.\n"
        f"Goal: {goal}\nScene: {scene_text}\nRecent moves: {json.dumps(recent[-5:])}"
    )
    if only_note:
        prompt += "\nThe last key did nothing here. This move you MUST call note: describe what looks odd or uncomfortable about it for a player."
    calls = function_calls(call_text(prompt, tools=[t for t in TOOLS if t["name"] == "note"] if only_note else TOOLS, image=image))
    if not calls:
        raise RuntimeError("툴 호출 없음")
    return calls[0]


if __name__ == "__main__":
    print(decide("player at center, door to the north, no enemies", [], "explore the room"))
