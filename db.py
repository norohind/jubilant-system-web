import json
import os
import aiosqlite
from schemas import Squad


uri = f'file:{os.environ["DB_PATH"]}?mode=ro'


def _patch_user_tags(row: dict) -> None:
    """
    Patches row from query by json.loads'ing user_tags field

    :param row:
    :return:
    """

    row['user_tags'] = json.loads(row['user_tags'])


async def _squads(query: str, params: tuple | dict) -> list[Squad]:
    res: list[Squad] = list()
    async with aiosqlite.connect(uri, uri=True) as db:
        db.row_factory = aiosqlite.Row
        async for squad_row in (await db.execute(query, params)):
            squad_row = dict(squad_row)
            _patch_user_tags(squad_row)
            res.append(Squad(**squad_row))

        return res


async def _squad(query, params: tuple | dict) -> Squad | None:
    async with aiosqlite.connect(uri, uri=True) as db:
        db.row_factory = aiosqlite.Row
        query_result = await (await db.execute(query, params)).fetchone()
        if query_result is not None:
            query_result = dict(query_result)
            _patch_user_tags(query_result)
            return Squad(**query_result)

        else:
            return None


async def squads_by_tag(tag: str) -> list[Squad]:
    return await _squads('select * from squadrons_current_data where tag = ? order by platform;', (tag.upper(),))


async def search_squads_by_tag(tag_pattern: str) -> list[Squad]:
    pattern = f'%{tag_pattern}%'.upper()
    return await _squads('select * from squadrons_current_data where tag like ? order by platform;', (pattern,))


async def squad_by_id(squad_id: int) -> Squad:
    return await _squad('select * from squadrons_current_data where squad_id = ?;', (squad_id,))
