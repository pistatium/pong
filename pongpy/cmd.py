import click

from pongpy.pong import Pong


@click.command()
def cmd():
    from pongpy.teams.random_team import RandomTeam
    from pongpy.teams.follow_team import FollowTeam
    Pong(FollowTeam(), RandomTeam())


def main():
    cmd()


if __name__ == '__main__':
    main()
