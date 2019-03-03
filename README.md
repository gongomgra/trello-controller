# trello-controller

This Python script plays with the trello.com API using the [py-trello](https://pypi.org/project/py-trello/) module.

The `trello_controller.py` script reads orders from a JSON file and runs them agains the trello.com API. The available orders are:

- create_boards: creates a new board named 'name'.
- create_lists: creates lists in the selected board.
- create_labels: creates labels in the selected board.
- create_cards: creates cards in the selected board.
- set_labels: set labels for a card in a board.

# Instructions

1. Install required python packages from `requirements.txt`:

```
pip install -r requirements.txt
```

2. Copy the `config.py.tpl` template to `config.py`:

```
cp config.py.tpl config.py
```

3. Modify the `config.py` file with your trello.com API values.

4. Generate the JSON file with the orders you want to run. For example, `orders.json`:

```
{
    "orders": [
        {
            "board": null,
            "create_boards": [
                {
                    "name": "test-board",
                    "permission_level": "private",
                    "lists": ["TODO", "Doing", "Done"]
                },
                {
                    "name": "test-board-2",
                    "permission_level": "private",
                    "lists": ["TODO", "Doing", "Done"]
                }
            ]
        },
        {
            "board": "test-board",
            "create_cards": [
                {
                    "name": "Test card 1",
                    "list": "Doing",
                    "labels": ["Important"]
                },
                {
                    "name": "Test card 2",
                    "list": "TODO"
                }
            ],
            "create_labels": [
                {
                    "name": "Important",
                    "color": "red"
                },
                {
                    "name": "Low",
                    "color": "yellow"
                }
            ]
        },
        {
            "board": "test-board-2",
            "prefix": "TB2",
            "create_labels": [],
            "create_cards": [
                {
                    "name": "Test card 3"
                }
            ]
        }
    ]
}
```

5. Run the `trello_controller.py` script passing the `orders.json` as argument:

```
python -B trello_controller.py orders.json
```

> Note: alternatively, you can use a virtualenv to install the required packages.
