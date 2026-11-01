# 7 packages missing from the build

- 심각도: medium
- 세션: 20261101-085034

## 재현 순서
1. Launch the game
2. Play the session runs/20261101-085034 (actions in log.jsonl)
3. Read the game log after the session

## 기대
every asset the game loads is in the packaged build

## 실제
7 occurrence(s) in the game log, 7 distinct:

```
[2026.10.31-23.52.10:080][863]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Ocean_02 (0x16A288E70D7ACF7F) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.10:080][863]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Wind_02 (0x1E82435134BFC990) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.10:081][863]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Swamp_02 (0x33F87BEBE247BBE3) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.10:081][863]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Night_02 (0xB0DD8371B7C8A9F7) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.10:082][863]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Rain_02 (0x54C5512FE3BD77DD) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.11:724][918]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Bird_07 (0x48F4AC7450CFA71B) - The package to load does not exist on disk or in the loader
[2026.10.31-23.52.20:552][309]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Swing_04 (0xEEF1EB3F02EFC59E) - The package to load does not exist on disk or in the loader
```

## 근거 프레임
- frames/001.png
- frames/Snarehaven.log

## 판단 근거
game log rule missing_asset: Snarehaven.log
