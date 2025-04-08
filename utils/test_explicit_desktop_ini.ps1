# Define explicit paths to check
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

# Explicit paths for testing
$PathsToCheck = @(
    "$ProjectDir\src\.pyinstaller\desktop.ini",
    "$ProjectDir\media\media-ico\desktop.ini"
)

# Log project paths for debugging
Write-Host "Script Directory"
Write-Host $ScriptDir
Write-Host "Project Directory"
Write-Host $ProjectDir
Write-Host ""
Write-Host "Checking specific desktop.ini files"

foreach ($FilePath in $PathsToCheck) {
    Write-Host ""
    Write-Host "Processing file"
    Write-Host $FilePath

    # Check if the file exists
    if (Test-Path -Path $FilePath) {
        Write-Host "File exists"
        Write-Host $FilePath
        
        try {
            # Read and display the content of desktop.ini
            $FileContent = Get-Content -Path $FilePath
            Write-Host ""
            Write-Host "Content of the file"
            Write-Host "-------------------------"
            foreach ($Line in $FileContent) {
                Write-Host $Line
            }
            Write-Host "-------------------------"

            # Example update: Replace IconResource paths
            $UpdatedLines = @()
            foreach ($Line in $FileContent) {
                if ($Line -like "IconResource=*") {
                    # Extract filename and construct the new path
                    $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=", "")
                    $NewPath = Join-Path -Path $ProjectDir -ChildPath "media\media-ico\$ExistingFilename"
                    Write-Host "Updating IconResource"
                    Write-Host $NewPath
                    $UpdatedLines += "IconResource=$NewPath"
                } else {
                    $UpdatedLines += $Line
                }
            }

            # Write updated content back to the file
            Set-Content -Path $FilePath -Value $UpdatedLines -Force
            Write-Host "Successfully updated the file"
            Write-Host $FilePath

        } catch {
            Write-Error "Failed to process the file"
            Write-Host $FilePath
            Write-Host "Error details"
            Write-Host $_.Exception.Message
        }
    } else {
        Write-Host "File not found"
        Write-Host $FilePath
    }
}

Write-Host ""
Write-Host "Completed processing specified files"