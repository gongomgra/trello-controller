"""
trello_controller.py

Main file for the trello_controller program.
"""

import sys
import argparse
import json

import trello_functions

# Version string
version = "0.0.1"

class TrelloController(object):
    """
    TrelloController main class.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("orders_file")
        self.all_args = self.parser.parse_args()
        # .- Extract orders_file name from parser
        self.orders_file = self.all_args.orders_file

        # .- Available commands
        self.commands = ["create_boards", "create_lists", "create_labels", "create_cards",
                         "set_labels"]

        self.current_board = None
        self.card_prefix = None
        # .- Connect with Trello
        self.client = trello_functions.connect_with_trello()
        self.boards_list = self.client.list_boards()

        # .- Run orders
        self.run()

    def run(self):
        """
        Run orders from JSON file passed as argument.
        """
        # .- Read file
        with open(self.orders_file) as f:
            orders = json.load(f)["orders"]
            f.close()

        # .- Iterate over orders list to check if 'board' is present or fail
        for order_descriptor in orders:
            if "board" not in order_descriptor:
                print("ERROR: There is an order descriptor without the 'board' key")
                sys.exit(1)

        # .- Run commands in the defined order
        for order_descriptor in orders:
            # .- Set current board
            self.current_board = order_descriptor["board"]

            if "prefix" in order_descriptor:
                self.card_prefix = order_descriptor["prefix"]

            for command in self.commands:
                if command in order_descriptor:
                    msg = "Will run command '{c}' for board '{b}'".format(
                        c=command,
                        b=self.current_board
                    )
                    print(msg)

                    # .- Run exact command
                    getattr(self, command)(order_descriptor[command])

    def create_boards(self, boards_list):
        """
        'create_boards' command.
        """
        for board in boards_list:
            trello_functions.create_board(
                client=self.client,
                values=board
            )

    def create_lists(self, lists_list):
        """
        'create_lists' command.
        """
        # .- ensure we will add lists at the end of current ones
        board = trello_functions.get_board_by_name(
            client=self.client,
            name=self.current_board
        )
        pos = len(board.all_lists()) + 1

        # .- create lists from this position
        trello_functions.create_lists(
            board=board,
            lists_to_create=lists_list,
            pos=pos
        )

    def create_cards(self, cards_list):
        """
        'create_cards' command.
        """
        for card in cards_list:
            # .- create card
            trello_functions.create_card(
                client=self.client,
                board=self.current_board,
                prefix=self.card_prefix,
                values=card
            )

    def create_labels(self, labels_list):
        """
        'create_labels' command.
        """
        print(labels_list)
        trello_functions.create_labels(self.client, self.current_board, labels_list)


if __name__ == '__main__':
    tc = TrelloController()
    del tc
