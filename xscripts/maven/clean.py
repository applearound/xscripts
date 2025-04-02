import os
import pathlib

def clean_m2():
    home_dir = pathlib.Path.home()
    # delete all empty directories under .m2/repository, ask before deleting
    for root, subdirs, files in os.walk(home_dir / ".m2" / "repository", topdown=False):
        if len(subdirs) != 0 or len(files) != 0:
            continue

        inp = input(f"delete {root}: (y/n)?")
        if inp.lower() == "y":
            os.rmdir(root)
            print(root, "deleted")
        else:
            print("skipping", root)
