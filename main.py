from fastapi import FastAPI, Path
import schemas
import db


app = FastAPI(title='jubilant-api')


@app.get('/api/squads/now/by-tag/{tag}',
         response_model=list[schemas.Squad],
         description='Get squadrons by tag, it can include up to 3 squadrons (for every platform)',
         name='Squadrons by tag'
         )
async def squads_by_tag(
        tag: str = Path(..., title='Squadron tag to lookup', min_length=4, max_length=4)
):
    return await db.squads_by_tag(tag)


@app.get('/api/squads/now/search/by-tag/{search_pattern}',
         response_model=list[schemas.Squad],
         description='Search squadrons matching by tag',
         name='Squadrons by part of tag'
         )
async def search_by_tag(
        search_pattern: str = Path(..., title='Search pattern', min_length=1, max_length=4)
):
    return await db.search_squads_by_tag(search_pattern)


@app.get('/api/squads/now/by-id/{squad_id}',
         response_model=schemas.Squad,
         description='Returns single squadron matching specified squad_id or nothing',
         name='Squadron by id'
         )
async def squad_by_id(
        squad_id: int = Path(..., title='Squadron id'),
):
    return await db.squad_by_id(squad_id)
