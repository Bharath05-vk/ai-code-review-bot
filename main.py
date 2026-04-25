"""AI Code Review Bot - entrypoint

This is a minimal starter script. Replace with your application's logic.
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Review Bot")
    parser.add_argument("--version", action="store_true", help="show version")
    args = parser.parse_args()
    if args.version:
        print("AI-CODE-REVIEW-BOT version 0.1")
    else:
        print("AI Code Review Bot running. Replace main() with real logic.")


if __name__ == "__main__":
    main()
