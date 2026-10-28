# same_screen at step 14

- 심각도: medium
- 세션: 20261028-220602

## 재현 순서
1. enter 100ms
2. enter 100ms
3. enter 100ms
4. enter 100ms
5. enter 100ms
6. enter 100ms
7. enter 100ms
8. enter 100ms
9. space 100ms
10. enter 100ms
11. right 500ms
12. up 500ms
13. enter 100ms
14. left 500ms

## 기대
game keeps responding

## 실제
screen unchanged for 11s while move keys were pressed

## 근거 프레임
- frames/013.png
- frames/014.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-014-up-before.png | frames/probe-014-up-after.png |
| down | 바뀜 | frames/probe-014-down-before.png | frames/probe-014-down-after.png |
| left | 그대로 | frames/probe-014-left-before.png | frames/probe-014-left-after.png |
| right | 그대로 | frames/probe-014-right-before.png | frames/probe-014-right-after.png |
| w | 바뀜 | frames/probe-014-w-before.png | frames/probe-014-w-after.png |
| s | 바뀜 | frames/probe-014-s-before.png | frames/probe-014-s-after.png |
| a | 바뀜 | frames/probe-014-a-before.png | frames/probe-014-a-after.png |
| d | 바뀜 | frames/probe-014-d-before.png | frames/probe-014-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
