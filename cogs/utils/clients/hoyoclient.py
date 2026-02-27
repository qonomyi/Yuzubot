from typing import cast

import aiohttp

from .baseclient import BaseClient


class HoYoClient(BaseClient):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        super().__init__(session)

    async def verify_l_token(self, cookies: dict) -> bool:
        await self._request(
            "POST",
            "https://passport-api-sg.hoyolab.com/account/ma-passport/token/verifyLToken",
            cookies,
        )

        return True

    async def get_game_record_card(self, cookies: dict, hl_uid: str) -> dict:
        data = await self._request(
            "GET",
            "https://bbs-api-os.hoyolab.com/game_record/card/wapi/getGameRecordCard?uid="
            + hl_uid,
            cookies,
        )
        data = cast(dict, data)

        return data
