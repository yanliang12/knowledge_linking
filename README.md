# yan_knowledge_linking

### pull the docker image

```bash
docker pull yanliang12/yan_knowledge_linking:1.0.2
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
yanliang12/yan_knowledge_linking:1.0.2
```


### input http://localhost:2974

<img src="WeChat%20Screenshot_20211209224431.png" width="500">

input text:

```
{
  "text": "I visited the Louvre Abu Dhabi today and Zayed National Museum today."
}
```

### output http://localhost:5974


<img src="WeChat%20Screenshot_20211209224203.png" width="500">
