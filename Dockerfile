############################################################
# Dockerfile to build hall/guacamole
#
############################################################
From centos:centos6
Maintainer Randy Hall <randy.hall@open-source.guru>

# I could not find a current prebuild RPM for guacd.  The
# BIN directory contains RPMS compiled by me.  They depend
# on packages from epel.  Will remove these binaries when
# I find a relable repo that contains the latest guacamole
# version.  The SPEC file for the RPMS in in the credits
# directory.

EXPOSE 8080
ENV GUACAMOLE_HOME /etc/guacamole
volume /etc/guacamole
ENTRYPOINT ["monit","-d","10","-Ic","/etc/monitrc"]
add BIN /tmp

## The war & jar files from these are included in the BIN directory
#http://downloads.sourceforge.net/project/guacamole/current/binary/guacamole-0.9.2.war
#http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.32.tar.gz
#http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-mysql-0.9.2.tar.gz
#http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-ldap-0.9.2.tar.gz
#http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-noauth-0.9.2.tar.gz

# Install my guacamole RPMS, tomcat, monit, dependancies & basic config.
# I have found that doing this all in one run command results in a smaller container.

run cd /tmp ;\
    mkdir -p /var/lib/guacamole/classpath ;\
    mv monitrc /etc/monitrc ;\
    chmod 700 /etc/monitrc ;\
    yum -y update ;\
    rpm -Uvh http://epel.mirror.constant.com/6/i386/epel-release-6-8.noarch.rpm 2> /dev/null ;\
    yum -y install tar java-1.7.0-openjdk tomcat6 monit 2> /dev/null ;\
    mv *.jar /var/lib/guacamole/classpath ;\
    yum --nogpgcheck -y localinstall guacd*.x86_64.rpm libguac*.x86_64.rpm 2> /dev/null ;\
    mv guacamole-0.9.2.war /var/lib/tomcat6/webapps/guacamole.war ;\
    pushd /var/lib/tomcat6/webapps ;\
    ln -s guacamole.war ROOT.war ;\
    cd ~tomcat ;\
    ln -s /etc/guacamole .guacamole ;\
    popd ;\
    rm -Rf /tmp/* ;\
    yum clean all
workdir /etc/guacamole
