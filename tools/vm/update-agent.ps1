# 돌고 있는 agent 를 새 agent.ps1 로 바꾼다 — 큐(.cmd)로 보낸다: powershell -ExecutionPolicy Bypass -File "\\Mac\Home\Git Project\muse-playtester\tools\vm\update-agent.ps1"
# 프로세스 사슬: 옛 agent(powershell) → cmd /c → 이 스크립트. 할아버지(옛 agent)를 끄고 새 것을 띄운다.
Copy-Item "\\Mac\Home\Git Project\muse-playtester\tools\vm\agent.ps1" C:\pt\agent.ps1 -Force
$cmd = Get-CimInstance Win32_Process -Filter "ProcessId=$((Get-CimInstance Win32_Process -Filter "ProcessId=$PID").ParentProcessId)"
Start-Process powershell -WindowStyle Minimized -ArgumentList "-ExecutionPolicy","Bypass","-File","C:\pt\agent.ps1"
Stop-Process -Id $cmd.ParentProcessId -Force
