param(
    [switch]$Verbose,  # Flag for verbose mode
    [switch]$Silent    # Flag for silent mode
)

# Determine verbosity
$SilentMode = $Silent
$VerboseMode = $Verbose -and -not $Silent

# Define directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir
$ProjectDirName = Split-Path -Leaf $ProjectDir  # Extract project directory name

# Function to convert absolute paths to project-relative paths
function Convert-ToRelativePath {
    param (
        [string]$AbsolutePath
    )
    if ($AbsolutePath -like "$ProjectDir*") {
        $RelativePath = $AbsolutePath.Substring($ProjectDir.Length).TrimStart('\')
        return ".\$ProjectDirName\$RelativePath"
    } else {
        return $AbsolutePath
    }
}

# Function to resolve icon paths
function Resolve-IconPath {
    param (
        [string]$Library,
        [string]$Filename
    )
    $ResolvedPath = "$Library\media\media-ico\$Filename"
    return $ResolvedPath
}

# Find all desktop.ini files
$DesktopIniFiles = Get-ChildItem $ProjectDir -Recurse -Filter "desktop.ini" -Force

if ($DesktopIniFiles.Count -eq 0) {
    if ($VerboseMode) { Write-Host "No desktop.ini files found." }
    Exit 0
}

foreach ($File in $DesktopIniFiles) {
    $DesktopIniPath = $File.FullName
    $RelativeDesktopIniPath = Convert-ToRelativePath -AbsolutePath $DesktopIniPath

    try {
        # Read content
        $FileContent = Get-Content $DesktopIniPath

        # Update paths
        $UpdatedLines = @()
        $Changed = $false
        $CurrentIconFilename = ""  # Variable to store the current icon filename
        $RelativeIconPath = ""    # Variable for relative icon path
        foreach ($Line in $FileContent) {
            if ($Line -like "IconResource=C:\Users\user\Documents\dev\AgMEQ\*") {
                $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=C:\Users\user\Documents\dev\AgMEQ\", "")
                $CurrentIconFilename = $ExistingFilename  # Store the current icon filename
                $NewPath = Resolve-IconPath -Library $ProjectDirName -Filename $ExistingFilename
                $RelativeIconPath = Convert-ToRelativePath -AbsolutePath $NewPath

                if ($Line -ne "IconResource=C:\Users\user\Documents\dev\AgMEQ\$NewPath") {
                    # Only update if the new path is different
                    $UpdatedLines += "IconResource=C:\Users\user\Documents\dev\AgMEQ\$NewPath"
                    $Changed = $true
                } else {
                    $UpdatedLines += $Line
                }
            } else {
                $UpdatedLines += $Line
            }
        }

        # Write changes if any
        if ($Changed) {
            Set-Content $DesktopIniPath -Value $UpdatedLines -Force
            if ($VerboseMode) {
                Write-Host "$RelativeDesktopIniPath -> $RelativeIconPath"
            }
        } else {
            if ($VerboseMode) {
                # Include the relative path to the icon file for unchanged files
                Write-Host "$RelativeDesktopIniPath ~ $RelativeIconPath"
            }
        }
    } catch {
        if ($VerboseMode) {
            Write-Error "Failed: $RelativeDesktopIniPath, Error: $($_.Exception.Message)"
        }
    }
}