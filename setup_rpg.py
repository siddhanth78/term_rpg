import os
import json

if os.path.exists("worlds") == False:
    os.mkdir("worlds")
    
if os.path.exists("players") == False:
    os.mkdir("players")
    
settings = {"max_slots": 3, "worlds_available": 0, "all_worlds": []}

with open(".settings", "w") as f:
    f.write(json.dumps(settings))