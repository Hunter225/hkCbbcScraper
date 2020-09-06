docker rm -f hkCbbcDockerInstance
docker build -t hk_cbbc_docker .
docker run -d -p 8082:8082 --name hkCbbcDockerInstance hk_cbbc_docker:latest