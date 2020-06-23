#!/bin/bash

PARAMS=()
OUTFILE=""
flag=0

for i in "$@"
do
case $i in
  -h | --help)
  docker run pbest:Dockerfile pbest-test $(echo $PARAMS) --help
  exit 0
  ;;
  -o |--output-file)
  flag=1
  shift # past argument=value
  ;;

  *)
  if [ $flag -eq 1 ]; then
    OUTFILE=$(readlink -m "$1")
    PARAMS+=" -o /data/"$(basename "$OUTFILE")
    flag=0
  else
    PARAMS+=" "$i
  fi
  shift # past argument=value
  ;;
esac
done
docker run -v $(dirname "$OUTFILE"):/data pbest:Dockerfile pbest-test $(echo $PARAMS)
