# yan_text_kg_enrichment

```bash
docker pull yanliang12/yan_knowledge_linking:1.0.2

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

input text:

```
{
  "text": "I visited the Louvre Abu Dhabi today and Zayed National Museum today."
}
```

### output http://localhost:5974

