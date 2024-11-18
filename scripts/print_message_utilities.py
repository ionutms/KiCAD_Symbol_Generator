"""TODO"""

from colorama import init, Fore, Style
init(autoreset=True)


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print an info message in yellow."""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
