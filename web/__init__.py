import sys

import falcon
import falcon.errors
import json

from model import model
from templates_engine import render

from loguru import logger

logger.remove()
logger.add(sys.stdout, level='DEBUG', backtrace=True, diagnose=False, colorize=False)


class SquadsInfoByTagHtml:
    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, tag: str, details_type: str) -> None:
        resp.content_type = falcon.MEDIA_HTML

        details_type = details_type.lower()

        if details_type not in ['short', 'extended']:
            raise falcon.HTTPBadRequest(description=f'details_type must be one of short, extended')

        resp.text = render(
            'table_template_squad_info_by_tag.html',
            {
                'target_column_name': 'None',
                'target_new_url': '',
                'tag': tag,
                'details_type': details_type.title()
            }
        )


class SquadsInfoByTag:
    def __init__(self, is_pattern: bool):
        self.is_pattern = is_pattern

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, tag: str, details_type: str) -> None:
        """
        Params to request:
        resolve_tags: bool - if we will resolve tags or put it just as tags ids
        pretty_keys: bool - if we will return list of dicts with human friendly keys or raw column names from DB
        motd: bool - if we will also return motd of squad, works only with `extended`

        :param details_type: short or extended, extended includes tags
        :param req:
        :param resp:
        :param tag: can be full tag or pattern, depend on self.is_pattern
        :return:
        """

        resp.content_type = falcon.MEDIA_JSON
        details_type = details_type.lower()

        if details_type not in ['short', 'extended']:
            raise falcon.HTTPBadRequest(description=f'details_type must be one of short, extended')

        extended = details_type == 'extended'

        resolve_tags = req.params.get('resolve_tags', '').lower() == 'true'  # false by default
        pretty_keys = req.params.get('pretty_keys', '').lower() == 'true'  # false by default too

        model_answer = model.list_squads_by_tag(tag, pretty_keys, resolve_tags, extended, self.is_pattern)

        resp.text = json.dumps(model_answer)


class SquadsName2Tags:
    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, name: str):
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(model.name2tags(name))

class AppFixedLogging(falcon.App):
    def _python_error_handler(self, req: falcon.request.Request, resp: falcon.response.Response, error, params):
        __exception__ = error
        logger.opt(exception=True).warning(f'failed on {req.method} {req.path}')
        self._compose_error_response(req, resp, falcon.errors.HTTPInternalServerError())


application = AppFixedLogging()
application.add_route('/squads/now/by-tag/{details_type}/{tag}', SquadsInfoByTagHtml())

application.add_route('/api/squads/now/by-tag/{details_type}/{tag}', SquadsInfoByTag(is_pattern=False))
application.add_route('/api/squads/now/search/by-tag/{details_type}/{tag}', SquadsInfoByTag(is_pattern=True))
application.add_route('/api/squads/now/by-name/{name}', SquadsName2Tags())

if __name__ == '__main__':
    import waitress
    import os
    application.add_static_route('/js', os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), 'js'))
    waitress.serve(application, host='127.0.0.1', port=9486)
