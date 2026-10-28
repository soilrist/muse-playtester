# same_screen at step 5

- 심각도: medium
- 세션: 20261028-202525

## 재현 순서
1. down 100ms
2. enter 100ms
3. right 200ms
4. up 300ms
5. left 300ms

## 기대
game keeps responding

## 실제
screen unchanged for 18s while move keys were pressed

## 근거 프레임
- frames/004.png
- frames/005.png

## 판단 근거
judge rule same_screen
