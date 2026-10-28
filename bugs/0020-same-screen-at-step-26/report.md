# same_screen at step 26

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
15. enter 100ms
16. left 500ms
17. left 500ms
18. left 500ms
19. left 500ms
20. left 500ms
21. up 500ms
22. right 500ms
23. down 500ms
24. enter 200ms
25. enter 200ms
26. left 500ms

## 기대
game keeps responding

## 실제
screen unchanged for 25s while move keys were pressed

## 근거 프레임
- frames/024.png
- frames/026.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-026-up-before.png | frames/probe-026-up-after.png |
| down | 바뀜 | frames/probe-026-down-before.png | frames/probe-026-down-after.png |
| left | 그대로 | frames/probe-026-left-before.png | frames/probe-026-left-after.png |
| right | 그대로 | frames/probe-026-right-before.png | frames/probe-026-right-after.png |
| w | 바뀜 | frames/probe-026-w-before.png | frames/probe-026-w-after.png |
| s | 바뀜 | frames/probe-026-s-before.png | frames/probe-026-s-after.png |
| a | 바뀜 | frames/probe-026-a-before.png | frames/probe-026-a-after.png |
| d | 바뀜 | frames/probe-026-d-before.png | frames/probe-026-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
