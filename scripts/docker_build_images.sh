
./scripts/build.sh

docker build -t br_server -f scripts/Dockerfile.server .

docker build -t br_client -f scripts/Dockerfile.client .
