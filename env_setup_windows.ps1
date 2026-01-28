docker compose build

# store current directory (absolute path)
$cwd = (Get-Location).Path

# open tabs in the same dir
wt.exe `
    new-tab --title "Server"   --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm server" `
    ';' new-tab --title "Client 1" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm client1" `
    ';' new-tab --title "Client 2" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm client2"