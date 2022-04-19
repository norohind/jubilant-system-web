from pydantic import BaseModel


class Squad(BaseModel):
    squad_id: int
    name: str
    tag: str
    owner_id: int
    owner_name: str
    platform: str
    created: str
    created_ts: int
    accepting_new_members: bool
    power_id: int | None
    power_name: str | None
    superpower_id: int | None
    superpower_name: str | None
    faction_id: int | None
    faction_name: str | None
    delete_after: str | None
    credits_balance: int | None
    credits_in: int | None
    credits_out: int | None
    user_tags: list[int]
    member_count: int
    online_count: int | None
    pending_count: int | None
    full: bool
    public_comms: bool | None
    public_comms_override: bool | None
    public_comms_available: bool | None
    current_season_trade_score: int
    previous_season_trade_score: int
    current_season_combat_score: int
    previous_season_combat_score: int
    current_season_exploration_score: int
    previous_season_exploration_score: int
    current_season_cqc_score: int
    previous_season_cqc_score: int
    current_season_bgs_score: int
    previous_season_bgs_score: int
    current_season_powerplay_score: int
    previous_season_powerplay_score: int
    current_season_aegis_score: int
    previous_season_aegis_score: int
    motd: str | None
    author: str | None
    cmdr_id: int | None
    user_id: int | None
    news_id: int | None
    date: int | None
    operation_id: int
    updated: str

    class Config:
        orm_mode = True
