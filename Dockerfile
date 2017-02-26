FROM ubuntu:16.04

WORKDIR /var/www

RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor

COPY ./utils/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./dist/* ./

CMD ["/usr/bin/supervisord"]

