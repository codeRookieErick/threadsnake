from asyncio import subprocess
import os
import json
from typing import Dict, List

commands:List[str] = ["::Auto-generate4d script"]

configurationPath:str = os.sep.join([os.path.abspath(os.curdir), 'build.json'])


file = open(configurationPath, 'r')
configuration = json.load(file)
file.close()

configuration["version"]["build"] += 1

if configuration["options"]["cleanDist"] and os.path.isdir("dist"):
    for f in os.listdir("dist"):
        path = os.sep.join(["dist", f])
        commands.append(f'del {path}')

major:int = configuration["version"]["major"]
minor:int = configuration["version"]["minor"]
build:int = configuration["version"]["build"]
version:str = f'{major}.{minor}.{build}'

wheel:str = configuration["templates"]["wheel"].replace("{version}", version)

commands.append(f'echo {version} > src\\threadsnake\\version.txt')
commands.append(f'call py -m build')
commands.append(configuration["commands"]["uninstall"])
commands.append(f'pip3 install dist\\{wheel}')


for command in commands:
    os.system(command)

with open(configurationPath, 'w') as f:
    json.dump(configuration, f, indent=4)
