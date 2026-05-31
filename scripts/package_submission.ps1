# Package experiment submission archive (v4 naming).
# Usage: .\scripts\package_submission.ps1 -GroupNumber "7"
param(
    [Parameter(Mandatory = $true)]
    [string]$GroupNumber,
    [string]$ClassName = "2024211301",
    [string]$LeaderName = "ZhangHengji"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if ($LeaderName -eq "ZhangHengji") {
    $LeaderName = [char]0x5F20 + [char]0x6052 + [char]0x57FA
}

$groupSuffix = [char]0x7EC4
$groupLabel = if ($GroupNumber -match ($groupSuffix + '$')) { $GroupNumber } else { $GroupNumber + $groupSuffix }
$baseName = "${groupLabel}+${ClassName}+${LeaderName}"
$staging = Join-Path $root "submission_staging"
if (Test-Path $staging) {
    Remove-Item $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging | Out-Null

$reportSuffix = [char]0x62A5 + [char]0x544A + [char]0x6587 + [char]0x6863
$codeSuffix = [char]0x4EE3 + [char]0x7801
$programSuffix = [char]0x7A0B + [char]0x5E8F
$videoSuffix = [char]0x89C6 + [char]0x9891

$reportDocx = Join-Path $staging ($baseName + "+" + $reportSuffix + ".docx")
$codeDir = Join-Path $staging ($baseName + "+" + $codeSuffix)
$programDir = Join-Path $staging ($baseName + "+" + $programSuffix)
$videoPath = Join-Path $staging ($baseName + "+" + $videoSuffix + ".mp4")

Write-Host "Converting report.md to docx..."
$convertScript = Join-Path $root "scripts\md_to_docx.py"
if (-not (Test-Path $convertScript)) {
    throw "Missing converter script: $convertScript"
}
py $convertScript (Join-Path $root "docs\report.md") $reportDocx

Write-Host "Copying source code..."
New-Item -ItemType Directory -Path $codeDir | Out-Null
$exclude = @(
    "__pycache__", ".pytest_cache", "build", "dist", "submission_staging",
    ".git", ".claude", "submission_package"
)
Get-ChildItem $root | Where-Object {
    $_.Name -notin $exclude -and $_.Name -notlike "*.zip"
} | ForEach-Object {
    Copy-Item $_.FullName -Destination $codeDir -Recurse -Force
}

Write-Host "Copying executable..."
New-Item -ItemType Directory -Path $programDir | Out-Null
$exe = Join-Path $root "dist\formal_lang_lab2.exe"
if (-not (Test-Path $exe)) {
    throw "Missing executable. Run: pyinstaller --onefile --name formal_lang_lab2 main.py"
}
Copy-Item $exe -Destination $programDir

$videoCandidates = @(
    (Join-Path $root "docs\demo.mp4"),
    (Join-Path $root "docs\video.mp4")
)
$foundVideo = $videoCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($foundVideo) {
    Copy-Item $foundVideo -Destination $videoPath
} else {
    throw "Video not found. Place demo video at docs\demo.mp4 before packaging."
}

$zipPrefix = [char]0x5B9E + [char]0x9A8C + [char]0x4E8C
$zipName = $zipPrefix + "+" + $baseName + ".zip"
$zipPath = Join-Path $root $zipName
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zipPath -Force
Write-Host "Created $zipPath"
