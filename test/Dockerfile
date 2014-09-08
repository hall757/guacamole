############################################################
# Based on hall/guacamole
############################################################
From guacamole
add .monitrc /etc/monitrc
run chmod 600 /etc/monitrc ;\
    echo monit -d 10 -c /etc/monitrc > /usr/local/bin/startmonit ;\
    chmod a+x /usr/local/bin/startmonit
EXPOSE 2812
ENTRYPOINT /usr/local/bin/startmonit && /bin/bash 
#ENTRYPOINT ["monit","-v","-d","10","-Ic","/etc/monitrc"]
