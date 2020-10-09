# Goal was to Gain hands-on experience with Google Cloud Platform and MapReduce (Hadoop).





### Problem statement :

##### Replacing existing heating/cooling (“HVAC”) systems can have a significant impact on the environment (as well as saving some money!) But in the absence of an outright failed system, identifying the specific system to replace can be challenging – one must consider years in service, efficiency of the unit, maintenance cost/records, general comfort level, user complaints, tax benefits, etc. In this small project, we are going to do some analysis that could help us make such a decision based on a dataset of measurements from a small collection of buildings using Hadoop to determine:
###### Q1. The 3 worst HVAC systems, based on all available data (where “worst” means the greatest difference between desired temperature and actual temperature)

###### Solution:

Mapper :
1. Takes the input from CSV and remove first line of csv
2. Used Desired and actual temperature to get the difference
3. Maintaining a global variable which stores the maximum value of the difference
4. Also, maintaining the age of the system to check for oldest systems for maximum temperature difference
5. Get only the maximum temperature difference values first
6. Sorting these values based on age and forwarding them to reducer

Reducer :
1. Takes input from mapper
2. Storing it in a list
3. Sorting this list reversely and getting the last three values (which contain maximums temp of the system and maximum age) which indicate the three worst systems.
4. Printing these values as the output
5. File is output.txt in zip


###### Q2. The 3 hottest buildings, based on all available data, during normal business hours.

###### Solution: 

Mapper :
1.	Takes the input from CSV and remove first line of csv
2.	Getting the normal working hours(8am -4pm)
3.	Getting the working days (Mon to Fri)
4.	Fetch all the records within these both ranges in a list
5.	On these records, taking average of similar machines records per building to get avg temperature per system in the building
6.	On these new records, get average of all the unique machine’s temperature to get the temperature of the building
7.	Getting the three hottest buildings from these records
8.	Passing on all the records (between working hours) of these three buildings to the reducer

Reducer :
1.	Takes the input from mapper
2.	For every duplicate value of time_stamp per building , calculating the average temperature value.
3.	So the output has unique value for each time stamp per building with the average temperature.
4.	Printing this output to the csv file which contains (unique time stamp per building, average temperature and building id)
5.	File is final.csv present in zip










##### Steps to replicate environment on Google Cloud Platform

1. Go to Google Cloud Platform (GCP): https://cloud.google.com/
2. Click “Compute Engine” on left side, click “VM instance”, and click “Create.”
3. [On the “Create an Instance” page] name the instance “<anything you like>” and change machine type to “4 vCPUs” (15 GB memory)
4. Change Boot disk from “Debian GNU/Linux 9 (stretch) “ to “Ubuntu 16.04 LTS“, (on the boot disk page) change “boot disk size“ to “32“ GB
5. Check both “Allow HTTP traffic” and “Allow HTTPS traffic” in Firewall and hit “create”.
6. Once you go on your instance, Go to “Network interfaces”, and click nic name (e.g. nic0)
7. Create a Fire rule from Firewall rules(On Network interface Details page) with "default-allow-all" select “All instances in the network” for Targets, Source IP ranges should be “0.0.0.0/0”, check “Allow all” for protocols and ports, and hit “create”
8. Click “Google Cloud Platform” on the left top. Next is “Compute Engine” --> VM Instances, then you will see your instance. Click “ssh” button, then another pop-up window will show up and you will log into your instance.

##### Steps to Install/Configure Hadoop on GCP Ubuntu 16.04 Server

1. Install java

    	sudo apt-get update
	    sudo apt-get install -y default jdk
2. Add Hadoop/YARN users

    	sudo addgroup hadoop
	    sudo adduser --ingroup hadoop hduser (enter password and just enter for other fields)
	    sudo adduser --ingroup hadoop yarn (enter password and just enter for other fields)
	    sudo usermod -a -G hadoop $(whoami)
	    
3. Setup SSH key for both Hadoop and YARN
	
	a. set key for Hadoop
		
		sudo su -hduser
		ssh-keygen -t rsa -P "" (enter when asks for a file)
		cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
		ssh localhost (Enter "yes" when confirmation asked, this is asked only first time.)
		exit
		exit
		
	b. Set key for YARN
		
		sudo su -yarn
		ssh-keygen -t rsa -P "" (Press enter when asks for a file)
		cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
		ssh localhost (Enter "yes" when confirmation asked, this is asked only first time.)
		exit
		exit
4. Download hadoop-2.7.7.tar.gz
	
	    cd
	    wget https://downloads.apache.org/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz
	    tar xvfz hadoop-2.7.7.tar.gz
	    sudo mv hadoop-2.7.7 /usr/local/hadoop
5. Create directories for namenode and datanode, and set permission for these directories
	
	    sudo mkdir -p /usr/local/hadoop/data/namenode
	    sudo mkdir -p /usr/local/hadoop/data/datanode
	    sudo mkdir -p /usr/local/hadoop/logs
	    sudo chown -R hduser:hadoop /usr/local/hadoop
	    sudo su - hduser
	    chmod g+w /usr/local/hadoop/logs
	    exit
6. Update .bashrc for your own account, hduser, and yarn

	a. (for your own account)
		
	    i. open .bashrc (using editor. e.g, emacs)
		ii. add the following lines at the end of the .bashrc file

            export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 export HADOOP_INSTALL=/usr/local/hadoop export HADOOP_CONF_DIR=$HADOOP_INSTALL/etc/hadoop export YARN_CONF_DIR=$HADOOP_INSTALL/etc/hadoop export PATH=$PATH:$HADOOP_INSTALL/bin export PATH=$PATH:$HADOOP_INSTALL/sbin export HADOOP_MAPRED_HOME=$HADOOP_INSTALL export HADOOP_COMMON_HOME=$HADOOP_INSTALL export HADOOP_HDFS_HOME=$HADOOP_INSTALL export YARN_HOME=$HADOOP_INSTALL export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_INSTALL/lib/native export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib" export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_INSTALL/lib/native" export JAVA_LIBRARY_PATH=$HADOOP_INSTALL/lib/native export LD_LIBRARY_PATH=$HADOOP_INSTALL/lib/native:$LD_LIBRARY_PATH export YARN_EXAMPLES=$HADOOP_INSTALL/share/hadoop/mapreduce export HADOOP_MAPRED_STOP_TIMEOUT=30 export YARN_STOP_TIMEOUT=30

		iii. source ~/.bashrc
	b. (for hduser)
	
		i. sudo su - hduser
	    ii. open and edit ~/.bashrc (using editor. e.g, emacs)
		iii. exit
	c. (for yarn)

		i. sudo su - yarn
		ii. open and edit ~/.bashrc (using editor. e.g, emacs)
		iii. exit	
7. Set Hadoop configurations (pseudo-distributed mode)

	a. (sudo) Edit /usr/local/hadoop/etc/hadoop/core-site.xml to be:

        <configuration>
                 <property>
        	<name>fs.defaultFS</name>
        	<value>hdfs://localhost:9000</value>
         </property> 
        </configuration>
	
	b.  (sudo) Edit /usr/local/hadoop/etc/hadoop/hdfs-site.xml to be:
	
        <configuration>
         <property>
        	<name>dfs.replication</name>
        	<value>1</value>
         </property>
         <property>
	        <name>dfs.namenode.name.dir</name>
        	<value>file:/usr/local/hadoop/data/namenode</value>
        </property>
         <property>
        	<name>dfs.datanode.data.dir</name>
        	<value>file:/usr/local/hadoop/data/datanode</value>
         </property>
         <property>
	        <name>dfs.permissions.superusergroup</name>
        	<value>hadoop</value>
         </property>
        </configuration>
	
	c. Create /usr/local/hadoop/etc/hadoop/mapred-site.xml from the template (mapred-site.xml.template)
		
		sudo su hduser
		cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/etc/hadoop/mapred-site.xml
		exit
	d. (sudo) Edit /usr/local/hadoop/etc/hadoop/mapred-site.xml to be:
	
        <configuration>
         <property> 
        	<name>mapreduce.framework.name</name> 
        	<value>yarn</value> 
         </property>
        </configuration>
	
	e.	(sudo) Edit /usr/local/hadoop/etc/hadoop/yarn-site.xml to be:
	
        <configuration>
         <property>
         	<name>yarn.nodemanager.aux-services</name> 
         	<value>mapreduce_shuffle</value> 
          </property>
          <property> 
         	<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
         	<value> org.apache.hadoop.mapred.ShuffleHandler</value> 
          </property> 
          <property> 
         	<name>yarn.resourcemanager.hostname</name> 
         	<value>localhost</value>
          </property>
         </configuration>

	f. (sudo) Edit /usr/local/hadoop/etc/hadoop/hadoop-env.sh to point JAVA_HOME at /usr/lib/jvm/java-8-openjdk-amd64 -- i.e., change this line: 
	    
	    “export JAVA_HOME = $(JAVA_HOME)” to: “export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64”
	
	g.	(sudo) Edit /usr/local/hadoop/etc/hadoop/mapred-env.sh to be:
	
		export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 
		export HADOOP_MAPRED_IDENT_STRING=hduser
	
8. Initialize and boot Hadoop

	    sudo su - hduser
	    $HADOOP_INSTALL/bin/hdfs namenode -format (This is to format namenode.)
	    $HADOOP_INSTALL/sbin/start-dfs.sh (accept connection to 0.0.0.0)
	    $HADOOP_INSTALL/sbin/stop-dfs.sh
	    exit
	
##### Done!!
	
#### Additional Notes
1. Start Hadoop (HDFS and YARN Resource Manager)
        
        sudo su -p - hduser -c $HADOOP_INSTALL/sbin/start-dfs.sh
        • sudo su -p - yarn -c $HADOOP_INSTALL/sbin/start-yarn.sh
2. Stop Hadoop (HDFS and YARN Resource Manager)

        sudo su -p - hduser -c $HADOOP_INSTALL/sbin/stop-dfs.sh
        sudo su -p - yarn -c $HADOOP_INSTALL/sbin/stop-yarn.sh
        HDFS commands guide: https://hadoop.apache.org/docs/r2.7.0/hadoop-project-dist/hadoop-common/FileSystemShell.html
