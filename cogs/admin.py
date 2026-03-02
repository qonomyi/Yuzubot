from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import discord
from discord.ext import commands
from discord.ext.commands import Context

if TYPE_CHECKING:
    from bot import Yuzubot


from bot import groups


class Admin(commands.Cog):
    def __init__(self, bot: Yuzubot) -> None:
        self.bot: Yuzubot = bot

    @commands.is_owner()
    @commands.group("groups")
    async def groups(self, ctx: Context):
        pass

    @groups.command("add")
    async def groups_add(
        self, ctx: Context, group_name: str, user: discord.User | Literal["*"]
    ) -> None:
        if isinstance(user, str):
            await groups.add(group_name, user)
        else:
            await groups.add(group_name, user.id)

        await ctx.message.add_reaction("✅")

    @groups.command("remove")
    async def groups_remove(
        self, ctx: Context, group_name: str, user: discord.User | Literal["*"]
    ) -> None:
        if isinstance(user, str):
            await groups.remove(group_name, user)
        else:
            await groups.remove(group_name, user.id)
        await ctx.message.add_reaction("✅")


async def setup(bot: Yuzubot) -> None:
    await bot.add_cog(Admin(bot))
