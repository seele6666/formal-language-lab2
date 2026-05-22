# Package experiment submission archive.
# Usage: .\scripts\package_submission.ps1 -GroupNumber "03"
param(
    [Parameter(Mandatory = $true)]
    [string]$GroupNumber,
    [string]$ClassName = "2024211301",
    [string]$LeaderName = "张恒基"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$baseName = "${GroupNumber}${ClassName}${LeaderName}"
$staging = Join-Path $root "submission_staging"
if (Test-Path $staging) {
    Remove-Item $staging -Recurse -Force
}
New-Item -ItemType Directory -Path $staging | Out-Null

$reportDocx = Join-Path $staging "${baseName}报告.docx"
$codeDir = Join-Path $staging "${baseName}代码"
$programDir = Join-Path $staging "${baseName}程序"
$videoPath = Join-Path $staging "${baseName}视频.mp4"

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
    (Join-Path $root "docs\${baseName}视频.mp4"),
    (Join-Path $root "docs\demo.mp4"),
    (Join-Path $root "docs\video.mp4")
)
$foundVideo = $videoCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($foundVideo) {
    Copy-Item $foundVideo -Destination $videoPath
} else {
    Write-Warning "Video not found. Place demo video at docs\demo.mp4 before packaging."
    New-Item -ItemType File -Path $videoPath | Out-Null
}

$zipName = "实验二${GroupNumber}${ClassName}${LeaderName}.zip"
$zipPath = Join-Path $root $zipName
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zipPath -Force
Write-Host "Created $zipPath"
