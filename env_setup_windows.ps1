# Build images in the correct directory
docker compose build

# Store current directory (absolute path)
$cwd = (Get-Location).Path

# Open tabs in the SAME directory
wt.exe `
    new-tab --title "Server"   --startingDirectory "$cwd" powershell -NoExit -Command "docker compose up -d server" `
    ';' new-tab --title "Client 1" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm -it client1" `
    ';' new-tab --title "Client 2" --startingDirectory "$cwd" powershell -NoExit -Command "docker compose run --rm -it client2"
