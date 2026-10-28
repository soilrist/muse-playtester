# same_screen at step 51

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
36. right 1000ms
37. right 1000ms
38. right 1000ms
39. right 1000ms
40. right 1000ms
41. right 1000ms
42. right 1000ms
43. right 1000ms
44. right 1000ms
45. up 1000ms
46. enter 100ms
47. space 100ms
48. left 1000ms
49. z 100ms
50. right 1000ms
51. right 1500ms

## 기대
game keeps responding

## 실제
screen unchanged for 19s while move keys were pressed

## 근거 프레임
- frames/049.png
- frames/051.png

## 판단 근거
judge rule same_screen

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| up | 그대로 | frames/probe-051-up-before.png | frames/probe-051-up-after.png |
| down | 바뀜 | frames/probe-051-down-before.png | frames/probe-051-down-after.png |
| left | 그대로 | frames/probe-051-left-before.png | frames/probe-051-left-after.png |
| right | 그대로 | frames/probe-051-right-before.png | frames/probe-051-right-after.png |
| w | 바뀜 | frames/probe-051-w-before.png | frames/probe-051-w-after.png |
| s | 바뀜 | frames/probe-051-s-before.png | frames/probe-051-s-after.png |
| a | 바뀜 | frames/probe-051-a-before.png | frames/probe-051-a-after.png |
| d | 바뀜 | frames/probe-051-d-before.png | frames/probe-051-d-after.png |

- 화면이 바뀐 키: down, w, s, a, d
- 안 바뀐 키: up, left, right
