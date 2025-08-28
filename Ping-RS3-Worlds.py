import subprocess
import platform
import re


valid_worlds = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,91,92,94,96,97,98,99,100,101,102,103,104,105,106,108,114,115,116,117,118,119,120,121,122,123,124,134,135,136,137,138,139,140,141,142,144,145,176,177,178,179,180,181,182,183,184,185,200,201,202,203,204,205,206,207,210,211,212,213,214,215,216,217,218,219,220,221,225,226,227,228,229,235,236,237,238,239,245,246,247,249,250,251,252,255,256,257,258,259
)

def ping_count():
    try:
        count = int(input("How many times would you like to ping each server?: "))
        return count
    except ValueError:
        print("Invalid input. Please enter a number")
        pass
    
def ping_world(world,count):
    host = f"world{world}.runescape.com"
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    print(f"Pinging world {world}...")
    result = subprocess.run(
        ["ping", count_flag, str(count), host],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None  # unreachable

    output = result.stdout

    if platform.system().lower() == "windows":
        match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", output)
        if match:
            return {"min": int(match.group(1)),
                    "max": int(match.group(2)),
                    "avg": int(match.group(3))}
    else:
        match = re.search(r"rtt min/avg/max/\w+ = ([\d.]+)/([\d.]+)/([\d.]+)/", output)
        if match:
            return {"min": float(match.group(1)),
                    "avg": float(match.group(2)),
                    "max": float(match.group(3))}

    return None


def pingall(valid_worlds):
    results = {}
    count = ping_count()
    for world in valid_worlds:
        results[world] = ping_world(world,count)
    return results


def menu():
    world_choice = input("Enter world number to ping, or 'a' to ping all worlds. 'x' to exit: ")

    # Special cases
    if world_choice.lower() == "a":
        ping_results = pingall(valid_worlds)
        print_results(ping_results)
        return True

    if world_choice.lower() == "x":
        return False
    
    try:
        world = int(world_choice)

        if world < 1 or world > 259:
            print("World must be between 1 and 259")
            return True

        else:
            stats = ping_world(world,ping_count())
            print_results({world: stats})  
            return True

    except ValueError:
        print("Invalid input. Please enter a number, 'a', or 'x'.")
        return True


def print_results(results):
    print("\nWorld | Min | Avg | Max")
    print("-" * 25)
    for world, stats in results.items():
        if stats:
            print(f"{world:<5} | {stats['min']:<3} | {stats['avg']:<3} | {stats['max']:<3}")
        else:
            print(f"{world:<5} | unreachable")


# How I found list of valid worlds:
# def find_reachable(start=1, end=259):
#     reachable = []
#     for world in range(start, end + 1):
#         print(f"Checking world {world}...")
#         if ping_world(world):
#             reachable.append(world)
#     return reachable


# def check_valid():
#     valid_worlds = find_reachable(1, 259)
#     print(valid_worlds)
#     print(f"There are {len(valid_worlds)} valid worlds.")
        

while menu():
    pass
