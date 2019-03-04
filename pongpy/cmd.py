import importlib

import click

from pongpy.pong import PongMatch


@click.command()
@click.argument('team1', default='pongpy.teams.random_team:RandomTeam')
@click.argument('team2', default='pongpy.teams.follow_team:FollowTeam')
def cmd(team1, team2):
    t1 = dynamic_import(team1)
    t2 = dynamic_import(team2)
    PongMatch(t1(), t2()).start()


def main():
    cmd()


def dynamic_import(name):
    module_name, class_name = name.split(':')
    module = importlib.import_module(module_name)
    klass = getattr(module, class_name)
    return klass


if __name__ == '__main__':
    main()
