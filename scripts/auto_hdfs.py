#!/usr/bin/python2

import commands
import cgi


nodesNum=cgi.FormContent()["nodesNum"][0]
nodeSize=cgi.FormContent()["nodeSize"][0]

nodesNumFile=open("NodesNumAuto","w")
nodesNumFile.write(nodesNum)
nodesNumFile.close()

nodeSizeFile=open("NodeSizeAuto","w")
nodeSizeFile.write(nodeSize)
nodeSizeFile.close()

nfsIpFile=open("nfsIP","r")
nfsPassFile=open("nfsPass","r")
nfsIp=nfsIpFile.read()
nfsPass=nfsPassFile.read()
nfsIpFile.close()
nfsPassFile.close()
nfsIp.strip("\n")
nfsPass.strip("\n")
nfsIp=nfsIp[0:len(nfsIp)-1]
nfsPass=nfsPass[0:len(nfsPass)-1]
username="gaurav"

commands.getoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita ifconfig enp0s10 0")

commands.getoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita ifconfig docker0 0")

#q=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita brctl addif mybr enp0s3")
#print q

daemonfile="""
{
        "bridge": "mybr"
}
"""
hostfile=open("daemon.json","w")
hostfile.write(daemonfile)
hostfile.close()
q= commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita brctl addbr mybr")
#print q

commands.getstatusoutput("sshpass -p q scp daemon.json root@harshita:/etc/docker")

q=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita brctl addif mybr enp0s10")
print q

#jt_ip=commands.getstatusoutput("docker inspect ar2 | jq .'[].NetworkSettings.Networks.bridge.IPAddress'")[1].strip('"')

#commands.getoutput("dhclient -v  eth0")
commands.getoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita systemctl restart docker")
p=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita docker run -dit --name=arya --privileged=true webserver1:v1")

q=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita docker exec arya ifconfig eth0 0")
p=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita docker exec arya dhclient -v eth0")
print q
print p

jt_ip=commands.getstatusoutput("sshpass -p q ssh -o stricthostkeychecking=no harshita docker inspect arya | jq .'[].NetworkSettings.Networks.bridge.IPAddress'")[1].strip('"')

print jt_ip


jt_ip_file=open("jt_ip.txt","a+")
jt_ip_file.write(jt_ip)
jt_ip_file.close()

