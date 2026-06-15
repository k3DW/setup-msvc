# Copyright 2026 Braden Ganetsky
# Distributed under the Boost Software License, Version 1.0.
# https://www.boost.org/LICENSE_1_0.txt

param(
  [Parameter(Mandatory=$true)]
  [string]$inputVersion,

  [Parameter(Mandatory=$true)]
  [string]$installPath
)

mkdir $installPath -Force
$installPath = Resolve-Path $installPath

Invoke-Webrequest `
  -Uri "https://raw.githubusercontent.com/k3DW/setup-msvc/3d35adb1d581fe54cf455339db2d5b0d38ecff1e/get_install_args.py" `
  -OutFile .\get_install_args.py
try {
  $scriptOutput = python .\get_install_args.py $inputVersion 2>&1
} finally {
  Remove-Item .\get_install_args.py
}

if ($LASTEXITCODE -eq 0) {
  $vsVersion = $scriptOutput[0]
  $bootstrapper = $scriptOutput[1]
  $componentID = $scriptOutput[2]
  Write-Host "Installing Visual Studio $vsVersion at $installPath"
} else {
  Write-Error "get_install_args.py failed with exit code: $LASTEXITCODE"
  Write-Error $scriptOutput
  exit $LASTEXITCODE
}

Invoke-Webrequest -Uri $bootstrapper -OutFile vs_buildtools.exe

Start-Process `
  -FilePath ".\vs_buildtools.exe" `
  -ArgumentList @(
    '--quiet', '--norestart',
    '--installPath', $installPath,
    '--add', $componentID,
    '--add', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
    '--includeRecommended',
    '--noUpdateInstaller'
  ) `
  -NoNewWindow `
  -Wait

Remove-Item .\vs_buildtools.exe
