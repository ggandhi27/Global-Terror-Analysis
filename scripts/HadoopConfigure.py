#!/usr/bin/python2
import commands as cmd
import getpass as gp

print "\nWelcome to the world of HADOOP.\n"
print "Let's start configuring hadoop.\n"
ipAddress=None
username=None
password=None
sshQuery=None
dirName=None
def HadoopConfiguration():
	f=0
	while f==0:
		#Input the ip address of the remote system you want to configure hadoop
		print "Enter the IP address of the system you want to configure hadoop : ",
		global ipAddress
		global username
		global password
		global sshQuery
		ipAddress=raw_input()
		#Try to ping the remote system and check that it is reachale or not
		ipStatus=cmd.getstatusoutput("ping -c 1 "+ipAddress)
		if ipStatus[0]!=0:
			print "Ip address is not reachable.\nPlease try again."
		else:
			f=1

	
	f=0
	while f==0:
		#Take username and pasword as the input
		username=raw_input("Enter the username : ")
		password=gp.getpass("Enter the password : ")
		sshQuery="sshpass -p "+password+" ssh -o stricthostkeychecking=no "+username+"@"+ipAddress
		sshstatus=cmd.getstatusoutput(sshQuery+" exit")
		if sshstatus[0]!=0:
			print "Error occured while login."
			print "Please recheck the username and password and try again."
		else:
			print "Login successfull."
			f=1


	#checking whether java is installed on the remote system or not.
	print "\nChecking for JDK on the remote system."
	javaStatus=cmd.getstatusoutput(sshQuery+" rpm -q jdk")
	if javaStatus[0]==0:
		print "JDK is already installed on the remote system."
	else:
		javaQuery="sshpass -p "+password+" scp jdk-7u79-linux-x64.rpm "+username+"@"+ipAddress+":/"
		javaScpStatus=cmd.getstatusoutput(javaQuery)
		if javaScpStatus[0]==0:
			print "JDK rpm is successfully transfered on the remote system"
			#The file is successfully transfered. Now we have to install it.
			print "Installing JDK ........."
			javaInstallStatus=cmd.getstatusoutput(sshQuery+" rpm -i /jdk-7u79-linux-x64.rpm")
			if javaInstallStatus[0]==0:
				print "JDK is successfully installed on the remote system."
			else:
				print "Failed to install jdk on the remote system."
				print javaInstallStatus[1]
				print "Exiting ......"
				exit(-1)
		else:
			print "Failed to transfer the file to the remote system"
			print javaScpStatus[1]
			print "Exiting......"
			exit(-1)

	#checking whether hadoop is installed on the remote system or not
	print "\nChecking for hadoop on the remote system."
	hadoopStatus=cmd.getstatusoutput(sshQuery+" rpm -q hadoop ")
	if hadoopStatus[0]==0:
		print "Hadoop is already installed on the remote system."
	else:
		hadoopQuery="sshpass -p "+password+" scp hadoop-1.2.1-1.x86_64.rpm "+username+"@"+ipAddress+":/"
                hadoopScpStatus=cmd.getstatusoutput(hadoopQuery)
                if hadoopScpStatus[0]==0:
                        print "Hadoop rpm is successfully transfered on the remote system"
                        #The file is successfully transfered. Now we have to install it.
                        print "Installing hadoop ........."
                        hadoopInstallStatus=cmd.getstatusoutput(sshQuery+" rpm -i /hadoop-1.2.1-1.x86_64.rpm --replacefiles")
                        if hadoopInstallStatus[0]==0:
                                print "Hadoop is successfully installed on the remote system."
                        else:
                                print "Failed to install hadoop on the remote system."
                                print hadoopInstallStatus[1]
                                print "Exiting ......"
                                exit(-1)
                else:
                        print "Failed to transfer the file to the remote system"
                        print hadoopScpStatus[1]
                        print "Exiting......"
                        exit(-1)
	#Bring .bashrc file to the local system and configure the java and hadoop variables.
	bashStatus=cmd.getstatusoutput("sshpass -p "+password+" scp "+username+"@"+ipAddress+":/root/.bashrc /root/Documents/Project/Hadoop/")
	if bashStatus[0]==0:
		print "Bash File successfully recieved"
		bashData='\nexport JAVA_HOME=/usr/java/jdk1.7.0_79/\nexport PATH=/usr/java/jdk1.7.0_79/bin/:$PATH\n'
		bashFile=open(".bashrc","a+")
		bashFile.write(bashData)
		bashFile.close()
	else:
		print "Error occured while recieving the bash file."
		print bashStatus[0]
		print bashStatus[1]
		print "Exiting ........"
		exit(-1)
	bashStatus=cmd.getstatusoutput("sshpass -p "+password+" scp /root/Documents/Project/Hadoop/.bashrc "+username+"@"+ipAddress+":/root/ ")
	if bashStatus[0]==0:
		print "Path variables updated on the remote system."
	else:
		print "Error occured while updating the path variables."
		print bashStatus[1]
		print "Exiting ........."
		exit(-1)

#Fucntion to configure the master node
def MasterConfiguration():
	#Data that is to be inserted into the core-site.xml file in /etc/hadoop folder on remote system
	coreSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://%s:10001</value>\n</property>\n</configuration>'%ipAddress
	#print coreSiteFile
	f=0
	global dirName
	while f==0:
		dirName=raw_input("Enter the name of the directory you want to store your meta data : ")
		#Checking if the directory exists or not.
		dirStatus=cmd.getstatusoutput(sshQuery+" ls "+dirName)
		if dirStatus[0]==0:
			print "This directory already exists on the remote system."
			print "Please try again"
		else:
			f=1
	#Data that is to be inserted into the hdfs-site.xml file in /etc/hadoop folder on the remote system
	hdfsSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>%s</value>\n </property>\n</configuration>'%dirName
	#Creating files for core and hdfs to transfer on the remote system.
	hdfsFile=open("hdfs-site.xml","w")
	coreFile=open("core-site.xml","w")
	hdfsFile.write(hdfsSiteFile)
	coreFile.write(coreSiteFile)
	hdfsFile.close()
	coreFile.close()
	#Sending the core file to the remote system.
	coreFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp core-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
	if coreFileStatus[0] != 0:
		print "Error occurred while writing the core-site file."
		print coreFileStatus[1]
		print "Exiting"
	else:
		print "core-site.xml file is successfully updated"
	#Sending the hdfs file to the remote system.
	hdfsFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp hdfs-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if hdfsFileStatus[0] != 0:
                print "Error occurred while writing the hdfs-site file."
                print hdfsFileStatus[1]
                print "Exiting"
        else:
                print "hdfs-site.xml file is successfully updated"

	#Executing the necessary commands on the master node.
	formatStatus=cmd.getstatusoutput(sshQuery+" hadoop namenode -format")
	if formatStatus[0]==0:
		print "The master node directory is successfully formatted"
	else:
		print "Error occurred while formating the master node directory."
	
	#Starting the namenode(Master node) daemon on the remote system.
	startStatus=cmd.getstatusoutput(sshQuery+" hadoop-daemon.sh start namenode")
	if startStatus[0]==0:
		print "\n\nNamenode daemon is successfully started on the remote system."
	else:
		print "\n\nError occurred while starting the namenode on the remote system."
		print startStatus[1]
		print "Exiting ......"
		exit(-1)


#Fucntion to configure the client configuration code.

def ClientConfiguration():
	f=0
	masterIP=None
	while f==0: 
		masterIP
		masterIP=raw_input("Enter the IP Address of the master node : ")
		masterPing=cmd.getstatusoutput(sshQuery+" ping -c 1 "+masterIP)
		if masterPing[0]!=0:
			print "Master node is not reachable from "+ipAddress
		else:
			f=1
	
	print "\nWant to change the default(3) number of replications ? (Y/N)"
	f=0
	Choice=None
	while f==0:
        	Choice=raw_input("Enter your choice : ")
        	if len(Choice)>1:
        	        print "Please enter a valid choice."
       		elif not (Choice=="Y" or Choice=="N" or Choice=="y" or Choice=="n"):
        	        print "Please enter a valid choice."
        	else:
        	        f=1
	replications=None
	replicationTxt=""
	blockTxt=""
	if Choice == "Y" or Choice == "y":
		print "Enter the number of replications : "
		#Number of replications are not validated
		replications
		replications = raw_input()
		replicationstxt="<name>dfs.replication</name>\n<value>%d</value>"%replications
	print "\nWant to change the block size ? (Y/N)"
	f=0
        Choice=None
	blkSize=""
        while f==0:
                Choice=raw_input("Enter your choice : ")
                if len(Choice)>1:
                        print "Please enter a valid choice."
                elif not (Choice=="Y" or Choice=="N" or Choice=="y" or Choice=="n"):
                        print "Please enter a valid choice."
                else:
                        f=1
	if Choice == "y" or Choice == "Y":
		size=None
		print "The minimum block size must be 512 byte."
		while type:
			size
		        try:
				size=raw_input("Enter the block size : ")
                        except (ValueError):
                                print "Wrong size selected. Choose the directory again"
                                continue
			break
		blkSize
		blkSize="<name>dfs.block.size</name><value>%d</value>"%size
	coreSiteText='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://%s:10001</value>\n</property>\n</configuration>'%masterIP
	
	hdfsSiteText='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n%s\n%s </property>\n</configuration>'%(blkSize,replicationTxt)

	#print coreSiteText
        hdfsFile=open("hdfs-site.xml","w")
        coreFile=open("core-site.xml","w")
        hdfsFile.write(hdfsSiteText)
        coreFile.write(coreSiteText)
        hdfsFile.close()
        coreFile.close()

        #Sending the core file to the remote system.
        coreFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp core-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if coreFileStatus[0] != 0:
                print "Error occurred while writing the core-site file."
                print coreFileStatus[1]
                print "Exiting"
        else:
                print "core-site.xml file is successfully updated"
        #Sending the hdfs file to the remote system.
        hdfsFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp hdfs-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if hdfsFileStatus[0] != 0:
                print "Error occurred while writing the hdfs-site file."
                print hdfsFileStatus[1]
                print "Exiting"
        else:
                print "hdfs-site.xml file is successfully updated"


		

#Code for the slave configuration
def SlaveConfiguration():
	global sshQuery
        f=0
        masterIP=None
        while f==0:
                masterIP=raw_input("Enter the IP Address of the master node : ")
                masterPing=cmd.getstatusoutput(sshQuery+" ping -c 1 "+masterIP)
                if masterPing[0]!=0:
                        print "Master node is not reachable from "+ipAddress
                else:
                        f=1
	vgCmd=sshQuery+" vgs -o vg_name,vg_size,vg_free --separator , --unit g"
	vgName=[]
	vgSpace=[]
	print "\n\n!!!Make sure that their exists a VG on the remote system!!!\n\n"
	print "Volume groups available on the remote system are :\n"
	vgCmdStatus=cmd.getstatusoutput(vgCmd)
	#print vgCmdStatus[1]
	count=1
	if vgCmdStatus[0]==0:
		vg=vgCmdStatus[1].split('\n')
		print "\t"+vg[0].split(",")[0]+"\t"+vg[0].split(",")[-1]
		vg=vg[1:]
		for a in vg:
			vgName.append(a.split(',')[0])
			vgSize=a.strip().split(',')[-1]
			vgSpace.append(float(vgSize[0:len(vgSize)-1]))
			print str(count)+"\t"+vgName[-1]+"\t"+str(vgSpace[-1])
			count+=1
	else:
		print vgCmdStatus[1]
		print "Exiting ........"
		exit(-1)
	
	f=0
	vgChoice=None
	while f==0:
		try :
			vgChoice=int(raw_input("\n\nSelect a VG from the above list : "))
		except(ValueError) :
			print "Please enter a correct choice."
			continue
		if vgChoice>len(vgName):
			print "Please enter a correct choice."
			continue
		break	
	lvSize=None
        while f==0:
		try :
			lvSize=float(raw_input("\n\nEnter the size of the logical volume you want to create in Gb : "))
		except(ValueError) :
			print "Please enter a correct choice."
			continue
		if lvSize>vgSpace[vgChoice-1] or vgSpace[vgChoice-1]==0:
			print "Space not available on the selected VG."
                	print "Please enter a correct choice."
                        continue
               	break

	lvCmd=sshQuery+" lvs -o lv_name --noheadings"
	lvStatus=cmd.getstatusoutput(lvCmd)
	lvLsit=None
	if lvStatus[0]==0:
		lvList=lvStatus[1].split("\n")
	else:
		print lvStatus[1]
		print "Exiting ......"
		exit(-1)
	lvName=None
	dirName=None
	while True:
		lvName=raw_input("\n\nEnter the name of the LV you want to create : ")
		if lvName in lvList:
			print "\nLV with this name already exists."
		else:
			dirName=raw_input("Enter the absolute path of the folder you want to mount the LV :")
			dirQuery=sshQuery+" ls -l "+dirName
			dirStatus=cmd.getstatusoutput(dirQuery)
			if dirStatus[0]!=0:
				mkDir=sshQuery+" mkdir -p "+dirName
				mkDirStatus=cmd.getstatusoutput(mkDir)
				if mkDirStatus[0]==0:
					print "Directory Successfully created."
				else:
					print mkDirStatus[1]
					print "Exiting ......."
					exit(-1)
				break
			else:
				#Validation Not implemented
				print "Directory already exists. Want to continue ? (Y/N)"
				ch=raw_input()
				if ch=="Y" or ch=="y":
					break
				else:
					continue
	#Creating a Logical Volume
	lvCmd=sshQuery+" lvcreate --size "+lvSize+"G --name"+lvName+" "+vgName[vgChoice-1]
	lvCmdStatus=cmd.getstatusoutput(lvCmd)
	if lvCmdStatus[0]==0:
		print "LV is created successfully"
	else:
		print lvCmdStatus[1]
		print "Exiting ....."
		exit(-1)

	#Mounting the Logical Volume
	lvMount=sshQuery+" mount /dev/"+vgName[vgChoice-1]+"/"+lvName+" "+dirName
	lvmntStatus=cmd.getstatusoutput(lvMount)
	if lvmntStatus[0]==0:
		print "LV is mounted successfully"
	else:
		print lvmntStatus[1]
		print "Exiting ......"
		exit(-1)
	
        #Data that is to be inserted into the core-site.xml file in /etc/hadoop folder on remote system
        coreSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://%s:10001</value>\n</property>\n</configuration>'%masterIP
        #Data that is to be inserted into the hdfs-site.xml file in /etc/hadoop folder on the remote system
        hdfsSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>%s</value>\n </property>\n</configuration>'%dirName
        #Creating files for core and hdfs to transfer on the remote system.
        hdfsFile=open("hdfs-site.xml","w")
        coreFile=open("core-site.xml","w")
        hdfsFile.write(hdfsSiteFile)
        coreFile.write(coreSiteFile)
        hdfsFile.close()
        coreFile.close()
        #Sending the core file to the remote system.
        coreFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp core-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if coreFileStatus[0] != 0:
                print "Error occurred while writing the core-site file."
                print coreFileStatus[1]
                print "Exiting"
        else:
                print "core-site.xml file is successfully updated"
        #Sending the hdfs file to the remote system.
        hdfsFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp hdfs-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if hdfsFileStatus[0] != 0:
                print "Error occurred while writing the hdfs-site file."
                print hdfsFileStatus[1]
                print "Exiting"
        else:
                print "hdfs-site.xml file is successfully updated"

       #Starting the datanode(Slave node) daemon on the remote system.
        startStatus=cmd.getstatusoutput(sshQuery+" hadoop-daemon.sh start datanode")
        if startStatus[0]==0:
                print "\n\nDatanode daemon is successfully started on the remote system."
        else:
                print "\n\nError occurred while starting the Datanode on the remote system."
                print startStatus[1]
                print "Exiting ......"
                exit(-1)




#Code for configuration of job tracker
def JobTrackerConfiguration():
	global ipAddress
	global username
	global sshQuery
	global password
        masterIP=None
	f=0
        while f==0:
                masterIP=raw_input("Enter the IP Address of the master node : ")
                masterPing=cmd.getstatusoutput(sshQuery+" ping -c 1 "+masterIP)
                if masterPing[0]!=0:
                        print "Master node is not reachable from "+ipAddress
                else:
                        f=1
        coreSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://%s:10001</value>\n</property>\n</configuration>'%masterIP
        #Creating files for core and hdfs to transfer on the remote system.
        coreFile=open("core-site.xml","w")
        coreFile.write(coreSiteFile)
        coreFile.close()
        #Sending the core file to the remote system.
        coreFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp core-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if coreFileStatus[0] != 0:
                print "Error occurred while writing the core-site file."
                print coreFileStatus[1]
                print "Exiting"
        else:
                print "core-site.xml file is successfully updated"


	#Text to be saved in the file mapred-site.xml file
	mapredTxt='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>http://%s:9001</value>\n</property>\n</configuration>'%ipAddress
	
	mapredFile=open("mapred-site.xml","w")
	mapredFile.write(mapredTxt)
	mapredFile.close()
	
	
	#sending the mapred-site.xml to the remote system
        mapredFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp mapred-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if mapredFileStatus[0] != 0:
                print "Error occurred while writing the hdfs-site file."
                print mapredFileStatus[1]
                print "Exiting"
        else:
                print "mapred-site.xml file is successfully updated"

       #Starting the job tracker daemon on the remote system.
        startStatus=cmd.getstatusoutput(sshQuery+" hadoop-daemon.sh start jobtracker")
        if startStatus[0]==0:
                print "\n\nJob Tracker node daemon is successfully started on the remote system."
        else:
                print "\n\nError occurred while starting the Datanode on the remote system."
                print startStatus[1]
                print "Exiting ......"
                exit(-1)




#Code for the configuration of the job tracker
def TaskTrackerConfiguration():
	jtip=None
	f=0
        while f==0:
                jtip=raw_input("Enter the IP Address of the Job Tracker node : ")
                jtPing=cmd.getstatusoutput(sshQuery+" ping -c 1 "+jtip)
                if jtPing[0]!=0:
                        print "Master node is not reachable from "+ipAddress
                else:
                        f=1
          #Text to be saved in the file mapred-site.xml file
        mapredTxt='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>%s</value>\n</property>\n</configuration>'%jtip

        mapredFile=open("mapred-site.xml","w")
        mapredFile.write(mapredTxt)
        mapredFile.close()


        #sending the mapred-site.xml to the remote system
        mapredFileStatus=cmd.getstatusoutput("sshpass -p "+password+" scp mapred-site.xml "+username+"@"+ipAddress+":/etc/hadoop/")
        if mapredFileStatus[0] != 0:
                print "Error occurred while writing the hdfs-site file."
                print mapredFileStatus[1]
                print "Exiting"
        else:
                print "mapred-site.xml file is successfully updated"

       #Starting the task tracker daemon on the remote system.
        startStatus=cmd.getstatusoutput(sshQuery+" hadoop-daemon.sh start task tracker")
        if startStatus[0]==0:
                print "\n\nTask Tracker node daemon is successfully started on the remote system."
        else:
                print "\n\nError occurred while starting the Datanode on the remote system."
                print startStatus[1]
                print "Exiting ......"
                exit(-1)






#########################
#	MAIN		#
#	PROGRAM		#
#	STARTS		#
#	HERE		#
#########################
HadoopConfiguration()
#Ask user that want the input IP address as a master or a slave node.
print "\n\nWant to make "+str(ipAddress)+"\n\n(1)Master\n(2)Slave\n(3)Client\n(4)Job Tracker\n(5)Task Tracker or you want to (6)exit.\n  "
f=0
nodeChoice=None
while f==0:
	nodeChoice=raw_input("Enter your choice : ")
	if len(nodeChoice)>1:
		print "Please enter a valid choice."
	elif not (nodeChoice=="1" or nodeChoice=="2" or nodeChoice=="3" or nodeChoice=="4" or nodeChoice=="5" or nodeChoice=="6"):
		print "Please enter a valid choice."
	else:
		f=1

if nodeChoice=="1":
	#Calling the master configuration code
	MasterConfiguration()
elif nodeChoice=="3":
	#Calling the client configuration code
	ClientConfiguration()
elif nodeChoice=="2":
	#Calling the slave configuration code
	SlaveConfiguration()
elif nodeChoice=="4":
	#Calling the Job Tracker configuration code
	JobTrackerConfiguration()
elif nodeChoice=="5":
	#Calling the Task Tracker Configuration code
	TaskTrackerConfiguration()
