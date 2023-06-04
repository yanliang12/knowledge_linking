# Knowledge Linking Engine

Linking the text to the IDs of entities from a knowledge graph. It not only produces the background knowledge of the directly mentioned entities in the text, but also the entities not mentioned in the text but closely linked to the content.

Input a free text, the engine will identify the entities from the text, together with the related relations and entities from the DBPedia knowledge graph, and show them in Noe4j. 

Below is how to use it:

### pull the docker image

```bash
docker pull jingyanwang1/knowledge_linking:1.0.3
```

### run the docker 

```bash
docker run -it ^
-p 0.0.0.0:2974:2974 ^
-p 0.0.0.0:8080:8080 ^
-p 0.0.0.0:9267:9267 ^
-p 0.0.0.0:5701:5701 ^
-p 0.0.0.0:5974:5974 ^
-p 0.0.0.0:3097:3097 ^
jingyanwang1/knowledge_linking:1.0.3
```


### input 

go to url: http://localhost:2974 to input your own text

<img src="input.png" width="500">

input text:

```
{
  "text": "I visited the Louvre Abu Dhabi and Zayed National Museum today."
}
```

### output 

go to the url: http://localhost:5974 to see the results

<img src="WeChat%20Screenshot_20211209224203.png" width="500">


### backend database

the knowledge graph triplets are in a ES instance, available at http://localhost:9267/dbpedia_triplet/_search?pretty=true

### contact

If you want to see a demo from me, or you have your own documents to be enriched by the knowledge graph, please contact me at jimjywang@gmail.com

### youtube demo link

https://youtu.be/jCqvBPSn4rA
