# Crash: Assertion failed: IsSet()

- 심각도: high
- 세션: 20261101-091606

## 재현 순서
1. Launch the game
2. Play the session runs/20261101-091606 (actions in log.jsonl)
3. Read the game log after the session

## 기대
the game keeps running

## 실제
1 occurrence(s) in the game log, 1 distinct:

```
[2026.11.01-00.16.07:425][  0]LogWindows: Error: Assertion failed: IsSet() [File:D:\build\++UE5\Sync\Engine\Source\Runtime\Core\Public\Misc\Optional.h] [Line: 372]
```

## 근거 프레임
- frames/001.png
- frames/Snarehaven-backup-2026.11.01-00.16.07.log

## 판단 근거
game log rule crash: Snarehaven-backup-2026.11.01-00.16.07.log
