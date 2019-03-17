# -*- coding: utf-8 -*-

# -- stdlib --
from typing import TYPE_CHECKING
import logging

# -- third party --
# -- own --
from server.base import Game as ServerGame
from server.endpoint import Client
import wiremodel

# -- typing --
if TYPE_CHECKING:
    from server.core import Core  # noqa: F401


# -- code --
log = logging.getLogger('server.parts.view')


class View(object):
    def __init__(self, core: 'Core'):
        self.core = core

    def User(self, u: Client) -> wiremodel.User:
        core = self.core

        return {
            'uid': core.auth.uid_of(u),
            'name': core.auth.name_of(u),
            'state': str(core.lobby.state_of(u)),
        }

    def Game(self, g: ServerGame) -> wiremodel.Game:
        core = self.core

        return {
            'gid':      core.room.gid_of(g),
            'type':     g.__class__.__name__,
            'name':     core.room.name_of(g),
            'started':  core.room.is_started(g),
            'online':   len(core.room.online_users_of(g)),
        }

    def GameDetail(self, g: ServerGame) -> wiremodel.GameDetail:
        core = self.core

        return {
            # HACK: workaround TypedDict limitations
            'gid':      core.room.gid_of(g),
            'type':     g.__class__.__name__,
            'name':     core.room.name_of(g),
            'started':  core.room.is_started(g),
            'online':   len(core.room.online_users_of(g)),
            # **self.Game(g),
            'users':  [self.User(u) for u in core.room.users_of(g)],
            'params': core.game.params_of(g),
            'items':  core.item.items_of(g),
        }
