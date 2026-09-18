# Native, same-parent directory renames after validating every path against this workspace.
$ErrorActionPreference = 'Stop'
$workspacePath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$daysPath = (Resolve-Path -LiteralPath (Join-Path $workspacePath 'days')).Path
$boundary = $daysPath.TrimEnd('\') + '\'
$records = Get-Content -LiteralPath (Join-Path $workspacePath 'docs/folder_renames.json') -Raw | ConvertFrom-Json
$validated = foreach ($record in $records) {
    $source = [System.IO.Path]::GetFullPath((Join-Path $workspacePath $record.old))
    $target = [System.IO.Path]::GetFullPath((Join-Path $workspacePath $record.new))
    if (-not $source.StartsWith($boundary, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not $target.StartsWith($boundary, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Rename escapes course days directory: $source -> $target"
    }
    if ([System.IO.Path]::GetDirectoryName($source) -ne [System.IO.Path]::GetDirectoryName($target)) {
        throw "Expected same-parent rename: $source -> $target"
    }
    $alreadyMoved = -not (Test-Path -LiteralPath $source)
    if ($alreadyMoved -and -not (Test-Path -LiteralPath $target -PathType Container)) {
        throw "Neither source nor moved folder exists: $source"
    }
    if (-not $alreadyMoved -and (Test-Path -LiteralPath $target)) { throw "Destination exists: $target" }
    # OneDrive cloud placeholders also carry ReparsePoint but have no link target.
    $existingPath = if ($alreadyMoved) { $target } else { $source }
    $sourceItem = Get-Item -LiteralPath $existingPath
    $parentItem = Get-Item -LiteralPath ([System.IO.Path]::GetDirectoryName($source))
    if ($sourceItem.LinkType -or $sourceItem.Target -or $parentItem.LinkType -or $parentItem.Target) {
        throw "Refusing to rename a linked directory: $source"
    }
    [PSCustomObject]@{Source=$source; Target=$target; AlreadyMoved=$alreadyMoved}
}
foreach ($record in $validated) {
    if ($record.AlreadyMoved) { continue }
    Rename-Item -LiteralPath $record.Source -NewName ([System.IO.Path]::GetFileName($record.Target))
}
Write-Output "Renamed $($validated.Count) subject folders inside $daysPath."
