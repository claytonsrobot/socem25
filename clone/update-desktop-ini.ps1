# Define the repository path and desktop.ini file
Param(
    [string]$RepoPath
)

$DesktopIniFile = Join-Path -Path $RepoPath -ChildPath "desktop.ini"

# Check if desktop.ini exists
if (Test-Path $DesktopIniFile) {
    $UpdatedLines = @()

    # Read and process desktop.ini
    Get-Content $DesktopIniFile | ForEach-Object {
        if ($_ -like "IconResource=*") {
            $RelativePath = $_ -replace "IconResource=", ""
            $AbsolutePath = Join-Path -Path $RepoPath -ChildPath $RelativePath
            $UpdatedLines += "IconResource=$AbsolutePath"
        } else {
            $UpdatedLines += $_
        }
    }

    # Write updated paths back to desktop.ini
    $UpdatedLines | Set-Content -Path $DesktopIniFile
    Write-Output "desktop.ini updated successfully."
} else {
    Write-Output "desktop.ini file not found at $DesktopIniFile"
}