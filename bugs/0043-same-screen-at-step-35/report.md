# same_screen at step 35

- 심각도: medium
- 세션: 20261029-013454

## 재현 순서
1. enter 100ms
2. enter 100ms
3. enter 100ms
4. enter 100ms
5. enter 100ms
6. enter 100ms
7. enter 100ms
8. space 100ms
9. enter 100ms
10. z 100ms
11. e 100ms
12. x 100ms
13. left 1000ms
14. enter 100ms
15. space 100ms
16. z 100ms
17. right 500ms
18. e 100ms
19. x 100ms
20. enter 100ms
21. space 100ms
22. enter 100ms
23. right 800ms
24. right 1000ms
25. right 1000ms
26. enter 100ms
27. space 100ms
28. z 100ms
29. right 1000ms
30. right 1000ms
31. up 1000ms
32. right 1000ms
33. up 1000ms
34. right 1000ms
35. right 1000ms

## 기대
game keeps responding

## 실제
screen unchanged for 12s while move keys were pressed

## 근거 프레임
- frames/034.png
- frames/035.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 바뀜 | frames/probe-035-up-before.png | frames/probe-035-up-after.png |
| down | 바뀜 | frames/probe-035-down-before.png | frames/probe-035-down-after.png |
| left | 그대로 | frames/probe-035-left-before.png | frames/probe-035-left-after.png |
| right | 그대로 | frames/probe-035-right-before.png | frames/probe-035-right-after.png |
| w | 바뀜 | frames/probe-035-w-before.png | frames/probe-035-w-after.png |
| s | 바뀜 | frames/probe-035-s-before.png | frames/probe-035-s-after.png |
| a | 바뀜 | frames/probe-035-a-before.png | frames/probe-035-a-after.png |
| d | 바뀜 | frames/probe-035-d-before.png | frames/probe-035-d-after.png |

- 화면이 바뀐 키: up, down, w, s, a, d
- 안 바뀐 키: left, right
