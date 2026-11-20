# Somente leitura; nenhum comando de instalação ou acesso a credenciais.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Write-Host 'VibeCoder DevKit - diagnóstico SOMENTE LEITURA'
Write-Host '-------------------------------------------------'
foreach ($cmd in @('node','npm','npx','git','python','codex','playwright-cli')) {
    $match = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($null -ne $match) { Write-Host ('OK       {0}' -f $cmd) }
    else { Write-Host ('AUSENTE  {0}' -f $cmd) }
}
$base = Join-Path $env:USERPROFILE '.codex'
$config = Join-Path $base 'config.toml'
$agents = Join-Path $base 'agents'
$skills = Join-Path (Join-Path $env:USERPROFILE '.agents') 'skills'
Write-Host ('Config TOML existe: {0}' -f (Test-Path $config))
Write-Host ('Diretório agentes: {0}' -f (Test-Path $agents))
if (Test-Path $agents) {
    $count = @(Get-ChildItem $agents -Filter '*.toml' -File -ErrorAction SilentlyContinue).Count
    Write-Host ('Arquivos de agentes: {0}' -f $count)
}
Write-Host ('Diretório skills globais: {0}' -f (Test-Path $skills))
if (Test-Path $skills) {
    $count = @(Get-ChildItem $skills -Directory -ErrorAction SilentlyContinue).Count
    Write-Host ('Diretórios de skills: {0}' -f $count)
}
Write-Host 'Nada foi instalado ou modificado. A presença de arquivos não confirma carregamento no runtime.'
