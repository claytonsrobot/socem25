param(
    [switch]$Verbose,  # Flag for verbose mode
    [switch]$Silent    # Flag for silent mode
)

# Determine verbosity
if ($Silent) {
    $SilentMode = $true
} elseif ($Verbose) {
    $SilentMode = $false
} else {
    # Default to verbose mode if neither flag is passed
    $SilentMode = $false
}

# Define directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir
$ProjectDirName = Split-Path -Leaf $ProjectDir
$MediaIconBasePath = Join-Path $ProjectDir "media\media-ico"

# Helper function to convert absolute paths to project-relative paths
function Convert-ToProjectRelativePath {
    param (
        [string]$AbsolutePath
    )
    $RelativePath = $AbsolutePath.Substring($ProjectDir.Length).TrimStart('\')
    return ".\$ProjectDirName\$RelativePath"
}

# Find all desktop.ini files
$DesktopIniFiles = Get-ChildItem $ProjectDir -Recurse -Filter "desktop.ini" -Force

if ($DesktopIniFiles.Count -eq 0) {
    if (-not $SilentMode) { Write-Host "No desktop.ini files found." }
    Exit 0
}

foreach ($File in $DesktopIniFiles) {
    $DesktopIniPath = $File.FullName
    $RelativeDesktopIniPath = Convert-ToProjectRelativePath -AbsolutePath $DesktopIniPath

    try {
        # Read content
        $FileContent = Get-Content $DesktopIniPath

        # Update paths
        $UpdatedLines = @()
        $Changed = $false
        $RelativeIconPath = ""
        foreach ($Line in $FileContent) {
            if ($Line -like "IconResource=*") {
                $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=", "")
                $NewPath = Join-Path $MediaIconBasePath $ExistingFilename
                $RelativeNewPath = Convert-ToProjectRelativePath -AbsolutePath $NewPath
                $RelativeIconPath = Convert-ToProjectRelativePath -AbsolutePath ($Line -replace "IconResource=", "")
                if ($Line -ne "IconResource=$NewPath") {
                    # Only update if the new path is different
                    $UpdatedLines += "IconResource=$NewPath"
                    $Changed = $true
                    $RelativeIconPath = $RelativeNewPath  # Update relative path reference
                } else {
                    $UpdatedLines += $Line  # Keep original if already correct
                }
            } else {
                $UpdatedLines += $Line
            }
        }

        # Write changes if any
        if ($Changed) {
            Set-Content $DesktopIniPath -Value $UpdatedLines -Force
            if (-not $SilentMode) {
                # Show changed files with relative path
                Write-Host "$RelativeDesktopIniPath -> $RelativeIconPath"
            }
        } else {
            if (-not $SilentMode) {
                # Show unchanged files with relative path
                Write-Host "$RelativeDesktopIniPath ~ $RelativeIconPath"
            }
        }
    } catch {
        if (-not $SilentMode) {
            Write-Error "Failed: $RelativeDesktopIniPath, Error: $($_.Exception.Message)"
        }
    }
}