import os
import time
from pathlib import Path

# move this script to instances folder

def root_dir(path:str):
    p = Path(path)
    if p.is_absolute():
        return p.parts[1] if len(p.parts) > 1 else p.parts[0]
    return p.parts[0] if p.parts else ""

options_dirs = []
root_dirs = [name for name in os.listdir(".") if os.path.isdir(os.path.join(".", name))]
for root in root_dirs:
    temp_path = f"./{root}/minecraft/options.txt"
    if os.path.exists(temp_path):
        print("fonud it!", f"in {temp_path}")
        options_dirs.append(str(temp_path))

last_update = ""
for opt in range(len(options_dirs)-1):
    if os.path.getmtime(options_dirs[opt]) < os.path.getmtime(options_dirs[opt+1]):
        last_update = options_dirs[opt+1]
    else:
        last_update = options_dirs[opt]
print("\nLast updated config is", root_dir(last_update),"\n")

picked_opts_file_num = -1
while picked_opts_file_num < 0:
    print("Choose file for sync:")
    print(f"    Last updated config [0]")
    for i in range(len(options_dirs)):
        print(f"    {root_dir(options_dirs[i])} [{i+1}]")
    try:
        picked_opts_file_num = int(input("Your choose: ")) 
        print()
    except ValueError:
        print("Do write number.")
    except KeyboardInterrupt:
        print("SU later...")
        exit()
    if picked_opts_file_num == 0:
        picked_opts_file = last_update
    elif picked_opts_file_num > 0:
        picked_opts_file = options_dirs[picked_opts_file_num-1]
    else:
        print("This is not possible...\n")
print("\n------You chosen:", picked_opts_file,"------\n")

options_dirs.remove(picked_opts_file)
options_dirs.append(picked_opts_file)

with open(picked_opts_file) as f:
    content = f.read()
    f.close()

if not os.path.exists("./options_backup.txt"):
    print("options backup file not found, creating...")

with open("./options_backup.txt", "w") as f:
    f.write(content)
    f.close()
print("Backup saved!","From",root_dir(picked_opts_file),"version!")

print("refreshing all options...")
for options_dir in options_dirs:
    with open(options_dir, "w") as f:
        f.write(content)
        f.close()
    print("yep..")
    time.sleep(0.2)

print("\nDone!")







