#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Game of Pig
"""

import random
import adts
import argparse


class Pig(object):
    """
    Game of Pig class
    """

    def __init__(self, players=2):
        """
        Pig game constructor
        :param players: (Int) - Number of players
        :return: None
        """
        self.players = adts.Queue()
        for num in xrange(players):
            self.players.enqueue(Player('Player' + str(num)))
        self.current_player = self.players.dequeue()
        self.current_player.turn = True
        print 'Current player: {}'.format(self.current_player.name)
        self.die = Die()

    def next_player(self):
        """
        Switch game to next player.
        :return: None
        """
        self.current_player.turn = False
        self.players.enqueue(self.current_player)
        self.current_player = self.players.dequeue()
        print 'Next player is {}'.format(self.current_player.name)
        self.current_player.turn = True

    def start_game(self):
        """
        Play the game
        :return: None
        """
        ask = 'Roll (R) Hold (H) or Quit (Q)?[Q]'
        ask_player = raw_input(ask)
        while ask_player:

            if ask_player.upper()[0] == 'R' and self.current_player.turn:
                num = self.current_player.play(self.die)
                if num == 1:
                    self.current_player.points = []
                    print '{} loses turn. Score set to {}'\
                        .format(self.current_player.name,
                                self.current_player.get_score())
                    self.next_player()
                else:
                    self.current_player.points.append(num)
                    score = self.current_player.get_score()
                    if score >= 100:
                        print '{} wins. Score: {}'.format(self.current_player.name, score)
                        break

            elif ask_player.upper()[0] == 'H':
                print '{} Holds. Score: {}'\
                    .format(self.current_player.name,
                            self.current_player.get_score())
                self.next_player()

            elif ask_player.upper()[0] == 'Q':
                print 'Quitting game...'
                self.players.enqueue(self.current_player)
                while self.players.size() > 0:
                    player = self.players.dequeue()
                    print 'Player {}: {}'.format(player.name, player.score)
                break

            print 'Player: ', self.current_player.name
            print 'Score: ', self.current_player.get_score()
            ask_player = raw_input(ask)


class Die(object):
    """
    Die class
    """
    faces = (1, 2, 3, 4, 5, 6)

    def roll(self):
        """
        Alea jacta est
        :return: (Int) - The die face
        """
        face = random.choice(self.faces)
        print 'Die face: {}'.format(face)
        return face


class Player(object):
    """
    Player
    """

    def __init__(self, name):
        """
        Constructor
        :param name: (String) Player identifier
        :return: (None)
        """
        self.name = name
        self.turn = False
        self.points = []
        self.score = 0
        self.plays = 0
        self.die = Die()

    def hold(self):
        """
        Take points and lose turn
        :return: (Int) - Player points
        """
        self.turn = False

    def play(self, die):
        """
        Roll the die
        :param die: (Object) Die instance
        :return: (None)
        """
        if self.turn:
            print 'Rolling the die...'
            return die.roll()

    def get_score(self):
        """
        Sum and return accumulated points
        :return: (Int) - Player's score
        """
        self.score = sum(self.points)
        return self.score


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--numPlayers', required=False, type=int, default=2)
    NUM = PARSER.parse_args()
    if NUM.numPlayers > 1:
        game = Pig(NUM.numPlayers)
        game.start_game()
    else:
        print 'You need at least two players for this game.'
