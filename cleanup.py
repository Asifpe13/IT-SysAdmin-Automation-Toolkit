import os
import shutil

TARGET_DIRS = ["hardware_audit", "onboarding_script", "uptime_monitor"]
DIRS_TO_DELETE = {"build", "__pycache__"}
SPEC_SUFFIX = ".spec"


def delete_dir(path: str):
    """Delete a directory tree if it exists, printing the action."""
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Deleted directory: {path}")


def delete_file(path: str):
    """Delete a file if it exists, printing the action."""
    if os.path.isfile(path):
        os.remove(path)
        print(f"Deleted file: {path}")


def clean_target(base_dir: str):
    """Clean PyInstaller artifacts under a specific target directory."""
    for root, dirs, files in os.walk(base_dir, topdown=True):
        # Safety: never delete or descend into dist/
        dirs[:] = [d for d in dirs if d != "dist"]

        # Delete build/__pycache__ dirs
        for d in list(dirs):
            if d in DIRS_TO_DELETE:
                delete_dir(os.path.join(root, d))

        # Delete *.spec files
        for f in files:
            if f.endswith(SPEC_SUFFIX):
                delete_file(os.path.join(root, f))


def main():
    for rel in TARGET_DIRS:
        if os.path.isdir(rel):
            clean_target(rel)
        else:
            print(f"Skipping missing directory: {rel}")


if __name__ == "__main__":
    main()

