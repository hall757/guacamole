hall/guacamole test container
====

This dockerfile bolts on debugging tools to the production container.  To use, first build hall/guacamole and give it a tag of guacamole. Next, change to this directory and type make.  The container will be built and started.  You can connect to http://host_ip:2812 to see the monit console.

```
docker build -t guacamole .
cd test
make
```
