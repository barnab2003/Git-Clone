import os
import data
import time

def add(filename):
    with open(filename, "rb") as f:
        data_bytes = f.read()
    
    sha1 = data.hash_object(data_bytes, type="blob")
    
    # Update the index
    with open(".pygit/index", "a") as f:
        f.write(f"{sha1} {filename}\n")

def commit(message):
    index_path = ".pygit/index"
    if not os.path.exists(index_path):
        return "Nothing to commit"

    with open(index_path, "r") as f:
        index_content = f.read()

    # Create Tree
    tree_sha = data.hash_object(index_content.encode(), type="tree")

    # Get Parent from HEAD
    with open(".pygit/HEAD", "r") as f:
        ref = f.read().strip().split(": ")[1]
    
    parent = data.get_ref(ref)

    # Build Commit Object
    commit_data = f"tree {tree_sha}\n"
    if parent:
        commit_data += f"parent {parent}\n"
    commit_data += f"author Barnab Barman\n"
    commit_data += f"date {int(time.time())}\n\n"
    commit_data += message + "\n"

    commit_sha = data.hash_object(commit_data.encode(), type="commit")
    
    # Update the branch pointer
    data.update_ref(ref, commit_sha)
    os.remove(index_path)
    
    return commit_sha

def get_log():
    # 1. Read HEAD to see which branch we're on
    with open(".pygit/HEAD", "r") as f:
        ref_path = f.read().strip().split(": ")[1]
    
    # 2. Get the hash of the latest commit on that branch
    current_hash = data.get_ref(ref_path)
    
    if not current_hash:
        print("No history found.")
        return

    # 3. Follow the chain of parent commits
    while current_hash:
        # Get the commit object's data (including header)
        obj_data = data.get_object(current_hash).decode()
        
        # Split the header from the content
        _, commit_content = obj_content = obj_data.split('\n', 1)

        print("-" * 50)
        print(f"commit {current_hash}")
        print(commit_content)

        # Look for a parent hash in the commit message
        parent_hash = None
        for line in commit_content.splitlines():
            if line.startswith("parent "):
                parent_hash = line.split(" ")[1]
                break
        
        current_hash = parent_hash

def checkout(commit_hash):
    # 1. Read the Commit object
    commit_data = data.get_object(commit_hash).decode()
    
    # 2. Find the Tree hash inside the commit
    tree_sha = None
    for line in commit_data.splitlines():
        if line.startswith("tree "):
            tree_sha = line.split(" ")[1]
            break
            
    if not tree_sha:
        print(f"Could not find tree for commit {commit_hash}")
        return

    # 3. Read the Tree object (which is our stored index content)
    tree_data = data.get_object(tree_sha).decode()
    
    # The tree_data looks like: "hash filename\nhash filename"
    # We ignore the header line (e.g., "tree 123")
    lines = tree_data.splitlines()[1:] 

    # 4. Restore the files
    for line in lines:
        if not line.strip(): continue
        sha, filename = line.split(" ", 1)
        
        # Get the file content (blob) from the objects folder
        blob_data = data.get_object(sha)
        
        # In our system, the blob data starts with a header like "blob 12\n"
        # We need to skip that header to get the real content
        _, real_content = blob_data.split(b"\n", 1)
        
        with open(filename, "wb") as f:
            f.write(real_content)
            
    print(f"Checked out commit {commit_hash}. Files restored.")