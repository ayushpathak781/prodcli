# prodcli
Productivity CLI: TODOs, Focus Timer, and Git Wrapper in Python

# ProdCLI — Lightweight Productivity CLI

ProdCLI is a small, single-file command-line productivity toolkit written in Python. It bundles a **TODO manager**, a **Focus (Pomodoro) timer**, and a **lightweight git wrapper** to speed up daily developer workflows.

## 🚀 Features
- **`todo`** — add/list/complete/remove tasks; stored in `~/.prodcli/todo.json`.
- **`focus`** — start a Pomodoro-style timer with customizable durations and cycles.
- **`gitwrap`** — quick git helpers: status, commit with template, and optional push.

## 📦 Installation
Clone the repository and make the script executable:
```bash
git clone https://github.com/ayushpathak781/prodcli.git
cd prodcli
chmod +x prodcli.py
```
Run directly:
```bash
python prodcli.py --help
```

## ⚡ Usage Examples
### TODO Manager
```bash
python prodcli.py todo add "Write project plan"
python prodcli.py todo list
python prodcli.py todo done <task-id>
python prodcli.py todo remove <task-id>
```

### Focus Timer (25/5 Pomodoro, 4 cycles)
```bash
python prodcli.py focus start --work 25 --break 5 --cycles 4
```

### Git Wrapper
```bash
python prodcli.py gitwrap status
python prodcli.py gitwrap commit "Fix bug" --push
```

## 🛠 Project Structure
```
prodcli/
  ├── prodcli.py
  ├── README.md
  ├── LICENSE
  ├── .gitignore
  └── .github/workflows/ci.yml (optional)
```

## 📤 How to Upload to GitHub Professionally
1. Initialize git and commit:
```bash
git init
git add .
git commit -m "chore: initial commit — ProdCLI CLI tool"
```
2. Create a GitHub repository and push:
```bash
gh repo create your-username/prodcli --public --source=. --remote=origin --push
```
3. Add a release/tag:
```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```
4. Add CI workflows, badges, and a demo GIF (record terminal demo with asciinema).

## 🤝 Contributing
PRs welcome! Please:
- Keep changes small.
- Include tests.
- Write clear commit messages.

## 📄 License
Apache License. See [LICENSE](./LICENSE) for details.

---

✨ *ProdCLI is perfect as a showcase repo: simple, useful, and a reflection of clean coding practices.*
