$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    py -m venv .venv
}

Write-Host "Installing dependencies..."
.\.venv\Scripts\python.exe -m pip install -q -U pip
.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt

$driverExe = Join-Path $PSScriptRoot "drivers\msedgedriver.exe"
if (-not (Test-Path $driverExe)) {
    Write-Host "Downloading Edge WebDriver..."
    $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if (-not (Test-Path $edge)) {
        $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
    }
    if (-not (Test-Path $edge)) {
        throw "Microsoft Edge not found. Install Edge or place msedgedriver.exe in drivers\"
    }
    $ver = (Get-Item $edge).VersionInfo.ProductVersion
    New-Item -ItemType Directory -Force -Path "drivers" | Out-Null
    $zip = Join-Path $env:TEMP "edgedriver_win64.zip"
    Invoke-WebRequest -Uri "https://msedgedriver.microsoft.com/$ver/edgedriver_win64.zip" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath "drivers" -Force
}

Write-Host "Running UI tests..."
.\.venv\Scripts\python.exe -m pytest -v tests
