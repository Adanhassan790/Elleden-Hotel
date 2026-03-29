# This script automates the railway link process
$ErrorActionPreference = "Stop"

# We need to select:
# 1. Workspace: Adan Adi's Projects (first option, press Enter)
# 2. Project: overflowing-enthusiasm (second option, press Down then Enter)
# 3. Environment: production (first option, press Enter)
# 4. Service: Postgres (first option, press Enter)

# Start the process and feed input
$process = Start-Process -FilePath "railway" -ArgumentList "link","--project","overflowing-enthusiasm" -PassThru -NoNewWindow

# Give it a moment to start
Start-Sleep -Milliseconds 500

# Try using SendKeys (might not work in all contexts)
try {
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait("{DOWN}{ENTER}")
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
} catch {
    Write-Host "SendKeys not available, trying alternative method..."
}

# Wait for process to complete
$process | Wait-Process

Write-Host "Railway link process completed"
