Guacamole
====

Dockerfile for quacamole 0.9.2

Based on centos6

---
Author
===

Randy Hall <randy.hall@open-source.guru>

---
Why are there binaries in this project?
===

My first try at this included the whole build environment to install guacd from
source.  The resulting docker image was too big and took forever to deploy.

I couldn't find a repo with version 0.9.2 of docker packaged for centos6.
I built my own based on a SRPM found on fedora rawhide (guacamole-server-0.9.2-2.fc22.src.rpm).

Those binary RPMS build by me are included in this package until I find a version that
installs on centos6.  I made no changes to the RPM build.

This leaves the image free from all the build requirments although still large do to RPM dependancies.

---
Building
===

Build from docker file:

```
git clone git@github.com:hall757/guacamole.git
cd guacamole
docker build -t guacamole . 
```

You can also obtain it via:  

```
docker pull hall/guacamole
```

---
Running
===

Create your guacamole config directory and populate with the guacamole.properties file.
See the sampleconfig directory.  Then launch with the following.

```
docker run -d -v /your-config-location:/etc/guacamole -p 8080:8080 guacamole
```

Browse to ```http://your-host-ip:8080```

