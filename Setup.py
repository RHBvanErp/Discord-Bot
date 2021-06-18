import os
 
def windowsSetup():
    pkgs = ["curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py", 
    "python get-pip.py", "pip install discord.py", "pip install discord.py[voice]", "pip install requests", 
    "pip install times", "pip install youtube_dl"]
 
    for pkg in pkgs:
        os.system(pkg)
 
        returned_value = os.system(pkg)
        print('returned value:', returned_value)

def linuxSetup():
    pkgs = ["sudo apt install python3-pip", "pip install discord.py", "pip install discord.py[voice]", 
    "pip install requests", "pip install times", "pip install youtube_dl", "sudo apt install ffmpeg"]
 
    for pkg in pkgs:
        os.system(pkg)
 
        returned_value = os.system(pkg)
        print('returned value:', returned_value)
 
def failSafe():
    operatingSystem = input("Are you using Windows or Linux? W/L ")
    if operatingSystem == "w" or operatingSystem == "W":
        windowsSetup()
    elif operatingSystem == "l" or operatingSystem == "L":
        linuxSetup()
    else:
        print("This is not a valid input, try again.")
        failSafe()
 
failSafe()
input("Press any key to exit")