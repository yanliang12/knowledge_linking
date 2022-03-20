###########Dockerfile############
FROM yanliang12/yan_dbpedia_query:1.0.2

##install entity linking dexter

WORKDIR /yan/
RUN wget http://dexter.isti.cnr.it/dexter.tar.gz
RUN tar xvzf /yan/dexter.tar.gz

WORKDIR /yan/
RUN mv /yan/dexter2/* ./

USER root
RUN pip3 install requests==2.24.0
USER yan

EXPOSE 8080

## install neo4j 

USER root
RUN pip3 install neo4j==4.1.1
USER yan

WORKDIR /yan/
RUN wget http://neo4j.com/artifact.php?name=neo4j-community-3.5.12-unix.tar.gz
RUN tar -xf 'artifact.php?name=neo4j-community-3.5.12-unix.tar.gz'

## install rest api

USER root
RUN pip3 install Werkzeug==0.16.1
RUN pip3 install flask==1.1.2
RUN pip3 install flask_restplus==0.13.0
USER yan

RUN echo "sdg5s1g515sd5gs15g5"

WORKDIR /yan/
RUN git clone https://github.com/yanliang12/yan_dbpedia_query.git
RUN mv yan_dbpedia_query/* ./
RUN rm -r yan_dbpedia_query

WORKDIR /yan/
RUN git clone https://github.com/jingyanwang/neo4j_docker.git
RUN mv neo4j_docker/* ./
RUN rm -r neo4j_docker

WORKDIR /yan/
RUN git clone https://github.com/yanliang12/yan_entity_linking.git
RUN mv yan_entity_linking/* ./
RUN rm -r yan_entity_linking

WORKDIR /yan/
RUN git clone https://github.com/yanliang12/yan_rest_api.git
RUN mv yan_rest_api/* ./
RUN rm -r yan_rest_api

WORKDIR /yan/
RUN git clone https://github.com/jingyanwang/knowledge_linking.git
RUN mv knowledge_linking/* ./
RUN rm -r knowledge_linking

CMD python3 app_path.py --port 2974
###########Dockerfile############