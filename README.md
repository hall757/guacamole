Guacamole
====

Dockerfile for quacamole 0.9.3

Based on phusion

---
Author
===

Randy Hall <randy.hall@open-source.guru>

---
Building
===

Build from docker file:

```
git clone git@github.com:hall757/guacamole.git
cd guacamole
docker build -t hall/guacamole . 
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
docker run -d -v /your-config-location:/etc/guacamole -p 8080:8080 hall/guacamole
```

Browse to ```http://your-host-ip:8080```

