# VM 실행 대리인 — Mac 이 vm\queue\<이름>.cmd 를 떨구면 이 사용자 세션(화면 있음)에서 실행하고
# 출력은 <이름>.out, 끝나면 <이름>.done. (Parallels 표준판은 prlctl exec 가 막혀 있어서 공유 폴더로 주고받는다)
$Q = "\\Mac\Home\Git Project\muse-playtester\vm\queue"
while (-not (Test-Path "\\Mac\Home")) { Start-Sleep 5 }
New-Item -ItemType Directory -Force $Q | Out-Null
while ($true) {
  Get-ChildItem $Q -Filter *.cmd | ForEach-Object {
    $base = $_.FullName -replace '\.cmd$', ''
    # 끝 줄바꿈이 남으면 cmd 가 거기서 줄을 끊어 '> .out' 리다이렉트가 사라진다
    $c = (Get-Content $_.FullName -Raw).Trim()
    Remove-Item $_.FullName
    cmd /c "(chcp 65001 >nul & $c) > `"$base.out`" 2>&1"  # 괄호: && 사슬 전체를 받는다
    "EXIT $LASTEXITCODE" | Add-Content "$base.out"
    New-Item "$base.done" -Force | Out-Null
  }
  Start-Sleep 2
}
