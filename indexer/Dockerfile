FROM elasticsearch:7.4.0
COPY serbian-analyzer-1.0-SNAPSHOT.zip /usr/share/elasticsearch/
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install file:///usr/share/elasticsearch/serbian-analyzer-1.0-SNAPSHOT.zip