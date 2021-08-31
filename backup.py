import os
import platform
from subprocess import check_output
from datetime import datetime

######################################################
######################################################
container_name = 'web-data'

db_container_name = 'db'
web_container_name = 'web'
######################################################
######################################################
system = platform.system()

if system == 'Windows':
    root_dir = os.getcwd().split('\\')[-2]
else:
    root_dir = os.getcwd().split('/')[-2]

root_dir = root_dir.lower()
current_time = datetime.now().strftime('%d%m%Y-%H%M%S')
backup_dir = current_time.split('-')[0]
######################################################
######################################################
os.chdir('../')
os.system('docker-compose stop')
print("Stopped services ...")
os.chdir('backup/')
print("Doing backup ...")
######################################################
######################################################
try:
    os.mkdir(backup_dir)
except:
    pass


def backup(filename):
    args = [
        'docker run -v',
        root_dir + _container_name + ':/volume',
        '--rm loomchild/volume-backup ',
        'backup - >',
        '"' + backup_dir + '/' + filename +
        '-volume-' + current_time + '.tar.bz2' + '"',
    ]

    #print(' '.join(args))

    check_output(' '.join(args), shell=True)


######################################################
######################################################
print("db ...")
backup(db_name)
print("web ...")
backup(web_name)
print("Restarting services ...")
######################################################
######################################################
# os.chdir('../../..')
os.system('docker-compose up -d')
print("DONE!!!")
