import json
import logging
import os
from typing import Literal

import aiofiles
from discord.ext import commands
from discord.ext.commands import Context

log = logging.getLogger(__name__)


class GroupsHelper:
    def __init__(self, groups_path: str = "./data/groups.json") -> None:
        self.groups_path = groups_path
        self.groups: dict[str, list] = {}
        if not os.path.isfile(groups_path):
            self.groups = {}
        else:
            with open(self.groups_path, "r", encoding="utf-8") as f:
                self.groups = json.load(f)

    def in_group(self, group_name: str):
        def predicate(ctx: Context):
            group = self.groups.get(group_name)
            if not group:
                return False

            if "*" in group:
                return True
            elif ctx.author.id in group:
                return True
            else:
                return False

        return commands.check(predicate)

    async def add(self, group_name: str, id: int | Literal["*"]) -> None:
        ids = self.groups.get(group_name, [])
        ids.append(id)

        self.groups[group_name] = ids

        async with aiofiles.open(self.groups_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.groups))

        log.info(f"Added {id} to {group_name}")

    async def remove(self, group_name: str, id: int | Literal["*"]) -> None:
        ids = self.groups.get(group_name, [])
        if id in ids:
            ids.remove(id)

        self.groups[group_name] = ids

        async with aiofiles.open(self.groups_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.groups))

        log.info(f"Removed {id} from {group_name}")
