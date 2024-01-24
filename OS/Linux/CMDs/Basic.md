# Basic CMD set

## Communications

#### echo

1. This is the basic command to print a *string* to the terminal output. 
```bash
└─$ echo "Shinchan"
Shinchan
```

2. Very helpful in reading variables and piping commands.
```bash
└─$ echo $OSTYPE     
linux-gnu
```

3. Help is always available at man.

## System Information

#### whoami

1. Prints the effective username to the screen. Effective user is the privileges that the logged in user is bound by or operate within.
```bash
└─$ whoami       
kali
```

2. Very effective command to know where you are int he system's user hierarchy. Helps decide the next horizontal and vertical jump.

#### uname

1. Tells us fruitful information about the system that we are logged in. **-a** option is useful.

```bash
└─$ uname -a
Linux kali ***************************************
```

#### df

1. Tells you critical information about file system and space usage. **-H** - to get information in human units. 

```bash
└─$ df -H    
Filesystem      Size  Used Avail Use% Mounted on
udev            2.1G     0  2.1G   0% /dev
```

#### lscpu

1. The lscpu utility provides a comprehensive summary of your CPU's capabilities, including model information, the number of cores, speeds, flags, virtualization capabilities, and security mitigation applied.

```bash
└─$ lscpu   
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         40 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  3
```

## File System

#### touch

1. Standard command used in the UNIX/Linux operating system which is used to create, change and modify the timestamps of a file. Can create empty files >=1. 

```bash
└─$ touch 1    
                                                                                                     
┌──(kali㉿kali)-[~/Desktop/Github/Footsteps]
└─$ ls -la
total 56
drwxr-xr-x 4 kali kali  4096 Jan 23 21:32 .
drwxr-xr-x 6 kali kali  4096 Jan 23 20:23 ..
-rw-r--r-- 1 kali kali     0 Jan 23 21:32 1
drwxr-xr-x 8 kali kali  4096 Jan 23 20:34 .git
                                                                                                     
┌──(kali㉿kali)-[~/Desktop/Github/Footsteps]
└─$ touch 2 3
                                                                                                     
┌──(kali㉿kali)-[~/Desktop/Github/Footsteps]
└─$ ls -la
total 56
drwxr-xr-x 4 kali kali  4096 Jan 23 21:33 .
drwxr-xr-x 6 kali kali  4096 Jan 23 20:23 ..
-rw-r--r-- 1 kali kali     0 Jan 23 21:32 1
-rw-r--r-- 1 kali kali     0 Jan 23 21:33 2
-rw-r--r-- 1 kali kali     0 Jan 23 21:33 3
```

2. Very useful if you only want to update the __associated timestamps__ with the files. Utilize the *-a*, *-d* or *-m* options. Please look out for help. Please look at [stat]() cmd for the meaning of the terms.

3. You can also create files with specific timestamps as 
```bash
└─$ touch -t 202205172301 1      
                                                                                                     
┌──(kali㉿kali)-[~/Desktop/Github/Footsteps]
└─$ ls -la 
total 56
drwxr-xr-x 4 kali kali  4096 Jan 23 21:40 .
drwxr-xr-x 6 kali kali  4096 Jan 23 20:23 ..
-rw-r--r-- 1 kali kali     0 May 17  2022 1
```

#### stat

1. Displays information about files and files systems. This is useful to see how can one avoid AVs scanning for **timestamp recency.** 

```bash
└─$ stat 1   
  File: 1
  Size: 0               Blocks: 0          IO Block: 4096   regular empty file
Device: 8,1     Inode: 4622203     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/    kali)   Gid: ( 1000/    kali)
Access: 2022-05-17 23:01:00.000000000 -0400
Modify: 2022-05-17 23:01:00.000000000 -0400
Change: 2024-01-23 21:40:52.794428639 -0500
 Birth: 2024-01-23 21:40:52.794428639 -0500
```

