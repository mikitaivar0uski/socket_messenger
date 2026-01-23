# store current directory (absolute path)
$cwd = (Get-Location).Path

# open tabs in the same dir
wt.exe `
    new-tab --title "Server"   --startingDirectory "$cwd" powershell -NoExit -Command "py server_side/src/server_main.py" `
    ';' new-tab --title "Client 1" --startingDirectory "$cwd" powershell -NoExit -Command "py client_side/src/main.py" `
    ';' new-tab --title "Client 2" --startingDirectory "$cwd" powershell -NoExit -Command "py client_side/src/main.py"
