# same_screen at step 13

- 심각도: medium
- 세션: 20261028-224621

## 재현 순서
1. enter 100ms
2. enter 100ms
3. enter 100ms
4. enter 100ms
5. enter 100ms
6. enter 100ms
7. space 100ms
8. enter 100ms
9. enter 100ms
10. enter 100ms
11. up 600ms
12. left 800ms
13. up 700ms

## 기대
game keeps responding

## 실제
screen unchanged for 13s while move keys were pressed

## 근거 프레임
- frames/012.png
- frames/013.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 그대로 | frames/probe-013-up-before.png | frames/probe-013-up-after.png |
| down | 바뀜 | frames/probe-013-down-before.png | frames/probe-013-down-after.png |
| left | 그대로 | frames/probe-013-left-before.png | frames/probe-013-left-after.png |
| right | 그대로 | frames/probe-013-right-before.png | frames/probe-013-right-after.png |
| w | 바뀜 | frames/probe-013-w-before.png | frames/probe-013-w-after.png |
| s | 바뀜 | frames/probe-013-s-before.png | frames/probe-013-s-after.png |
| a | 바뀜 | frames/probe-013-a-before.png | frames/probe-013-a-after.png |
| d | 바뀜 | frames/probe-013-d-before.png | frames/probe-013-d-after.png |

- 화면이 바뀐 키: down, w, s, a, d
- 안 바뀐 키: up, left, right
