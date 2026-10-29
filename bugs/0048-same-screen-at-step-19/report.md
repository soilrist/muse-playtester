# same_screen at step 19

- 심각도: medium
- 세션: 20261029-172210

## 재현 순서
1. enter 100ms
2. enter 100ms
3. enter 100ms
4. space 100ms
5. enter 100ms
6. enter 100ms
7. enter 100ms
8. enter 100ms
9. enter 100ms
10. note ux
11. space 100ms
12. right 300ms
13. up 300ms
14. right 300ms
15. enter 100ms
16. space 100ms
17. right 300ms
18. left 300ms
19. left 800ms

## 기대
game keeps responding

## 실제
screen unchanged for 13s while move keys were pressed

## 근거 프레임
- frames/018.png
- frames/019.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-019-up-before.png | frames/probe-019-up-after.png |
| down | 바뀜 | frames/probe-019-down-before.png | frames/probe-019-down-after.png |
| left | 그대로 | frames/probe-019-left-before.png | frames/probe-019-left-after.png |
| right | 그대로 | frames/probe-019-right-before.png | frames/probe-019-right-after.png |
| w | 바뀜 | frames/probe-019-w-before.png | frames/probe-019-w-after.png |
| s | 바뀜 | frames/probe-019-s-before.png | frames/probe-019-s-after.png |
| a | 바뀜 | frames/probe-019-a-before.png | frames/probe-019-a-after.png |
| d | 바뀜 | frames/probe-019-d-before.png | frames/probe-019-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
