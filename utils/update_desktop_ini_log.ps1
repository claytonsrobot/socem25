# Define the project directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

# Define the media icon base path
$MediaIconBasePath = Join-Path -Path $ProjectDir -ChildPath "media\media-ico"

Write-Host "Script Directory"
Write-Host $ScriptDir
Write-Host "Project Directory"
Write-Host $ProjectDir
Write-Host "Media Icon Base Path"
Write-Host $MediaIconBasePath
Write-Host ""
Write-Host "Searching for desktop.ini files..."

# Recursively find all desktop.ini files
$DesktopIniFiles = Get-ChildItem -Path $ProjectDir -Recurse -Filter "desktop.ini" -Force

if ($DesktopIniFiles.Count -eq 0) {
    Write-Host "No desktop.ini files found."
    Exit 0
}

foreach ($File in $DesktopIniFiles) {
    $DesktopIniPath = $File.FullName
    Write-Host ""
    Write-Host "Processing file"
    Write-Host $DesktopIniPath

    try {
        # Read and display the content of the desktop.ini file
        $FileContent = Get-Content -Path $DesktopIniPath
        Write-Host ""
        Write-Host "Content of the file"
        Write-Host "-------------------------"
        foreach ($Line in $FileContent) {
            Write-Host $Line
        }
        Write-Host "-------------------------"

        # Update IconResource paths
        $UpdatedLines = @()
        foreach ($Line in $FileContent) {
            if ($Line -like "IconResource=*") {
                $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=", "")
                $NewPath = Join-Path -Path $MediaIconBasePath -ChildPath $ExistingFilename
                Write-Host "Updating IconResource"
                Write-Host $NewPath
                $UpdatedLines += "IconResource=$NewPath"
            } else {
                $UpdatedLines += $Line
            }
        }

        # Write updated content back to the file
        Set-Content -Path $DesktopIniPath -Value $UpdatedLines -Force
        Write-Host "Successfully updated the file"
        Write-Host $DesktopIniPath

    } catch {
        Write-Error "Failed to process the file"
        Write-Host $DesktopIniPath
        Write-Host "Error details"
        Write-Host $_.Exception.Message
    }
}

Write-Host ""
Write-Host "Completed processing all desktop.ini files."