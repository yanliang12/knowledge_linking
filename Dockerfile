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

RUN pip3 install Flask==1.1.1
RUN pip3 install flask_restplus==0.13.0
RUN pip3 install Werkzeug==0.15.5
RUN pip3 install itsdangerous==1.1.0

RUN pip3 install jinja2==2.10.1
RUN pip3 install MarkupSafe==1.1.1

USER yan

RUN echo "ds2g1s2gs2"

WORKDIR /yan/
ADD *.py /yan/
ADD *.conf /yan/

CMD python3 app_path.py --port 2974
###########Dockerfile############