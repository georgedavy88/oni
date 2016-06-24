#!/usr/bin/env python
import os
import subprocess
import ConfigParser
import re
import commands

def applyconf(filename,conf):

    RE = '(('+'|'.join(conf.keys())+')\s*=)[^\r\n]*?(\r?\n|\r)'
    pat = re.compile(RE)

    def apply(var,cf = conf ):
        return cf[var.group(2)].join(var.group(1,3))

    with open(filename,'rb') as f:
        content = f.read()

    with open(filename,'wb') as f:
        f.write(pat.sub(apply,content))


node1 = 'mworker1'
node2 = 'mworker2'

print("--------- Initializing Setup.")
CONFIG = ConfigParser.ConfigParser()
CONFIG.read("oniconf.ini")
ONI_GROUP       = CONFIG.get("USER", "oni.group")
ONI_USERNAME    = CONFIG.get("USER", "oni.user")

CLUSTER_HOSTS   = CONFIG.get("ONI", "cluster.hosts").split(',')
ONI_OA          = CONFIG.get("OA", "oa.host")
ONI_MLMASTER    = CONFIG.get("ML", "ml.master")
ONI_INGEST      = CONFIG.get("INGEST", "ingest.host")


print("--------- Creating ONI User and Directories.")
os.system('groupadd ' + ONI_GROUP)
print(ONI_GROUP +" Created...")
os.system('echo "%' + ONI_GROUP +'  ALL=(ALL) ALL" >> /etc/sudoers')
os.system('adduser '+ ONI_USERNAME )
print(ONI_USERNAME + " Created...")
os.system('useradd -G' + ONI_GROUP + ' ' +  ONI_USERNAME )
os.system('mkdir -p /home/' + ONI_USERNAME +'/.ssh')
print(ONI_USERNAME + " Directory created...")
result = commands.getoutput('sudo -u hdfs hadoop fs -mkdir /user/'+ONI_USERNAME)
if result == "":
    result = commands.getoutput('sudo -u hdfs hadoop fs -chown '+ONI_USERNAME+':hdfs /user/'+ONI_USERNAME)
elif result == "mkdir: `/user/"+ONI_USERNAME+"': File exists":
    print("HDFS Directory Exist !!!")
else:
    print("HDFS Error")
    exit()


print("--------- Applying ONI User Configurations")
vars = ['NODES','UINODE','MLNODE','GWNODE','IMPALA_DEM','HUSER','LUSER']
conf_values = ["('"+ node1 +"' '"+ node2 +"')",ONI_OA,ONI_MLMASTER,ONI_INGEST,ONI_MLMASTER,'/user/'+ONI_USERNAME,'/home/'+ONI_USERNAME]
conf_chg = dict(zip(vars,conf_values))
applyconf('/etc/duxbay.conf',conf_chg)
