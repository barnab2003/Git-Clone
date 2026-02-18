# pygit: A Minimalist Version Control System in Python

**pygit** is a functional, content-addressable version control system built from scratch. It replicates the core architecture of Git, including a content-addressable filesystem, staging area (index), and commit history.

##  Features

* **Initialization**: Setup a hidden storage database (`.pygit`).
* **Hashing & Storage**: Content-addressable storage using SHA-1 hashing.
* **Staging Area**: An index file to track changes before they are committed.
* **Commit System**: Snapshots of the entire project with author metadata and parent-linking.
* **Time Travel**: A functional `checkout` command to restore files from any point in history.
* **Logs**: View the historical chain of commits.

##  Tech Stack

* **Language**: Python 3.x
* **Libraries**: `os`, `hashlib`, `sys`, `time`

##  Project Structure

```text
pygit/
├── main.py          # Command-line interface and entry point
├── base.py          # High-level logic (Commit, Add, Checkout)
├── data.py          # Low-level storage (Hashing, Objects, Refs)
└── .pygit/          # Internal database (Generated after 'init')

```

##  Usage

### 1. Initialize the repository

```bash
python main.py init

```

### 2. Stage a file

```bash
python main.py add example.txt

```

### 3. Create a snapshot

```bash
python main.py commit "My first version"

```

### 4. View history

```bash
python main.py log

```

### 5. Restore a version

```bash
python main.py checkout <commit-hash>

```

---

##  What I Learned

Building this project was a "rite of passage" for me as a CSE student. Key takeaways included:

* Understanding how Git isn't just a "backup tool," but a **Directed Acyclic Graph (DAG)** of snapshots.
* Deep diving into **Content-Addressable Storage**—where the filename is the hash of the content.
* Implementing **modular architecture** in Python to separate storage logic from user interface.

## Contributing

This is an educational project. Feel free to fork it and add features like branching or diffing!


