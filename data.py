import os
import hashlib

GIT_DIR = ".pygit"

def init():
    dirs = [GIT_DIR, f"{GIT_DIR}/objects", f"{GIT_DIR}/refs/heads"]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
    
    with open(f"{GIT_DIR}/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")

def hash_object(data, type="blob"):
    # We add a small header so we know what kind of object it is later
    obj = f"{type} {len(data)}\n".encode() + data
    sha1 = hashlib.sha1(obj).hexdigest()
    
    path = os.path.join(GIT_DIR, "objects", sha1)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(obj)
    return sha1

def get_object(sha1):
    # This reads an object back from the 'database'
    path = os.path.join(GIT_DIR, "objects", sha1)
    with open(path, "rb") as f:
        return f.read()

def update_ref(ref, sha1):
    # Updates a branch (like main) to point to a new hash
    ref_path = os.path.join(GIT_DIR, ref)
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(ref_path, "w") as f:
        f.write(sha1)

def get_ref(ref):
    ref_path = os.path.join(GIT_DIR, ref)
    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            return f.read().strip()
    return None