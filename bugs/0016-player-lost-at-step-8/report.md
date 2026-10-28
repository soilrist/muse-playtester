# player_lost at step 8

- 심각도: medium
- 세션: 20261028-204216

## 재현 순서
1. down 100ms
2. enter 100ms
3. right 500ms
4. esc 100ms
5. up 500ms
6. esc 100ms
7. right 500ms
8. esc 100ms

## 기대
game keeps responding

## 실제
'player character' was seen on the previous step but not now

## 근거 프레임
- frames/007.png
- frames/008.png

## 판단 근거
judge rule player_lost
