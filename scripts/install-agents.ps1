<#
Instala perfis do kit em ~/.codex/agents com backup por arquivo.
Padrão: simulação. -Apply: copia apenas arquivos inexistentes.
-Replace: permite substituir com backup (exige -Apply); use com cautela.
-SourceDirectory: permite selecionar profiles/generated-agents.
#>
param(
  [switch]$Apply,
  [switch]$Replace,
  [string]$SourceDirectory = ''
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($Replace -and -not $Apply) { throw '-Replace exige -Apply.' }
$root = Split-Path -Parent $PSScriptRoot
$source = if ($SourceDirectory) { (Resolve-Path $SourceDirectory).Path } else { Join-Path $root 'agents' }
$homeCodex = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$target = Join-Path $homeCodex 'agents'
if (-not (Test-Path $source)) { throw "Fonte ausente: $source" }
$inputs = @(Get-ChildItem $source -Filter '*.toml' -File | Sort-Object Name)
if ($inputs.Count -eq 0) { throw 'Nenhum arquivo TOML encontrado.' }
Write-Host "Fonte: $source"
Write-Host "Destino: $target"
if (-not $Apply) { Write-Host 'SIMULAÇÃO — nenhum arquivo será alterado.' }
if ($Apply) { New-Item -ItemType Directory -Force -Path $target | Out-Null }
$backupDir = Join-Path (Join-Path $homeCodex 'backups') ('agent-profiles-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$added=0; $replaced=0; $preserved=0
foreach ($item in $inputs) {
  $dest=Join-Path $target $item.Name
  if (-not (Test-Path $dest)) {
    if ($Apply) { Copy-Item -LiteralPath $item.FullName -Destination $dest -ErrorAction Stop }
    Write-Host "NOVO: $($item.Name)"; $added++
  } elseif (-not $Replace) {
    Write-Host "PRESERVADO: $($item.Name)"; $preserved++
  } else {
    if ($Apply) {
      New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
      Copy-Item -LiteralPath $dest -Destination (Join-Path $backupDir $item.Name) -ErrorAction Stop
      Copy-Item -LiteralPath $item.FullName -Destination $dest -Force -ErrorAction Stop
    }
    Write-Host "SUBSTITUÍDO COM BACKUP: $($item.Name)"; $replaced++
  }
}
Write-Host "Resumo: novos=$added, substituidos=$replaced, preservados=$preserved"
if ($replaced -gt 0) { Write-Host "Backup: $backupDir" }
Write-Host 'Verifique os modelos no provedor, reinicie Codex e valide a descoberta em sessão real.'
