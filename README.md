# WANKA NUKER

## setup

1. create bot at discord.com/developers
2. enable all Privileged Gateway Intents
3. invite with admin perms:
   https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands
4. paste token into TOKEN in main.py

## deploy (Railway)

1. push repo to github
2. railway.app → New Project → Deploy from GitHub
3. add env var: TOKEN = your token
4. deploy

## deploy (Render)

1. push repo to github
2. render.com → New → Background Worker → connect repo
3. add env var: TOKEN = your token
4. build command: pip install -r requirements.txt
5. start command: python main.py

## usage

/nuke — fires in target server where bot has admin
