# Windows VM 1회 준비 — Python·Godot·게임 복사본·실행 대리인(agent). Mac 홈이 \\Mac\Home 으로 공유돼 있어야 한다.
# VM 안 PowerShell 에서: powershell -ExecutionPolicy Bypass -File "\\Mac\Home\Git Project\muse-playtester\tools\vm\bootstrap.ps1"
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Repo = "\\Mac\Home\Git Project\muse-playtester"
$Root = "C:\pt"
New-Item -ItemType Directory -Force $Root, "$Repo\logs" | Out-Null
Start-Transcript "$Repo\logs\vm-bootstrap.log" -Force

if (-not (Test-Path "$Root\python\python.exe")) {
  # 설치 파일(.exe)은 /quiet 에서 소리 없이 실패한다 — NuGet 패키지(zip, pip 포함)를 푼다
  Invoke-WebRequest https://api.nuget.org/v3-flatcontainer/pythonarm64/3.12.10/pythonarm64.3.12.10.nupkg -OutFile "$Root\py.zip"
  Expand-Archive "$Root\py.zip" "$Root\pyn" -Force
  Move-Item "$Root\pyn\tools" "$Root\python"
}
& "$Root\python\python.exe" -m pip install -q mss pynput requests pillow

if (-not (Test-Path "$Root\godot\godot.exe")) {
  Invoke-WebRequest https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_windows_arm64.exe.zip -OutFile "$Root\godot.zip"
  Expand-Archive "$Root\godot.zip" "$Root\godot" -Force
  Get-ChildItem "$Root\godot" -Filter "*_console.exe" | Remove-Item
  Get-ChildItem "$Root\godot" -Filter "Godot*.exe" | Rename-Item -NewName godot.exe
}

# 게임은 읽기 전용 복사본으로만 쓴다(원본 snapshot 은 건드리지 않음)
robocopy "\\Mac\Home\Git Project\zerostudyrpg-snapshot" "$Root\game" /MIR /XD .git /NFL /NDL /NJH /NJS | Out-Null
& "$Root\godot\godot.exe" --headless --path "$Root\game" --import 2>&1 | Select-Object -Last 3

Copy-Item "$Repo\tools\vm\agent.ps1" "$Root\agent.ps1" -Force
$startup = [Environment]::GetFolderPath("Startup")
"@start """" /min powershell -ExecutionPolicy Bypass -File $Root\agent.ps1" | Set-Content "$startup\pt-agent.cmd" -Encoding ascii
Stop-Transcript
Start-Process powershell -WindowStyle Minimized -ArgumentList "-ExecutionPolicy","Bypass","-File","$Root\agent.ps1"
"BOOTSTRAP OK" | Set-Content "$Repo\logs\vm-bootstrap.ok"
