FROM envoyproxy/envoy-dev:latest

COPY envoy.yml /etc/envoy/envoy.yml

CMD /usr/local/bin/envoy -c /etc/envoy/envoy.yml -l trace --log-path /tmp/envoy_info.log

# command to run and publish port 9090
# docker run -d -p 9090:9090 --name envoy envoy:test