# YouTube 업로드 문안

- 영상: `demo/playtester-demo.mp4` (2:32, 1920×1080)
- 썸네일: `demo/thumbnail.jpg` (1280×720, 영상 1:18 장면)
- 공개 범위: 공개(Public) 또는 일부 공개(Unlisted) — 심사위원이 링크로 볼 수 있으면 된다
- 아동용: 아니요 / 카테고리: 과학기술 / 언어: 영어

## 제목

PlayTester — an AI playtester that only sees the screen (Meta SAM 3.1 + Muse Spark)

## 설명

PlayTester plays your game like a human: it watches the screen, presses real keys, and writes bug reports a human can reproduce. No game code, no engine hooks.

Every step:
1. Capture the game window
2. Meta SAM 3.1 segments what is on screen (people, health bars, the player)
3. Muse Spark picks one action
4. A real key press or mouse click (pynput)
5. A judge checks whether the game responded — if not, it probes every key and files a report

Everything in this video is a real, unattended recording in a Windows VM:
- Godot 4 game: 60 actions, 16 minutes, no human input. It found that left/right stop responding and filed a report with the exact key sequence, evidence frames and a per-key probe table.
- Unreal Engine 5 game (Snarehaven, Win64 build): same agent, real mouse clicks. It found conflicting server status on screen, and from the game log, 8 sound packages missing from the packaged build.

Chapters
0:00 Real gameplay, no human input
0:28 How it works
0:40 SAM 3.1 segments the screen
0:54 Muse Spark picks one action per step
1:11 Judge: the screen stopped changing
1:25 A bug report a human can reproduce
1:37 Playtest notes (UX feedback)
1:47 Same agent, Unreal Engine 5
2:04 What it found in the Unreal build

Code (open source): https://github.com/soilrist/muse-playtester
Built for the Meta Global AI Developer Hackathon (Indie track).
Promptforge · mindkiln.dev@gmail.com

#AI #GameDev #Playtesting #Meta #IndieDev

## 태그

AI playtester, game testing, QA automation, Meta SAM, Muse Spark, Godot, Unreal Engine 5, indie game, hackathon, bug report
