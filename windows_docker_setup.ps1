# start server and 2 clients | update builds and specify project name (main)
docker compose -p main up --build --scale client=2 -d

# open two tabs with client apps
wt `
  new-tab powershell -NoExit -Command "docker exec -it main-client-1 python3 /app/main.py" `
  ';' new-tab powershell -NoExit -Command "docker exec -it main-client-2 python3 /app/main.py"