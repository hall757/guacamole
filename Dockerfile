FROM phusion/baseimage:0.9.13
ENV HOME /root
CMD ["/sbin/my_init"]
ADD excludes /etc/dpkg/dpkg.cfg.d/excludes
run mkdir -p /etc/guacamole /var/lib/guacamole/classpath ;\
    apt-get update ;\
    apt-get install -y libcairo2-dev libpng12-dev freerdp-x11 libssh2-1 \
    libfreerdp-dev libvorbis-dev libssl0.9.8 gcc libssh-dev libpulse-dev \
    tomcat7 tomcat7-admin libpango1.0-dev libssh2-1-dev autoconf wget \
    libossp-uuid-dev libtelnet-dev libvncserver-dev ;\
    cd /tmp ;\
    wget --span-hosts http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.32.tar.gz ;\
    wget --span-hosts http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-ldap-0.9.2.tar.gz ;\
    wget --span-hosts http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-noauth-0.9.2.tar.gz ;\
    wget --span-hosts http://downloads.sourceforge.net/project/guacamole/current/source/guacamole-client-0.9.2.tar.gz ;\
    wget --span-hosts http://downloads.sourceforge.net/project/guacamole/current/extensions/guacamole-auth-mysql-0.9.2.tar.gz ;\
    tar -zxf mysql-connector-java-5.1.32.tar.gz ;\
    tar -zxf guacamole-client-0.9.2.tar.gz ;\
    tar -zxf guacamole-auth-ldap-0.9.2.tar.gz ;\
    tar -zxf guacamole-auth-noauth-0.9.2.tar.gz ;\
    tar -zxf guacamole-auth-mysql-0.9.2.tar.gz ;\
    mv `find . -type f -name '*.jar'` /var/lib/guacamole/classpath ;\
    wget --span-hosts http://sourceforge.net/projects/guacamole/files/current/source/guacamole-server-0.9.2.tar.gz ;\
    tar -zxf guacamole-server-0.9.2.tar.gz ;\
    cd /var/lib/tomcat7/webapps ;\
    wget --span-hosts http://sourceforge.net/projects/guacamole/files/current/binary/guacamole-0.9.2.war ;\
    ln -s guacamole-0.9.2.war ROOT.war ;\
    ln -s guacamole-0.9.2.war guacamole.war ;\
    cd /tmp/guacamole-server-0.9.2 ;\
    ./configure --with-init-dir=/etc/init.d ;\
    make ;\
    make install ;\
    update-rc.d guacd defaults ;\
    ldconfig ;\
    cd /usr/share/tomcat7 ;\
    ln -s /etc/guacamole .guacamole ;\
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
                            /usr/share/man /usr/share/groff /usr/share/info \
                            /usr/share/lintian /usr/share/linda /var/cache/man ;\
    find /usr/share/doc -depth -type f ! -name copyright|xargs rm || true ;\
    find /usr/share/doc -empty|xargs rmdir || true
