# interact_stuck at step 27

- 심각도: low
- 세션: 20261030-083029

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
10. note ux
11. enter 100ms
12. right 200ms
13. up 200ms
14. right 200ms
15. right 200ms
16. d 200ms
17. enter 200ms
18. d 200ms
19. d 300ms
20. note ux
21. a 300ms
22. enter 200ms
23. d 300ms
24. a 300ms
25. a 300ms
26. enter 200ms
27. space 200ms
28. hint: 'enter' changes the screen when interacting — use it

## 기대
an interaction key opens a dialog or inspects something

## 실제
screen unchanged after 3 interaction key presses

## 근거 프레임
- frames/017.png
- frames/027.png

## 판단 근거
judge rule interact_stuck

## 키별 확인

| 키 | 화면 | 누르기 전 | 누른 뒤 |
|---|---|---|---|
| enter | 바뀜 | frames/probe-027-enter-before.png | frames/probe-027-enter-after.png |

- 화면이 바뀐 키: enter
- 안 바뀐 키: 없음
