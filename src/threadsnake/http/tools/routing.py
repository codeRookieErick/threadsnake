##    Threadsnake. A tiny experimental server-side express-like library.
##    Copyright (C) 2022  Erick Fernando Mora Ramirez
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##
##    mailto:erickfernandomoraramirez@gmail.com

import importlib
import os
from types import ModuleType
from typing import List, Tuple

from ..application import Application
from ..router import Router

ConfiguredRoute = Tuple[str, List[Router]]

def get_routers(moduleName:str) -> List[Router]:
    routers:List[Router] = []
    module:ModuleType = importlib.import_module(moduleName)
    for property in dir(module):
        if isinstance(getattr(module, property), Router):
            routers.append(getattr(module, property))
    return routers

def load_router(path:str) -> ConfiguredRoute:
    if not path.endswith('.py'):
        return
    path = path[:-3]
    pathParts:List[str] = [i for i in path.replace(os.sep, '.').split('.') if len(i) > 0]
    module:str = '.'.join(pathParts)
    path:str = '/'.join(pathParts[1:])
    return path, get_routers(module)

def load_routes(path:str) -> List[ConfiguredRoute]:
    configuredRoutes: List[ConfiguredRoute] = []
    modules:List[str] = [i for i in os.listdir(path) if i.endswith('.py')]
    for module in modules:
        configuredRoutes.append(load_router(os.sep.join([path, module])))
    return configuredRoutes
        
def configure_routes(app:Application, path:str) -> None:
    for configuredRoute in load_routes(path):
        for router in configuredRoute[1]:
            app.use_router(router, configuredRoute[0])