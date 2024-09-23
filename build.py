import ftplib
import subprocess

import requests

from ftpconfig import HOST, USER, PASSWORD
from rewlis import *
from rewlis.entity import *


def directory_exists(ftp, folder):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for file in filelist:
        if file.split()[-1] == folder and file.upper().startswith('D'):
            return True
    return False


build = "build.bat"
subprocess.call([build], shell=False)

latest = "latest.txt"
version = "v" + VERSION

with open(latest, mode="w") as f:
    f.write(version + "\n")

print(f"Connecting to server '{HOST}'...")
session = ftplib.FTP(HOST, USER, PASSWORD)

print(f"Creating folder {version}...")
if directory_exists(session, version) is False:
    session.mkd(version)

resp = requests.get(
    "https://github.com/xayam/rewlis/archive/refs/heads/main.zip",
    timeout=3,
    verify=False,
    headers={
        "User-Agent":
            r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) " +
            "Gecko/20100101 Firefox/96.0",
        "Content-type": "application/x-www-form-urlencoded"
    })
if resp.status_code == 200:
    with open(f"dist/{APP_CLIENT.lower()}-src.zip", mode="wb") as f:
        f.write(resp.content)
    with open(f"dist/{APP_CLIENT.lower()}-src.zip", mode="rb") as f:
        print(f"Uploading {version}/{APP_CLIENT.lower()}-src-{version}.zip...")
        session.storbinary(
            f"STOR {version}/{APP_CLIENT.lower()}-src-{version}.zip", f)
else:
    print(f"WARNING: resp.StatusCode={resp.status_code}")

print(f"Uploading {version}/rewlis_client-{version}.exe...")
with open("dist/rewlis_client.exe", mode="rb") as f:
    session.storbinary(
        f"STOR {version}/{APP_CLIENT.lower()}-x64-{version}.exe", f)

print(f"Uploading {version}/rewlis_creator-{version}.exe...")
with open("dist/rewlis_creator.exe", mode="rb") as f:
    session.storbinary(
        f"STOR {version}/{APP_CREATOR.lower()}-x64-{version}.exe", f)

print(f"Uploading latest/{latest}...")
with open(latest, mode="rb") as f:
    session.storbinary(f"STOR latest/{latest}", f)

session.quit()
