# Sammy v0.1.0-dev

A Discord bot creator that uses JSON as it's primary source for configuring
the bots.

> **WIP!**
> This project is a work in progress, so things might (and will) change!

## How to Use

Sammy is pretty simple, all you have to do is create a `bot.json` file
right next to the `main.py` file and follow a common config structure:

-   Every key found in the root scope of the JSON is considered a root key;
-   Some subkeys support dynamic values, others support formating, and the rest are fully static;
-   Dynamic values may receive values;
-   Error messages can be customized;
-   Mappings allow you to create aliases for commands.

```json
{
    "Bot": {
        "Token": "<file:.token>",
        "ReplyForBots": false
    },
    "Errors": {
        "NoSuchCommand": "Can't understand the command **{cmd}** you mentioned"
    },
    "Commands": {
        "ping": {
            "Reply": ":ping_pong: Pong!"
        },
        "hello": {
            "Reply": "Hey there {author}! How's it shaking?"
        }
    },
    "Mappings": {
        "hello": ["hi", "hey", "howdy"]
    }
}
```

Above is a simple script containing everything Sammy can do so far.

# License

This project is protected under the [GPL v3.0](./LICENSE) license.

# Contributions

Feel free to fork and contribute on this project.
