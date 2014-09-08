all:	.monitrc .always_run_this 
	docker build -t test .
	docker run -i -p 8080:8080 -p 2812:2812 -p 2222:22 -v /etc/guacamole:/etc/guacamole -t test 

.monitrc: monitrc ../BIN/monitrc
	cat monitrc > .monitrc
	cat ../BIN/monitrc >> .monitrc

#id_dsa:
#	ssh-keygen -b 1024 -t dsa -f id_dsa -P ""

.always_run_this:

clean:
	rm -f id_dsa id_dsa.pub .monitrc	
