import sqlite3

import utils
from . import sqlite_sql_requests
import json
import os
from datetime import datetime


class SqliteModel:
    db: sqlite3.Connection

    def get_db(self):
        """
        One connection per request is only one method to avoid sqlite3.DatabaseError: database disk image is malformed.
        Connections in sqlite are extremely cheap (0.22151980000001004 secs for 1000 just connections and
        0.24141229999999325 secs for 1000 connections for this getter, thanks timeit)
        and don't require to be closed, especially in RO mode. So, why not?

        :return:
        """

        db = sqlite3.connect(f'file:{os.environ["DB_PATH"]}?mode=ro', check_same_thread=False, uri=True)
        db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        db.create_function('null_fdev', 1, self.null_fdev, deterministic=True)

        return db

    @staticmethod
    def null_fdev(value):
        if value == '':
            return None

        elif value == 'None':
            return None

        else:
            return value

    def list_squads_by_tag(self, tag: str, pretty_keys=False, resolve_tags=False, extended=False, is_pattern=False) -> list[dict]:
        """
        Take tag and return all squads with tag matches

        :param is_pattern: is tag var is pattern to search
        :param extended: if false, then we don't return tags and motd anyway
        :param resolve_tags: if we should resolve tags or return it as plain list of IDs
        :param pretty_keys: if we should use pretty keys or raw column names from DB
        :param tag: tag to get info about squad
        :return:
        """

        tag = tag.upper()

        if is_pattern:
            query = sqlite_sql_requests.squads_by_tag_pattern_extended_raw_keys
            tag = f'%{tag}%'

        else:
            query = sqlite_sql_requests.squads_by_tag_extended_raw_keys

        squads = self.get_db().execute(query, {'tag': tag}).fetchall()

        squad: dict
        for squad in squads:
            squad['user_tags'] = json.loads(squad['user_tags'])

            """
            We have, according to arguments, to:
            include motd if extended
            try to resolve owner nickname for consoles
            delete owner_id
            resolve tags if extended
            remove tags if not extended
            make keys pretty
            """

            if extended:
                if resolve_tags:  # tags resolving
                    squad['user_tags'] = utils.humanify_resolved_user_tags(utils.resolve_user_tags(squad['user_tags']))

            else:
                del squad['user_tags']

            if squad['platform'] != 'PC':  # then we have to try to resolve owner's nickname using motd
                if squad['owner_id'] == squad['cmdr_id']:
                    squad['owner_name'] = squad['author']

            if squad['date'] is not None:
                squad['date'] = datetime.utcfromtimestamp(squad['date']).strftime('%Y-%m-%d %H:%M:%S')

            del squad['owner_id']  # delete fid anyway
            del squad['cmdr_id']

            # prettify keys
            if pretty_keys:
                for key in list(squad.keys()):

                    pretty_key = utils.pretty_keys_mapping.get(key, key)
                    squad[pretty_key] = squad.pop(key)

        return squads

    def name2tags(self, name: str) -> list[dict]:
        v = self.get_db().execute(sqlite_sql_requests.name2tags, {'name': name}).fetchall()
        return v
