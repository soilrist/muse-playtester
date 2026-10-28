# interact_stuck at step 38

- 심각도: low
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
34. left 700ms
35. right 700ms
36. left 700ms
37. enter 200ms
38. left 700ms
39. hint: 'e' changes the screen when interacting — use it

## 기대
an interaction key opens a dialog or inspects something

## 실제
screen unchanged after 3 interaction key presses

## 근거 프레임
- frames/019.png
- frames/038.png

## 판단 근거
judge rule interact_stuck

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| enter | 그대로 | frames/probe-038-enter-before.png | frames/probe-038-enter-after.png |
| space | 그대로 | frames/probe-038-space-before.png | frames/probe-038-space-after.png |
| z | 그대로 | frames/probe-038-z-before.png | frames/probe-038-z-after.png |
| e | 바뀜 | frames/probe-038-e-before.png | frames/probe-038-e-after.png |

- 화면이 바뀐 키: e
- 안 바뀐 키: enter, space, z
