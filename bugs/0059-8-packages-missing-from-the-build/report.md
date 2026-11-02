# 8 packages missing from the build

- 심각도: medium
- 세션: 20261102-152538

## 재현 순서
1. Launch the game
2. Play the session runs/20261102-152538 (actions in log.jsonl)
3. Read the game log after the session

## 기대
every asset the game loads is in the packaged build

## 실제
8 occurrence(s) in the game log, 8 distinct:

```
[2026.11.02-06.27.15:570][ 40]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Ocean_02 (0x16A288E70D7ACF7F) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.15:571][ 40]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Wind_02 (0x1E82435134BFC990) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.15:572][ 40]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Swamp_02 (0x33F87BEBE247BBE3) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.15:573][ 40]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Night_02 (0xB0DD8371B7C8A9F7) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.15:574][ 40]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Amb_Rain_02 (0x54C5512FE3BD77DD) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.17:218][ 90]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Bird_07 (0x48F4AC7450CFA71B) - The package to load does not exist on disk or in the loader
[2026.11.02-06.27.21:909][294]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Swing_04 (0xEEF1EB3F02EFC59E) - The package to load does not exist on disk or in the loader
[2026.11.02-06.28.57:802][553]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/Game/Audio/SFX/SFX_Footstep_Grass_06 (0xFAD277DDBA0E68E7) - The package to load does not exist on disk or in the loader
```

## 근거 프레임
- frames/001.png
- frames/Snarehaven.log

## 판단 근거
game log rule missing_asset: Snarehaven.log
