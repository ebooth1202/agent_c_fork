$overrideContent = @"
version: '3.8'
services:
  api:
    volumes:
      # User profile folders
      - $env:USERPROFILE\.agent_c\images:/app/images
      - $env:USERPROFILE\.agent_c\agents:/app/agent_c_config/agents/local
      - $env:USERPROFILE\Documents:/app/workspaces/documents
      - $env:USERPROFILE\Downloads:/app/workspaces/downloads
      - $env:USERPROFILE\Desktop:/app/workspaces/desktop
      - $env:USERPROFILE\.agent_c\saved_sessions:/app/agent_c_config/saved_sessions
      - $env:USERPROFILE\.agent_c\chat_sessions.db:/app/agent_c_config/chat_sessions.db
      - $env:USERPROFILE\.agent_c\chat_chat_user_auth.db:/app/agent_c_config/chat_chat_user_auth.db
      # Host drives
"@

$drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -match '^[A-Z]:\\$' }
foreach ($drive in $drives) {
    $driveLetter = $drive.Name.ToLower()
    $overrideContent += "`n      - $($drive.Name):\:/host/$driveLetter"
}

$overrideContent | Out-File -FilePath "docker-compose.override.yml" -Encoding UTF8
Write-Host "Generated docker-compose.override.yml with $($drives.Count) drives"