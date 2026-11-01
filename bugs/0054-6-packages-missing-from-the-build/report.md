# 6 packages missing from the build

- 심각도: medium
- 세션: 20261101-091606

## 재현 순서
1. Launch the game
2. Play the session runs/20261101-091606 (actions in log.jsonl)
3. Read the game log after the session

## 기대
every asset the game loads is in the packaged build

## 실제
6 occurrence(s) in the game log, 6 distinct:

```
[2026.11.01-00.18.32:339][791]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Ocean_02 (0x16A288E70D7ACF7F) - The package to load does not exist on disk or in the loader
[2026.11.01-00.18.32:340][791]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Wind_02 (0x1E82435134BFC990) - The package to load does not exist on disk or in the loader
[2026.11.01-00.18.32:340][791]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Swamp_02 (0x33F87BEBE247BBE3) - The package to load does not exist on disk or in the loader
[2026.11.01-00.18.32:341][791]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Night_02 (0xB0DD8371B7C8A9F7) - The package to load does not exist on disk or in the loader
[2026.11.01-00.18.32:341][791]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Rain_02 (0x54C5512FE3BD77DD) - The package to load does not exist on disk or in the loader
[2026.11.01-00.18.33:970][849]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Bird_07 (0x48F4AC7450CFA71B) - The package to load does not exist on disk or in the loader
```

## 근거 프레임
- frames/001.png
- frames/Snarehaven.log

## 판단 근거
game log rule missing_asset: Snarehaven.log
