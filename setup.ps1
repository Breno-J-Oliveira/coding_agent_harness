<#
VibeCoder DevKit 2.0 — wrapper PowerShell portátil.
Padrão: somente prévia. Use -Apply para modificar arquivos.
Não exige alterar ExecutionPolicy permanentemente.
#>
param(
  [ValidateSet('install','plan','audit','uninstall','doctor')][string]$Action='install',
  [ValidateSet('core','web','security','full')][string]$Profile='core',
  [ValidateRange(1,8)][int]$MaxAgents=3,
  [switch]$Apply,
  [switch]$WithSkills,
  [switch]$WithDesign,
  [switch]$WithTools,
  [switch]$WithRTKHook,
  [ValidateSet('global','project')][string]$Scope='global',
  [string]$Target=''
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
$entry=Join-Path $root 'scripts\devkit.py'
$arguments=@($entry,$Action)
if ($Action -in @('install','plan','audit','uninstall')) { $arguments+=@('--scope',$Scope) }
if ($Target) {$arguments+=@('--target',$Target)}
if ($Action -in @('install','plan')) {
  $arguments+=@('--profile',$Profile,'--max-agents',$MaxAgents)
  if ($WithSkills) {$arguments+='--with-skills'}
  if ($WithDesign) {$arguments+='--with-design'}
  if ($WithTools) {$arguments+='--with-tools'}
  if ($WithRTKHook) {$arguments+='--with-rtk-hook'}
}
if ($Apply) {$arguments+='--apply'}
if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 @arguments
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python @arguments
} else {
  Write-Error 'Python 3.11+ não encontrado. Instale e reabra o terminal.'
  exit 2
}
exit $LASTEXITCODE
