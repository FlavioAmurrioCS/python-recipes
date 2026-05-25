from __future__ import annotations

import argparse
import logging
from textwrap import dedent
from typing import TYPE_CHECKING
from typing import NamedTuple

if TYPE_CHECKING:
    from typing_extensions import Protocol

    class Cmd(Protocol):
        @classmethod
        def arg_parser(
            cls, parser: argparse.ArgumentParser | None = None
        ) -> argparse.ArgumentParser: ...
        def run(self) -> int: ...


logger = logging.getLogger(__name__)


class SampleCmd(NamedTuple):
    """<Brief description of the command>."""

    @classmethod
    def arg_parser(cls, parser: argparse.ArgumentParser | None = None) -> argparse.ArgumentParser:
        parser = parser or argparse.ArgumentParser()
        parser.description = cls.__doc__ or "<PLACEHOLDER_DESCRIPTION>"
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.epilog = dedent("""\
        Example:
          %(prog)s <PLACEHOLDER_EXAMPLE>
        """)
        return parser

    def run(self) -> int:
        print(f"Executing {self}...")
        return 0


################################################################################
# endregion: Commands
################################################################################

SUB_COMMANDS: dict[str, type[Cmd]] = {
    "hello": SampleCmd,
    "bye": SampleCmd,
}

VERSION = "0.1.0"


def main(argv: list[str] | tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.description = "CLI Example with subcommands"
    parser.formatter_class = lambda prog: argparse.HelpFormatter(prog, max_help_position=27)
    parser.epilog = dedent("""\
    Example:
      %(prog)s hello
    """)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity level."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command")
    for cmd_name, cmd in SUB_COMMANDS.items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd.__doc__ or None)
        cmd.arg_parser(cmd_parser)
    args = parser.parse_args(argv)
    command: str | None = args.command
    verbose: int = args.verbose
    if command is None:
        # NOTE: You can also set a default command here if desired
        parser.print_help()
        return 1
    logging.basicConfig(
        level=logging.WARNING - (verbose * 10),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    cls = SUB_COMMANDS[command]

    excluded_args = ("command", "verbose")
    cmd_instance = cls(**{k: v for k, v in vars(args).items() if k not in excluded_args})
    return cmd_instance.run()


if __name__ == "__main__":
    raise SystemExit(main())
