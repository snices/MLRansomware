#Capstone MLRansomware
#Python3
import os;
check = input("Want to restart your computer ? (y/n): ");
if check == 'n':
    exit();
else:
    os.system("shutdown /r /t 1");
#best option rn but slow in terms of how fast ransomware works
