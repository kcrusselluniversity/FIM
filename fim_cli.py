import argparse
import json
import os

CONFIG_FILE = "fim_config.json"

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"files": []}

# Save configuration
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Add a file to monitor
def add_file(file_path, rule, authorized_users=None):
    config = load_config()
    for entry in config["files"]:
        if entry["path"] == file_path:
            print("File already monitored.")
            return
    entry = {"path": file_path, "rule": rule}
    if rule == 1:
        entry["authorized_users"] = authorized_users or []
    config["files"].append(entry)
    save_config(config)
    print("File added for monitoring.")

# Remove a file from monitoring
def remove_file(file_path):
    config = load_config()
    config["files"] = [f for f in config["files"] if f["path"] != file_path]
    save_config(config)
    print("File removed from monitoring.")

# View monitored files
def view_files():
    config = load_config()
    if not config["files"]:
        print("No files are currently being monitored.")
    else:
        for entry in config["files"]:
            print(entry)

# Print the log
def print_log():
    if os.path.exists("fim_log.txt"):
        with open("fim_log.txt", "r") as f:
            print(f.read())
    else:
        print("No logs available.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Integrity Monitor CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("file_path", help="Path to the file to monitor")
    add_parser.add_argument("rule", type=int, help="Rule to apply (1: Authorized users, 2: No changes, 3: Business hours)")
    add_parser.add_argument("--users", nargs="*", help="Authorized users (for Rule 1)")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("file_path", help="Path to the file to remove from monitoring")

    view_parser = subparsers.add_parser("view", help="View monitored files")

    log_parser = subparsers.add_parser("log", help="Print the monitoring log")

    args = parser.parse_args()

    if args.command == "add":
        add_file(args.file_path, args.rule, args.users)
    elif args.command == "remove":
        remove_file(args.file_path)
    elif args.command == "view":
        view_files()
    elif args.command == "log":
        print_log()
    else:
        parser.print_help()