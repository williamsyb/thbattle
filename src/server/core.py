# -*- coding: utf-8 -*-

# -- stdlib --
from collections import defaultdict
from typing import Dict, Tuple

# -- third party --
# -- own --
from . import parts
from .base import Game
from .endpoint import Client
from game.base import Packet
from utils.events import EventHub


# -- code --
class Options(object):
    def __init__(self, options):
        self.node         = options.get('node', 'localhost')  # Current node name
        self.backend      = options.get('backend', '')        # Backend URI
        self.interconnect = options.get('interconnect', '')   # URI of chat server
        self.archive_path = options.get('archive_path', '')   # file:// URI of dir for storing game archives
        self.disables     = options.get('disables', [])       # disabled core components, will assign a None value


class Events(object):
    def __init__(self) -> None:
        # ev = (core: Core)
        self.core_initialized = EventHub[Core]()

        # Fires when user state changes,
        # ev = (c: Client, from: str, to: str)
        self.user_state_transition = EventHub[Tuple[Client, str, str]]()

        # Client connected
        self.client_connected = EventHub[Client]()

        # Client dropped(connection lost)
        self.client_dropped = EventHub[Client]

        # Client logged in when previous login still online, or still in active game
        # ev = c: Client  # old client obj with new connection `pivot_to`ed to it
        self.client_pivot = EventHub[Client]()

        # Client send some command
        # ev = (c: Client, args: (...))
        self.client_command: Dict[str, EventHub[Tuple[Client, list]]] = \
            defaultdict(lambda: EventHub[Tuple[Client, list]]())

        # Game is created
        # ev = g: Game
        self.game_created = EventHub[Game]()

        # Sent client game data
        self.game_data_send = EventHub[Tuple[Game, Client, Packet]]()

        # Received client game data
        self.game_data_recv = EventHub[Tuple[Game, Client, Packet]]()

        # Fires after old game ended and new game created.
        # Actors should copy settings from old to new
        # ev = (old: Game, g: Game)
        self.game_successive_create = EventHub[Tuple[Game, Game]]()

        # Game started running
        # ev = (g: Game)
        self.game_started = EventHub[Game]()

        # Client joined a game
        # ev = (g: Game, c: Client)
        self.game_joined = EventHub[Tuple[Game, Client]]()

        # Client left a game
        # ev = (g: Game, c: Client)
        self.game_left = EventHub[Tuple[Game, Client]]()

        # Game was ended, successfully or not.
        # ev = (g: Game)
        self.game_ended = EventHub[Game]()

        # Game ended in half way.
        # This fires before GAME_ENDED
        # ev = (g: Game)
        self.game_aborted = EventHub[Game]()


class Core(object):
    def __init__(self: 'Core', **options):
        self.options = Options(options)

        self.events = Events()

        disables = self.options.disables

        if 'auth' not in disables:
            self.auth = parts.auth.Auth(self)

        if 'lobby' not in disables:
            self.lobby = parts.lobby.Lobby(self)

        if 'room' not in disables:
            self.room = parts.room.Room(self)

        if 'game' not in disables:
            self.game = parts.game.Game(self)

        if 'observe' not in disables:
            self.observe = parts.observe.Observe(self)

        if 'invite' not in disables:
            self.invite = parts.invite.Invite(self)

        if 'item' not in disables:
            self.item = parts.item.Item(self)

        if 'reward' not in disables:
            self.reward = parts.reward.Reward(self)

        if 'match' not in disables:
            self.match = parts.match.Match(self)

        if 'admin' not in disables:
            self.admin = parts.admin.Admin(self)

        if 'kedama' not in disables:
            self.kedama = parts.kedama.Kedama(self)

        if 'archive' not in disables:
            self.archive = parts.archive.Archive(self)

        if 'hooks' not in disables:
            self.hooks = parts.hooks.Hooks(self)

        if 'connect' not in disables:
            self.connect = parts.connect.Connect(self)

        if 'backend' not in disables:
            self.backend = parts.backend.Backend(self)

        if 'log' not in disables:
            self.log = parts.log.Log(self)

        if 'stats' not in disables:
            self.stats = parts.stats.Stats(self)

        if 'view' not in disables:
            self.view = parts.view.View(self)

        self.events.core_initialized.emit(self)
