import sys
import data
import base

def main():
    if len(sys.argv) < 2:
        print("Usage: python vcs.py [init|add|commit] [args]")
        return

    command = sys.argv[1]

    if command == "init":
        data.init()
        print("Initialized pygit")
    
    elif command == "log":
        base.get_log()
        
    elif command == "add":
        base.add(sys.argv[2])
        print(f"Added {sys.argv[2]}")
        
    elif command == "commit":
        sha = base.commit(sys.argv[2])
        print(f"Committed: {sha}")

if __name__ == "__main__":
    main()