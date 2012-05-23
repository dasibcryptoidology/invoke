from .argument import Argument


class Context(object):
    """
    Parsing context with knowledge of flags & their format.

    Generally associated with the core program or a task.

    When run through a parser, will also hold runtime values filled in by the
    parser.
    """
    def __init__(self, name=None, aliases=()):
        """
        Create a new ``Context`` named ``name``, with ``aliases``.

        ``name`` is optional, and should be a string if given. It's used to
        tell Context objects apart, and for use in a Parser when determining
        what chunk of input might belong to a given Context.

        ``aliases`` is also optional and should be an iterable containing
        strings. Parsing will honor any aliases when trying to "find" a given
        context in its input.
        """
        self.args = []
        self.name = name
        self.aliases = aliases

    def __str__(self):
        aliases = (" (%s)" % ', '.join(self.aliases)) if self.aliases else ""
        name = (" %s%s" % (self.name, aliases)) if self.name else ""
        return "Context%s: %r" % (name, self.args)

    def add_arg(self, *args, **kwargs):
        """
        Adds given ``Argument`` (or constructor args for one) to this context.
        """
        # Normalize
        if len(args) == 1 and isinstance(args[0], Argument):
            arg = args[0]
        else:
            arg = Argument(*args, **kwargs)
        # Test
        for name in arg.names:
            if self.has_arg(name):
                msg = "Tried to add an argument named %r but one already exists!"
                raise ValueError(msg % name)
        # Add
        self.args.append(arg)

    def has_arg(self, arg):
        """
        Is this string (``argv`` list member) a valid flag for this context?
        """
        # TODO: maybe just use a dict after all, same value multiple times
        # TODO: this is shitty/brittle/dumb
        try:
            return self.get_arg(arg) is not None
        except ValueError:
            return False

    def get_arg(self, arg):
        match = None
        for argument in self.args:
            if argument.answers_to(arg):
                match = argument
                break
        if match is not None:
            return match
        else:
            raise ValueError, "Argument %r not found" % arg

    def needs_value(self, arg):
        return self.get_arg(arg).needs_value


