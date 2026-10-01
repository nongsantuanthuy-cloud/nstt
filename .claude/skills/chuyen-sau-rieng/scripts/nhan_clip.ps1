param(
  [Parameter(Mandatory = $true)][string]$So,          # vd S06
  [string]$Ma = "NSTT-20261001-B",                     # mã video
  [int]$Timeout = 60
)
# Chờ file mp4 mới nhất trong Downloads (trong 3 phút gần đây, chưa từng nhận) rồi chép thành kich_ban\<Ma>\clip_veo\<So>.mp4
# Chạy từ thư mục gốc repo. Bản cũ (nếu có) được giữ ở cho_duyet\<So>_cu.mp4.
$dl = "$env:USERPROFILE\Downloads"
$seenFile = "$env:TEMP\nstt_da_nhan.txt"
$seen = @(); if (Test-Path $seenFile) { $seen = Get-Content $seenFile }
$dich = "kich_ban\$Ma\clip_veo\$So.mp4"
New-Item -ItemType Directory -Force "kich_ban\$Ma\clip_veo", "kich_ban\$Ma\cho_duyet" | Out-Null
for ($i = 0; $i -lt $Timeout; $i++) {
  $f = Get-ChildItem $dl -Filter *.mp4 | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-3) -and $seen -notcontains $_.Name } |
       Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($f -and -not (Test-Path "$($f.FullName).crdownload")) {
    Start-Sleep 1
    if (Test-Path $dich) { Copy-Item $dich "kich_ban\$Ma\cho_duyet\${So}_cu.mp4" -Force }
    Copy-Item $f.FullName $dich -Force
    Add-Content $seenFile $f.Name
    "$So <- $($f.Name) ($([math]::Round($f.Length/1MB,1)) MB)"; exit 0
  }
  Start-Sleep 1
}
"${So}: KHONG THAY FILE TAI VE (kiem tra Chrome tat 'Hoi noi luu truoc khi tai')"; exit 1
