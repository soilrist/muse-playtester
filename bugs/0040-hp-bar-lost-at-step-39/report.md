# hp_bar_lost at step 39

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
34. left 700ms
35. right 700ms
36. left 700ms
37. enter 200ms
38. left 700ms
39. hint: 'e' changes the screen when interacting — use it
40. e 200ms

## 기대
game keeps responding

## 실제
'health bar' was seen on the previous step but not now

## 근거 프레임
- frames/038.png
- frames/039.png

## 판단 근거
judge rule hp_bar_lost
