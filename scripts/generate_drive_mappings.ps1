$drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -match '^[A-Z]:\\$' }

$overrideContent = @"
version: '3.8'
services:
  api:
    volumes:
"@

foreach ($drive in $drives) {
    $driveLetter = $drive.Name.ToLower()
    $overrideContent += "`n      - $($drive.Name):\:/host/$driveLetter"
}

$overrideContent | Out-File -FilePath "docker-compose.override.yml" -Encoding UTF8
Write-Host "Generated docker-compose.override.yml with $($drives.Count) drives"