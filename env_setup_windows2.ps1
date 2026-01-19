# Save as run_messenger.ps1
$cwd = (Get-Location).Path

wt.exe `
    new-tab --title "Server"   --startingDirectory "$cwd" powershell -NoExit -Command "py server_side/src/server_main.py" `
    ';' new-tab --title "Client 1" --startingDirectory "$cwd" powershell -NoExit -Command "py client_side/src/main.py" `
    ';' new-tab --title "Client 2" --startingDirectory "$cwd" powershell -NoExit -Command "py client_side/src/main.py"
