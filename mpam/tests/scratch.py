import argparse
import warnings

from typing import Any, Callable, Optional, Union, Type

def create_deprecated_action_class(original_action_class: Type[argparse.Action], warning_message: Optional[str]) -> Type[argparse.Action]:
    def deprecated_call(self, parser: argparse.ArgumentParser,   # type: ignore[no-untyped-def] 
                        namespace: argparse.Namespace,
                        values: Any, 
                        option_string: Optional[str] = None) -> None:
        if warning_message:
            warnings.warn(warning_message, DeprecationWarning)
        super(type(self), self).__call__(parser, namespace, values, option_string)

    return type("DeprecatedSubAction", (original_action_class,), {"__call__": deprecated_call})

class DeprecatedAction(argparse.Action):
    def __init__(self, *args: Any, warning_message: Optional[str] = None, **kwargs: Any) -> None:
        self.warning_message = warning_message
        original_action = kwargs.get('action', None)

        # Get the original action class
        if isinstance(original_action, str):
            original_action_class = parser._registries['action'][original_action]
        elif original_action is None:
            original_action_class = argparse.Action
        else:
            original_action_class = original_action

        self.DeprecatedSubAction = create_deprecated_action_class(original_action_class, self.warning_message)

        super().__init__(*args, **kwargs)

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Any, option_string: Optional[str] = None) -> None:
        deprecated_action_instance = self.DeprecatedSubAction(option_strings=self.option_strings,
                                                              dest=self.dest,
                                                              nargs=self.nargs,
                                                              const=self.const,
                                                              default=self.default,
                                                              type=self.type,
                                                              choices=self.choices,
                                                              required=self.required,
                                                              help=self.help,
                                                              metavar=self.metavar)
        deprecated_action_instance(parser, namespace, values, option_string)

# Example usage
parser = argparse.ArgumentParser()

# Deprecated argument
parser.add_argument(
    "--old_arg",
    action=DeprecatedAction,
    original_action='store_const',
    const=42,
    warning_message="The --old_arg option is deprecated.",
    help="Old argument (deprecated)"
)

# Regular argument
parser.add_argument("--new_arg", help="New argument")

args = parser.parse_args()

print(args)
