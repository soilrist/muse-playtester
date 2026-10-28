# same_screen at step 33

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
14. left 800ms
15. left 700ms
16. left 700ms
17. left 700ms
18. left 700ms
19. enter 200ms
20. up 700ms
21. down 700ms
22. right 200ms
23. up 700ms
24. left 700ms
25. left 700ms
26. up 700ms
27. left 700ms
28. up 700ms
29. down 700ms
30. enter 100ms
31. up 700ms
32. left 700ms
33. left 700ms

## 기대
game keeps responding

## 실제
screen unchanged for 11s while move keys were pressed

## 근거 프레임
- frames/032.png
- frames/033.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-033-up-before.png | frames/probe-033-up-after.png |
| down | 바뀜 | frames/probe-033-down-before.png | frames/probe-033-down-after.png |
| left | 그대로 | frames/probe-033-left-before.png | frames/probe-033-left-after.png |
| right | 그대로 | frames/probe-033-right-before.png | frames/probe-033-right-after.png |
| w | 바뀜 | frames/probe-033-w-before.png | frames/probe-033-w-after.png |
| s | 바뀜 | frames/probe-033-s-before.png | frames/probe-033-s-after.png |
| a | 바뀜 | frames/probe-033-a-before.png | frames/probe-033-a-after.png |
| d | 바뀜 | frames/probe-033-d-before.png | frames/probe-033-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
