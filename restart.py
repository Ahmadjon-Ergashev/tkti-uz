import argparse
import subprocess

desc = """
    restart and delete 
"""
parser = argparse.ArgumentParser(description=desc)

def Main():
    parser.add_argument('-r', '--restart', type=str, required=False, help='restart docker project')
    parser.add_argument('-p', '--prune', type=str, required=False, help='prune all containers and images')
    args = parser.parse_args()
    if args.restart:
        subprocess.call(["sudo", "docker", "container", "restart", "tkti_web"])
    elif args.prune:
        subprocess.call(["sudo", "docker", "container", "stop", "tkti_web"])
        subprocess.call(["sudo", "docker", "container", "prune"])
        subprocess.call(["sudo", "docker", "system", "prune"])
        volumes = subprocess.check_output(["sudo", "docker", "volume", "ls"])
        print(volumes)
        volume_name = input("enter volume name: ")
        subprocess.call(["sudo", "docker", "volume", "rm", volume_name])
        subprocess.call(["sudo", "docker", "compose", "up", "-d", "--build"])
    else:
        subprocess.call(["python3", "restart.py", "--help"])
Main()