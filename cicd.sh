docker rm -f hkCbbcDockerInstance
docker build -t hk_cbbc_docker .
docker run -d -p 8000:8000 --name hkCbbcDockerInstance hk_cbbc_docker:latest