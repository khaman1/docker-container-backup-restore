import os
import platform
from subprocess import check_output
from datetime import datetime
######################################################
######################################################
date_to_restore = '19052021-141415'

db_container_name = 'db'
web_container_name = 'web'
######################################################
######################################################
system = platform.system()

if system == 'Windows':
    root_dir = os.getcwd().split('\\')[-2]
    extract_cmd = 'type'
else:
    root_dir = os.getcwd().split('/')[-2]
    extract_cmd = 'cat'

root_dir = root_dir.lower()
backup_dir = date_to_restore.split('-')[0]
######################################################
######################################################
os.chdir('..')
os.system('docker-compose stop')
print("Stopped services ...")
os.chdir('backup/'+backup_dir)
print("Doing restore ...")
######################################################
######################################################


def restore(filename):
    args = [
        extract_cmd,
        filename + '-volume-' + date_to_restore + '.tar.bz2 |',
        'docker run -i -v',
        root_dir + '_odoo-'+filename+'-data:/volume',
        '--rm loomchild/volume-backup',
        'restore -f -',
    ]

    print(' '.join(args))

    check_output(' '.join(args), shell=True)


######################################################
######################################################
print("db ...")
restore(db_name)
print("web ...")
restore(web_name)
######################################################
######################################################
os.chdir('..')
os.chdir('..')
os.system('docker-compose up -d')
print("DONE!!!")
