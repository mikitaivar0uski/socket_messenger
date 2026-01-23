docker compose build

# store current directory (absolute path)
$cwd = (Get-Location).Path

# open tabs in the same dir
wt.exe `
    new-tab --title "Server"   --startingDirectory "$cwd" powershell -NoExit -Command "docker compose up -d server" `
    ';' new-tab --title "Client 1" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm -it client1" `
    ';' new-tab --title "Client 2" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm -it client2"