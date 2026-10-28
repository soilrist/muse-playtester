# same_screen at step 30

- 심각도: medium
- 세션: 20261028-222711

## 재현 순서
1. enter 100ms
2. enter 100ms
3. enter 100ms
4. enter 100ms
5. enter 100ms
6. enter 100ms
7. enter 100ms
8. enter 100ms
9. enter 100ms
10. space 100ms
11. right 500ms
12. up 500ms
13. left 500ms
14. up 500ms
15. up 500ms
16. down 500ms
17. up 500ms
18. enter 200ms
19. right 500ms
20. left 500ms
21. up 500ms
22. left 500ms
23. left 500ms
24. left 500ms
25. right 500ms
26. left 500ms
27. up 500ms
28. up 500ms
29. left 500ms
30. down 500ms

## 기대
game keeps responding

## 실제
screen unchanged for 23s while move keys were pressed

## 근거 프레임
- frames/028.png
- frames/030.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-030-up-before.png | frames/probe-030-up-after.png |
| down | 바뀜 | frames/probe-030-down-before.png | frames/probe-030-down-after.png |
| left | 그대로 | frames/probe-030-left-before.png | frames/probe-030-left-after.png |
| right | 그대로 | frames/probe-030-right-before.png | frames/probe-030-right-after.png |
| w | 바뀜 | frames/probe-030-w-before.png | frames/probe-030-w-after.png |
| s | 바뀜 | frames/probe-030-s-before.png | frames/probe-030-s-after.png |
| a | 바뀜 | frames/probe-030-a-before.png | frames/probe-030-a-after.png |
| d | 바뀜 | frames/probe-030-d-before.png | frames/probe-030-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
