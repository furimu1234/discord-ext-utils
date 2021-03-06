import re

from more_itertools import unique_everseen

from .unicode_emojis import emojis


__all__ = ("encode", "decode", "listup", "count", "get", "emojis")

_text_to_emoji_regex = re.compile("(?P<all>:(?P<name>.+?):)")
(_reversed := [*emojis.items()]).reverse()
_swaped_emojis = {v: k for k, v in _reversed}
_emoji_to_text_regex = re.compile("(?P<emoji>%s)" % (
    "|".join(map(re.escape, _swaped_emojis.keys()))
))


def encode(text):
    def repl(match):
        name = match.group("name")
        emoji = emojis.get(name, None)
        if emoji is None:
            return match.group("all")
        return emoji
    return _text_to_emoji_regex.sub(repl, text)


def decode(text):
    def repl(match):
        emoji = match.group("emoji")
        return ":%s:" % _swaped_emojis.get(emoji, None)
    return _emoji_to_text_regex.sub(repl, text)


def listup(text):
    return _emoji_to_text_regex.findall(text)


def count(text, unique=False):
    func = set if unique else list
    return len(func(listup(text)))


def get(text, keep_order=False):
    func = unique_everseen if keep_order else set
    return tuple(func(listup(text)))
