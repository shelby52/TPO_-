$ErrorActionPreference = "Stop"
$page = Join-Path $PSScriptRoot "public\index.html"
Start-Process $page
