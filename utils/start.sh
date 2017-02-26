#!/bin/bash
#docker pull ingressguard/main
docker rm -f ingress
docker rm -f redis
#docker run -d --name redis -p 127.0.0.1:6379:6379 --restart=always redis
#docker run -d --name ingress --restart=always -h ingress-guard --link redis:redis ingressguard/main