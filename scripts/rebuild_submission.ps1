# Full rebuild and v4 submission packaging.
# Usage: .\scripts\rebuild_submission.ps1 -GroupNumber "7"
param(
    [Parameter(Mandatory = $true)]
    [string]$GroupNumber,
    [string]$SourceVideo = "",
    [switch]$SkipExe
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "==> Running unit tests..."
py -m unittest discover -s tests -q

Write-Host "==> Regenerating report.docx..."
py (Join-Path $root "scripts\md_to_docx.py") (Join-Path $root "docs\report.md") (Join-Path $root "docs\report.docx")

Write-Host "==> Compiling Typst report..."
py (Join-Path $root "scripts\compile_typst.py")

Write-Host "==> Capturing terminal screenshots..."
py (Join-Path $root "scripts\capture_terminal_screenshots.py")

if (-not $SkipExe) {
    Write-Host "==> Building executable..."
    pyinstaller --noconfirm --onefile --name formal_lang_lab2 main.py | Out-Null
}

Write-Host "==> Ensuring demo video..."
py (Join-Path $root "scripts\bootstrap_demo_video.py")

$packageArgs = @{
    GroupNumber = $GroupNumber
}
if ($SourceVideo) {
    $packageArgs.SourceVideo = $SourceVideo
}

Write-Host "==> Packaging submission..."
& (Join-Path $root "scripts\package_submission.ps1") @packageArgs

Write-Host "Done."
