if docker -v; then
    echo "Docker is installed"
else
    echo "please install docker and docker compose first"
    exit 1
fi

if docker-compose -v; then
    echo "docker-compose is installed"
else
    echo "please install docker-compose first"
    exit 1
fi

echo "creating directories in ${HOME}/bot"
mkdir  ~/bot ~/bot/registry ~/bot/db-data
cp ./docker-compose.yaml ~/bot/docker-compose.yaml

docker build -f ./Dockerfile -t demonoverlord:latest ..



