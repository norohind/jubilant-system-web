import json
import time

with open('available.json', 'r', encoding='utf-8') as available_file:
    TAG_COLLECTIONS: dict = json.load(available_file)['SquadronTagData']['SquadronTagCollections']


def resolve_user_tag(single_user_tag: int) -> [str, str]:
    for tag_collection in TAG_COLLECTIONS:
        for tag in tag_collection['SquadronTags']:
            if tag['ServerUniqueId'] == single_user_tag:
                return tag_collection['localisedCollectionName'], tag['LocalisedString']


def resolve_user_tags(user_tags: list[int]) -> dict[str, list[str]]:
    """Function to resolve user_tags list of ints to dict with tag collections as keys and list of tags as value

    :param user_tags: list of ints of tags to resolve
    :return: dict of tags
    """

    _resolved_tags: dict[str, list[str]] = dict()

    for user_tag in user_tags:
        collection_name, tag_name = resolve_user_tag(user_tag)
        if collection_name in _resolved_tags:  # if key in dict
            _resolved_tags[collection_name].append(tag_name)

        else:
            _resolved_tags.update({collection_name: [tag_name]})

    return _resolved_tags


def humanify_resolved_user_tags(user_tags: dict[str, list[str]], do_tabulate=True) -> str:
    """Function to make result of resolve_user_tags more human readable

    :param do_tabulate: if we should insert tabulation or you already did it in source data, default to True
    :param user_tags: result of resolve_user_tags function
    :return: string with human-friendly tags list
    """

    result_str: str = str()
    if do_tabulate:
        tab = '    '

    else:
        tab = str()

    for tag_collection_name in user_tags:
        result_str += f"{tag_collection_name}:\n"

        for tag in user_tags[tag_collection_name]:
            result_str += f"{tab}{tag}\n"

    return result_str


def measure(function: callable, name_to_display: str = ''):
    """
    Decorator to measure function (method) execution time
    Use as easy as

    @utils.measure
    def im_function_to_measure():
        ....

    :param name_to_display:
    :param function:
    :return:
    """
    if name_to_display != '':
        name_to_display = name_to_display + ':'

    def decorated(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print(f'{name_to_display}{function.__name__}: {(end - start) * 100} ms')
        return result

    return decorated


class Measure:
    def __init__(self, name: str):
        self.start = time.time()
        self.name = name

    def record(self) -> None:
        print(f'{self.name}: {(time.time() - self.start) * 100} ms')


pretty_keys_mapping = {
        'name': 'Squadron name',
        'tag': 'Tag',
        'member_count': 'Members',
        'owner_name': 'Owner',
        'platform': 'Platform',
        'created': 'Created UTC',
        'power_name': 'Power name',
        'super_power_name': 'Super power name',
        'faction_name': 'Faction name',
        'user_tags': 'User tags',
        'inserted_timestamp': 'Updated UTC',
}
