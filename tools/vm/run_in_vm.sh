#!/bin/bash
# Windows VM 안에서 실측을 돌린다 (사람 화면에 안 보임). 사용: tools/vm/run_in_vm.sh [모듈 인자…]
# VM 의 agent.ps1 이 vm/queue/run.cmd 를 집어 실행하고 run.out(끝에 EXIT n)·run.done 을 남긴다.
# 주의: src/ 는 패키지가 아니라 `src\run.py` 로 부른다 (`-m src.run` 은 `from capture import` 가 깨진다). -u 필수.
cd "$(dirname "$0")/../.." || exit 1
Q=vm/queue
TIMEOUT=${PT_VM_TIMEOUT:-900}
mkdir -p "$Q" || exit 1
rm -f "$Q/run.out" "$Q/run.done"
# PT_* 환경변수는 VM 으로 안 넘어가니 cmd 의 set 으로 실어 보낸다
SETS=""; for v in $(env | grep -o '^PT_[A-Z_]*'); do SETS="$SETS set $v=${!v}&&"; done
printf '%s\r\n' "$SETS pushd \"\\\\Mac\\Home\\Git Project\\muse-playtester\" && C:\\pt\\python\\python.exe -u src\\run.py $*" > "$Q/run.tmp" || exit 1
mv "$Q/run.tmp" "$Q/run.cmd" || exit 1
waited=0
while [ ! -f "$Q/run.done" ]; do
  sleep 3; waited=$((waited + 3))
  if [ "$waited" -ge "$TIMEOUT" ]; then echo "VM 실행 시간 초과 (${TIMEOUT}초)"; tail -n 20 "$Q/run.out" 2>/dev/null; exit 2; fi
done
tail -n 30 "$Q/run.out"
tr -d '\r' < "$Q/run.out" | grep -q '^EXIT 0$'  # Windows 줄끝(\r\n)
