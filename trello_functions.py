"""
trello_functions.py

Helper functions for the trello_controller program. User 'pytrello' module
"""

import sys

import trello
import config


def connect_with_trello():
    """
    Connects with Trello using config.py values.
    """
    # .- stablish connection
    print("Connecting with Trello...")
    client = trello.TrelloClient(
        api_key=config.API_KEY,
        api_secret=config.API_SECRET
    )
    print("Connection stablished")
    # .- return TrelloClient object
    return client


def get_board_by_name(client=None, name=None):
    """
    Returns board reference searched by name.
    """
    # .- fail if name not provided
    if name is None:
        print("get_board_by_name(): a 'name' must be provided")
        sys.exit(1)
    else:
        # .- compare lowercase
        name = name.lower()

    # .- stablish connection if not provided
    if client is None:
        client = connect_with_trello()

    # .- get boards and obtain board object for name
    board = None
    for b in client.list_boards():
        if (b.name.lower().find(name) != -1):
            board = b

    # .- return board reference
    return board


def get_list_by_name(board=None, name=None):
    """
    Returns list reference searched by name.
    """
    # .- fail if no board provided
    if board is None:
        print("get_list_by_name(): a 'board' must be provided")
        sys.exit(1)

    # .- fail if no name provided
    if name is None:
        print("get_list_by_name(): a 'name' must be provided")
        sys.exit(1)
    else:
        # .- lowercase to compare
        name = name.lower()

    # .- get lists and obtain list object for name
    required_list = None
    for l in board.all_lists():
        if (l.name.lower().find(name) != -1):
            required_list = l

    # .- return required list reference
    return required_list


def get_card_by_name(board=None, name=None):
    """
    Returns card reference searched by name.
    """
    # .- fail if no board provided
    if board is None:
        print("get_card_by_name(): a 'board' must be provided")
        sys.exit(1)

    # .- fail if no name provided
    if name is None:
        print("get_card_by_name(): a 'name' must be provided")
        sys.exit(1)
    else:
        # .- lowercase to compare
        name = name.lower()

    # .- get cards and obtain card object for name
    card = None
    for c in board.all_cards():
        if (c.name.lower().find(name) != -1):
            card = c

    # .- return required card reference
    return card


def get_label_by_name(board=None, name=None):
    """
    Returns label reference searched by name.
    """
    # .- fail if no board provided
    if board is None:
        print("get_label_by_name(): a 'board' must be provided")
        sys.exit(1)

    if name is None:
        print("get_label_by_name(): a label 'name' must be provided")
        sys.exit(1)

    required_label = None
    for label in board.get_labels():
        if label.name.upper() == name.upper():
            required_label = label

    return required_label


def get_card_by_id(board=None, cid=None):
    """
    Returns card reference searched by id.
    """
    # .- fail if no board provided
    if board is None:
        print("get_card_by_id(): a 'board' must be provided")
        sys.exit(1)

    # .- fail if no name provided
    if cid is None:
        print("get_card_by_id(): an 'id' must be provided")
        sys.exit(1)
    else:
        # .- get only id number
        short_id = int(str(cid).lstrip("T").lstrip("0"))

    # .- get cards and obtain card object for name
    card = None
    for c in board.all_cards():
        if (int(c.idShort) == short_id):
            card = c

    # .- return required card reference
    return card


def get_label_by_id(board=None, lid=None):
    """
    Returns label reference searched by id.
    """
    # .- fail if no board provided
    if board is None:
        print("get_label_by_id(): a 'board' must be provided")
        sys.exit(1)

    if lid is None:
        print("get_label_by_id(): a label 'id' must be provided")
        sys.exit(1)

    required_label = None
    for label in board.get_labels():
        if label.id == lid:
            required_label = label

    return required_label


def create_card(client=None, board=None, prefix="", values=None):
    """
    Creates new card in a Trello 'board'.
    """
    _create_card = True

    # .- fail if no board provided
    if board is None:
        print("create_card(): a 'board' must be provided")
        sys.exit(1)
    else:
        board = get_board_by_name(client, board)

    # .- Check if name provided
    if "name" not in values:
        msg = "Card must have a 'name'"
        print(msg)
        _create_card = False

    # .- fail if destination list not provided or not exists
    if ("list" not in values) or (values["list"] is None):
        print("create_card(): a destination 'list' must be provided")
        sys.exit(1)
    else:
        dest_list = get_list_by_name(board, values["list"])

    # .- no 'labels' in values or empty
    if ("labels" not in values) or \
       (values["labels"] is None) or \
       (len(values["labels"]) == 0):
        add_labels = False
    else:
        add_labels = True

    # .- no 'description'
    if "description" not in values:
        values["description"] = None

    # .- do not create card if exists
    new_card = None
    card_found = get_card_by_name(
        board=board,
        name=values["name"]
    )

    if (card_found is None) and (_create_card is True):
        new_card = dest_list.add_card(
            name=values["name"],
            desc=values["description"],
        )

        # .- rename card with '[{prefix}{id_number}]'
        task_id = "%04d" % new_card.idShort
        short_id = "[{p}{ids}]".format(p=prefix, ids=task_id)
        new_name = "{ids} {n}".format(ids=short_id, n=new_card.name)
        new_card.set_name(new_name)

        # .- add labels
        if add_labels is True:
            for label in values["labels"]:
                # .- get label object
                board_label = get_label_by_name(board, label)
                # .- skip if label do not exists
                if board_label is None:
                    print("Label '{label}' do not exists".format(label=label))
                    continue
                else:
                    new_card.add_label(board_label)

    else:
        msg = "Card already exists with id: {id}".format(id=card_found.idShort)
        print(msg)

    # .- return generated card
    return new_card


def create_board(client=None, values=None):
    """
    Creates new board in Trello.
    """
    # .- Connect with Trello if necessary
    if client is None:
        client = connect_with_trello()

    # .- Check user input
    if ("name" not in values) or (values["name"] is None):
        print("You can not create an unnamed board")
        sys.exit(1)

    if ("permission_level" not in values):
        values["permission_level"] = "private"

    if "remove_labels" not in values:
        values["remove_labels"] = True

    flag_create_lists = True
    if ("lists" not in values) or \
       (len(values["lists"]) == 0):
        flag_create_lists = False

    # .- Check if board name exists
    if get_board_by_name(client, values["name"]) is not None:
        msg = "Board '{b}' already exists".format(b=values["name"])
        print(msg)
    else:
        msg = "Creating board '{b}'...".format(b=values["name"])
        print(msg)
        board = client.add_board(
            board_name=values["name"],
            permission_level=values["permission_level"],
            default_lists=False
        )

        # .- create lists if present
        if flag_create_lists is True:
            create_lists(
                board=board,
                lists_to_create=values["lists"]
            )

        # .- remove default labels
        if values["remove_labels"] is True:
            for label in board.get_labels():
                print("Removing default label '{id}'".format(id=label.id))
                board.delete_label(label.id)

        print("Created board successfully")


def create_lists(board=None, lists_to_create=None, pos=-1):
    """
    Creates multiple lists in a Trello 'board'.
    """
    if board is None:
        msg = "Cannot create list for board 'None'"
        print(msg)

    elif (lists_to_create is None) or \
            (len(lists_to_create) == 0):
        pass
    else:
        # .- generate list and place them from left to right on board
        if pos <= 0:
            pos = 1

        for li in lists_to_create:
            if get_list_by_name(board, li) is None:
                print("Creating list: '{li}'".format(li=li))
                board.add_list(li, pos)
                pos += 1


def create_labels(client=None, board=None, labels=None):
    """
    Creates multiple labels in a Trello 'board'.
    """
    # .- fail if no board provided
    if board is None:
        print("create_labels(): a 'board' must be provided")
        sys.exit(1)
    else:
        board = get_board_by_name(client, board)

    # .- fail if destination list not provided or not exists
    if labels is None:
        print("create_labels(): a 'labels' list must be provided")
        sys.exit(1)

    available_labels = get_labels(board)

    print("create_labels(): {}".format(labels))
    for label in labels:
        create_label(board, label, available_labels)


def create_label(board=None, values=None, available_labels=None):
    """
    Creates label in a Trello 'board'.
    """
    add_label = False
    if available_labels is None:
        available_labels = {}
    # .- check label is valid
    if "name" not in values:
        print("create_label(): label must set a 'name'")
        sys.exit(1)
    elif values["name"].upper() not in available_labels:
        add_label = True

    if "color" not in values:
        print("create_label(): setting default color to 'green'")
        values["color"] = "green"

    # .- create label
    if add_label is True:
        new_label = board.add_label(
            name=values["name"],
            color=values["color"]
        )

        msg = "Created label '{n}' with id: '{id}'". format(
            n=new_label.name,
            id=new_label.id
        )
        print(msg)

    else:
        msg = "Label named '{n}' already exists with id '{lid}'"
        msg = msg.format(
            n=values["name"],
            lid=available_labels[values["name"].upper()]
        )
        print(msg)


def get_labels(board=None):
    """
    Returns a Python dict with labels in a Trello 'board'.
    """
    # .- fail if no board provided
    if board is None:
        print("get_labels(): a 'board' must be provided")
        sys.exit(1)
    else:
        labels = board.get_labels()

    labels_dict = {}

    for label in labels:
        labels_dict[label.name.upper()] = label.id

    return labels_dict
