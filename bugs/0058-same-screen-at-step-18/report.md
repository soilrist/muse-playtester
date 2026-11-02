# same_screen at step 18

- 심각도: medium
- 세션: 20261102-150749

## 재현 순서
1. enter 100ms
2. enter 200ms
3. enter 100ms
4. enter 100ms
5. enter 100ms
6. enter 100ms
7. enter 100ms
8. space 100ms
9. enter 100ms
10. note ux
11. z 100ms
12. e 100ms
13. left 300ms
14. up 500ms
15. down 300ms
16. right 300ms
17. right 300ms
18. right 300ms

## 기대
game keeps responding

## 실제
screen unchanged for 22s while move keys were pressed

## 근거 프레임
- frames/016.png
- frames/018.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-018-up-before.png | frames/probe-018-up-after.png |
| down | 바뀜 | frames/probe-018-down-before.png | frames/probe-018-down-after.png |
| left | 그대로 | frames/probe-018-left-before.png | frames/probe-018-left-after.png |
| right | 그대로 | frames/probe-018-right-before.png | frames/probe-018-right-after.png |
| w | 바뀜 | frames/probe-018-w-before.png | frames/probe-018-w-after.png |
| s | 바뀜 | frames/probe-018-s-before.png | frames/probe-018-s-after.png |
| a | 바뀜 | frames/probe-018-a-before.png | frames/probe-018-a-after.png |
| d | 바뀜 | frames/probe-018-d-before.png | frames/probe-018-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
