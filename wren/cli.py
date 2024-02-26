#!/usr/bin/env python3

import os
import argparse
import subprocess
from random import choice
from wren.core import (
    create_new_task,
    get_summary,
    get_task_content,
    get_task_file,
    get_tasks,
    mark_task_done,
    mark_task_postponed,
    mark_task_todo,
    mark_task_cancelled,
    notes_dir,
    postponed_dir,
    cancelled_dir,
    done_dir,
    config_file,
    data_dir,
    __version__,
)

editor = os.environ.get("EDITOR", "vi")


def create_file(name):
    filename = create_new_task(name)
    print("created task:", filename)


def list_files(dir: str, bullet='➜', s=""):
    tasks = get_tasks(dir)
    print("".join(map(lambda t: bullet + " " + t + "\n", tasks))[:-1])


def print_random():
    tasks = get_tasks(notes_dir, "")
    print(choice(tasks))


def print_summary():
    summary = get_summary()
    print(summary)


def edit_content(name):
    found, filename = get_task_file(name, notes_dir)
    if found:
        filepath = os.path.join(notes_dir, filename)
        subprocess.run([editor, filepath])


def read_content(name):
    content = get_task_content(name)
    print(content)


def mark_done(name):
    message = mark_task_done(name)
    print(message)

def mark_postponed(name):
    message = mark_task_postponed(name)
    print(message)

def mark_todo(name):
    message = mark_task_todo(name)
    print(message)


def mark_cancelled(name):
    message = mark_task_cancelled(name)
    print(message)

def flat_map_args(args: list) -> str:
    return " ".join(args).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="*", help="a new task to be created")
    parser.add_argument(
        "-l",
        "--ls",
        "--list",
        type=str,
        help="List all current tasks. Add -d/-c/-p to list done, cancelled or postponed tasks",
        nargs="?",
        const="",
        default=None,
    )
    parser.add_argument(
        "-d", "--done", metavar="foo", type=str, nargs="+", help="Mark a task as done"
    )
    parser.add_argument(
        "-p", "--postpone", metavar="foo", type=str, nargs="+", help="Postpone a task for the time being"
    )
    parser.add_argument(
        "-t", "--todo", metavar="foo", type=str, nargs="+", help="Move a postponed task to current"
    )
    parser.add_argument(
        "-c", "--cancel", metavar="foo", type=str, nargs="+", help="Mark a postponed task as canceled"
    )
    parser.add_argument(
        "-r", "--read", metavar="foo", nargs="+", type=str, help="Read a task content"
    )
    parser.add_argument(
        "-e", "--edit", metavar="foo", nargs="+", type=str, help="Edit a task content"
    )
    parser.add_argument(
        "-o", "--one", action="store_true", help="Print one random task"
    )
    parser.add_argument(
        "-s", "--summary", action="store_true", help="Generate a summary"
    )
    parser.add_argument("--telegram", action="store_true", help="Start Telegram bot")
    parser.add_argument("--http", action="store_true", help="Start HTTP server")
    parser.add_argument("--version", action="store_true", help="Show Wren version")

    args = parser.parse_args()

    if args.ls != None and args.postpone != None:
        list_files(postponed_dir, bullet="?")
    elif args.ls != None and args.cancel != None:
        list_files(cancelled_dir, bullet="✘")
    elif args.ls != None and args.done != None:
        list_files(done_dir, bullet="✔")
    elif args.ls != None:
        list_files(notes_dir)
    elif args.version:
        print("Wren " + __version__)
        print("\nconfig: " + config_file)
        print("data directory: " + data_dir)
    elif args.http:
        from wren.http_server import start_server

        start_server()
    elif args.telegram:
        from wren.telegram import start_bot

        start_bot()
    elif args.one:
        print_random()
    elif args.edit:
        edit_content(flat_map_args(args.edit))
    elif args.summary:
        print_summary()
    elif args.read:
        read_content(flat_map_args(args.read))
    elif args.done:
        mark_done(flat_map_args(args.done))
    elif args.postpone:
        mark_postponed(flat_map_args(args.postpone))
    elif args.todo:
        mark_todo(flat_map_args(args.todo))
    elif args.cancel:
        mark_cancelled(flat_map_args(args.cancel))
    else:
        if args.task:
            create_file(" ".join(args.task))
        else:
            list_files(notes_dir)


if __name__ == "__main__":
    main()
