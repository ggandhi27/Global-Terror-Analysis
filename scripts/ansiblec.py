#!/usr/bin/python2
import commands
f=open('namenode.yml','a+')
noofnodes=3
user='harshita'
size=2
for i in range(0,noofnodes):
	userid=str(i)+user
	f=open('datanode{}.yml'.format(userid),'a+')
	f.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n'%(
---
- hosts: web
  tasks:
   - command: "lvcreate --size 2G --name lv{} vg".format(userid)
   - command: "mkfs.ext4 /dev/vg/lv{}".format(userid)
   - file:
      state: directory
      path: "/nfsshare{}".format(userid)
   - command: "mount /dev/vg/lv{} /nfsshare{}".format(userid,userid)
   - copy: 
      src: "/root/exports"
      dest: "/etc/exports"
   - service:
      name: "nfs"
      state: started
)) 
	commands.getoutput("ansible-playbook {}".format(userid))
