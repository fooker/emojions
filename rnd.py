import click
import json
import random
import unicodedata

from nototools import unicode_data as data


EXCLUDED_GROUPS = {
  b'Misc',
  b'Symbols',
  b'Flags',
  b'Component',
}


def run():
    # Select three distinct categories randomly
    categories = random.sample(list(set(data.get_emoji_groups()) - EXCLUDED_GROUPS), k=3)

    # For each category, choose a sub-category
    categories = ((category, random.choice(data.get_emoji_subgroups(category))) for category in categories)

    # Choose a symbol from each sub-category while simplifying the symbol by removing all modifiers
    symbols = [
            random.choice(list({
                emoji
                for emoji
                in (chr(emoji[0])
                    for emoji
                    in data.get_emoji_in_group(*category))
                if unicodedata.name(emoji, False) }))
            for category
            in categories]

    if click.confirm(' '.join(symbols)):
        with open('data', 'a') as f:
            f.write('|'.join((data.name(symbol) for symbol in symbols)))
            f.write('\n')


@click.command()
def main():
    while True:
        run()

if __name__ == '__main__':
    main()
