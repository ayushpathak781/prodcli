import argparse
import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / '.prodcli'
TODO_FILE = CONFIG_DIR / 'todo.json'


def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not TODO_FILE.exists():
        TODO_FILE.write_text(json.dumps({'tasks': []}, indent=2))


def load_todo():
    ensure_config()
    with open(TODO_FILE, 'r') as f:
        return json.load(f)


def save_todo(data):
    ensure_config()
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def now_str():
    return datetime.now().isoformat(timespec='seconds')

# -------------------- TODO subcommands --------------------

def todo_add(args):
    data = load_todo()
    task = {
        'id': int(time.time()),
        'title': args.title,
        'created_at': now_str(),
        'done': False
    }
    data['tasks'].append(task)
    save_todo(data)
    print(f"Added: [{task['id']}] {task['title']}")


def todo_list(args):
    data = load_todo()
    tasks = data.get('tasks', [])
    if not tasks:
        print('No tasks.')
        return
    for i, t in enumerate(tasks, start=1):
        status = '✔' if t.get('done') else '✖'
        print(f"{i}. {status} {t['title']} (id:{t['id']})")


def todo_done(args):
    data = load_todo()
    tasks = data.get('tasks', [])
    found = False
    for t in tasks:
        if str(t['id']) == str(args.id) or (args.index and tasks.index(t)+1 == args.index):
            t['done'] = True
            t['completed_at'] = now_str()
            found = True
            print(f"Marked done: {t['title']}")
            break
    if not found:
        print('Task not found (use `todo list` to see ids).')
    save_todo(data)


def todo_remove(args):
    data = load_todo()
    tasks = data.get('tasks', [])
    original_len = len(tasks)
    tasks = [t for t in tasks if not (str(t['id']) == str(args.id) or (args.index and tasks.index(t)+1 == args.index))]
    data['tasks'] = tasks
    save_todo(data)
    if len(tasks) < original_len:
        print('Task removed.')
    else:
        print('No matching task found.')

# -------------------- Focus timer --------------------

def focus_start(args):
    work = int(args.work) * 60
    brk = int(args.break_) * 60
    cycles = int(args.cycles)
    try:
        for cycle in range(1, cycles+1):
            print(f"Cycle {cycle}/{cycles}: Work for {args.work} minutes — starts now.")
            countdown(work)
            notify(f"Work session {cycle}/{cycles} complete. Time for a break!")
            if cycle < cycles:
                print(f"Break for {args.break_} minutes — starts now.")
                countdown(brk)
                notify(f"Break {cycle}/{cycles} over. Back to work!")
        print('All cycles complete. Great job!')
        notify('All focus cycles complete. Good work!')
    except KeyboardInterrupt:
        print('\nFocus timer interrupted.')


def countdown(seconds):
    try:
        while seconds:
            m, s = divmod(seconds, 60)
            print(f"\r{m:02d}:{s:02d}", end='')
            time.sleep(1)
            seconds -= 1
        print('\r00:00')
    except KeyboardInterrupt:
        raise


def notify(message):
    # Attempt cross-platform notification: macOS `osascript`, Linux `notify-send`, fallback to print
    try:
        if sys.platform == 'darwin':
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "ProdCLI"'])
        elif sys.platform.startswith('linux'):
            subprocess.run(['notify-send', 'ProdCLI', message])
        else:
            print('\n[NOTIFY]', message)
    except Exception:
        print('\n[NOTIFY]', message)

# -------------------- Git wrapper --------------------

def git_status(args):
    subprocess.run(['git', 'status'])


def git_commit(args):
    msg = args.message
    if args.template:
        msg = args.template.replace('{msg}', msg)
    subprocess.run(['git', 'add', '-A'])
    subprocess.run(['git', 'commit', '-m', msg])
    if args.push:
        subprocess.run(['git', 'push'])

# -------------------- CLI wiring --------------------

def build_parser():
    parser = argparse.ArgumentParser(prog='prodcli', description='ProdCLI — productivity toolkit')
    sub = parser.add_subparsers(dest='cmd')

    # TODO commands
    todo_p = sub.add_parser('todo', help='Todo manager')
    todo_sub = todo_p.add_subparsers(dest='sub')
    p_add = todo_sub.add_parser('add', help='Add a task')
    p_add.add_argument('title', help='Task title')
    p_add.set_defaults(func=todo_add)

    p_list = todo_sub.add_parser('list', help='List tasks')
    p_list.set_defaults(func=todo_list)

    p_done = todo_sub.add_parser('done', help='Mark task done')
    p_done.add_argument('id', nargs='?', help='Task id')
    p_done.add_argument('--index', type=int, help='List index (1-based)')
    p_done.set_defaults(func=todo_done)

    p_remove = todo_sub.add_parser('remove', help='Remove task')
    p_remove.add_argument('id', nargs='?', help='Task id')
    p_remove.add_argument('--index', type=int, help='List index (1-based)')
    p_remove.set_defaults(func=todo_remove)

    # Focus commands
    focus_p = sub.add_parser('focus', help='Focus timer (pomodoro)')
    focus_sub = focus_p.add_subparsers(dest='sub')
    p_start = focus_sub.add_parser('start', help='Start timer')
    p_start.add_argument('--work', default=25, help='Work minutes (default 25)')
    p_start.add_argument('--break', dest='break_', default=5, help='Break minutes (default 5)')
    p_start.add_argument('--cycles', default=4, help='Number of cycles (default 4)')
    p_start.set_defaults(func=focus_start)

    # Git wrapper
    git_p = sub.add_parser('gitwrap', help='Small git helpers')
    git_sub = git_p.add_subparsers(dest='sub')
    g_status = git_sub.add_parser('status')
    g_status.set_defaults(func=git_status)
    g_commit = git_sub.add_parser('commit')
    g_commit.add_argument('message', help='Commit message')
    g_commit.add_argument('--push', action='store_true', help='Push after commit')
    g_commit.add_argument('--template', help='Commit message template, use {msg} for message')
    g_commit.set_defaults(func=git_commit)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        parser.print_help()
        return 1
    try:
        args.func(args)
    except Exception as e:
        print('Error:', e)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
