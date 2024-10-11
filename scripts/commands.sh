#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e
echo '🟡 Initializing initial commands!'

wait_psql.sh
migrate.sh
runserver.sh