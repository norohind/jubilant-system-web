squads_by_tag_extended_raw_keys = """select 
    name,
    tag,
    member_count,
    owner_name,
    owner_id,
    platform,
    created,
    null_fdev(power_name) as power_name,
    null_fdev(superpower_name) as super_power_name,
    null_fdev(faction_name) as faction_name,
    user_tags,
    motd,
    "date",
    author,
    cmdr_id,
    updated as inserted_timestamp,
    squad_id
from squadrons_current_data
where tag = :tag  
order by platform;
"""

squads_by_tag_pattern_extended_raw_keys = """select 
    name,
    tag,
    member_count,
    owner_name,
    owner_id,
    platform,
    created,
    null_fdev(power_name) as power_name,
    null_fdev(superpower_name) as super_power_name,
    null_fdev(faction_name) as faction_name,
    user_tags,
    motd,
    "date",
    author,
    cmdr_id,
    updated as inserted_timestamp,
    squad_id
from squadrons_current_data 
where tag like :tag 
order by platform;
"""

name2tags = """select
    platform,
    squad_id,
    updated as updated_at,
    name,
    tag
from squadrons_current_data
where lower(name) = lower(:name);"""
