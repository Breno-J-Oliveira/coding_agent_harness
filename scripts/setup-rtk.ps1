<#
Configura RTK nativo para Codex. Padrão: simula e inspeciona. -Apply: faz backup + init.
-Install: usa winget, necessita -Apply. Sempre revise alterações de hooks.
Não muda config.toml nem provedores de modelos.
#>
param([switch]$Apply,[switch]$Install)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($Install -and -not $Apply) { throw '-Install exige -Apply.' }
$homeCodex=if ($env:CODEX_HOME) {$env:CODEX_HOME} else {Join-Path $env:USERPROFILE '.codex'}
$rtk=Get-Command rtk -ErrorAction SilentlyContinue
if (-not $rtk -and -not $Install) {
  Write-Host 'RTK ausente. Instale manualmente com: winget install rtk-ai.rtk'
  if ($Apply) { throw 'Instale RTK antes de aplicar.' }
  exit 0
}
if ($Install -and -not $rtk) {
  Write-Host 'Instalacao por winget solicitada explicitamente.'
  & winget install --id rtk-ai.rtk --exact
  if ($LASTEXITCODE -ne 0) { throw "winget falhou: $LASTEXITCODE" }
  $rtk=Get-Command rtk -ErrorAction SilentlyContinue
  if (-not $rtk) { throw 'Reabra o terminal para atualizar PATH e repita sem -Install.' }
}
& rtk --version
& rtk gain
Write-Host 'Prévia oficial das alterações propostas pelo RTK:'
& rtk init -g --codex --dry-run
if ($LASTEXITCODE -ne 0) { throw 'RTK dry-run falhou; nenhuma alteração aplicada.' }
if (-not $Apply) { Write-Host 'SIMULAÇÃO concluída. Execute com -Apply após conferir a prévia.'; exit 0 }
$backup=Join-Path (Join-Path $homeCodex 'backups') ('rtk-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Force -Path $backup | Out-Null
foreach ($name in @('AGENTS.md','RTK.md','hooks.json')) {
  $path=Join-Path $homeCodex $name
  if (Test-Path $path) { Copy-Item -LiteralPath $path -Destination (Join-Path $backup $name) -ErrorAction Stop }
}
Write-Host "Backup criado: $backup"
& rtk init -g --codex
if ($LASTEXITCODE -ne 0) { throw 'RTK init falhou; backup preservado, revise hooks.' }
Write-Host 'RTK instalado: reinicie Codex, verifique /hooks e use rtk gain. Não remove hooks de terceiros.'
