############################################################
# Dockerfile to build guacamole proxy
# intended to be used with a tomcat image hosting the 
# guacamole client files.
#
# Based on centos:6
############################################################
From centos:centos6
Maintainer Randy Hall

# I could not find a current prebuild RPM for guacd.  The
# RPMS directory contains RPMS compiled by me.  They depend
# on packages from epel.  Will remove these binaries when
# I find a relable repo that contains the latest guacamole
# version.

EXPOSE 8080
ENV GUACAMOLE_HOME /etc/guacamole
volume /etc/guacamole
ENTRYPOINT ["monit","-d","10","-Ic","/etc/monitrc"]
add BIN /tmp
add monitrc /etc/monitrc
workdir /tmp
add http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.32.tar.gz /tmp/mysql-connector-java-5.1.32.tar.gz
add http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-mysql-0.9.2.tar.gz /tmp/guacamole-auth-mysql-0.9.2.tar.gz
add http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-ldap-0.9.2.tar.gz /tmp/guacamole-auth-ldap-0.9.2.tar.gz
add http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-noauth-0.9.2.tar.gz /tmp/guacamole-auth-noauth-0.9.2.tar.gz

# TODO: make custom cups-libs and bzip2 packages to cut build size in half

# Install my guacamole RPMS, tomcat, monit, dependancies & basic config
run mkdir -p /var/lib/guacamole/classpath ;\
    chmod 700 /etc/monitrc; \
    yum -y install tar java-1.7.0-openjdk tomcat6 monit 2> /dev/null ;\
    tar -zxf mysql-connector-java-5.1.32.tar.gz ;\
    tar -zxf guacamole-auth-mysql-0.9.2.tar.gz ;\
    tar -zxf guacamole-auth-ldap-0.9.2.tar.gz ;\
    tar -zxf guacamole-auth-noauth-0.9.2.tar.gz ;\
    mv mysql-connector-java-5.1.32/mysql-connector-java-5.1.32-bin.jar /var/lib/guacamole/classpath ;\
    mv guacamole-auth-mysql-0.9.2/lib/* /var/lib/guacamole/classpath ;\
    mv guacamole-auth-ldap-0.9.2/lib/* /var/lib/guacamole/classpath ;\
    mv guacamole-auth-noauth-0.9.2/lib/* /var/lib/guacamole/classpath ;\
    rpm -Uvh http://epel.mirror.constant.com/6/i386/epel-release-6-8.noarch.rpm 2> /dev/null ;\
    yum --nogpgcheck -y localinstall guacd*.x86_64.rpm libguac*.x86_64.rpm 2> /dev/null ;\
    mv guacamole-0.9.2.war /var/lib/tomcat6/webapps/guacamole.war ;\
    pushd /var/lib/tomcat6/webapps ;\
    ln -s guacamole.war ROOT.war ;\
    cd ~tomcat ;\
    ln -s /etc/guacamole .guacamole ;\
    popd ;\
    rm -Rf /tmp/* ;\
    yum clean all

