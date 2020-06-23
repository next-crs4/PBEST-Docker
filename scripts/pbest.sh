#!/bin/bash
PARAMS=()
INFILE=""
INDIR=""
OUTFILE=""
OUTDIR=""
iflag=0
oflag=0


showError() {
# `cat << EOF` This means that cat should stop reading when EOF is detected
cat << EOF
Please, be careful. Input & Output files must be:

EOF
# EOF is found above and hence cat command stops reading. This is equivalent to echo but much neater when printing out.
}

for i in "$@"
do
case $i in
  -h | --help)
  docker run pbest:Dockerfile pbest --help
  exit 0
  ;;
  -o |--output-file)
  oflag=1
  shift
  ;;
  -i |--input-file)
  iflag=1
  shift
  ;;
  *)
  if [ $oflag -eq 1 ];
  then
    OUTFILE=$(readlink -m "$1")
    PARAMS+=" -o /data/"$(basename "$OUTFILE")
    OUTDIR=$(dirname "$OUTFILE")
    oflag=0
  elif [ $iflag -eq 1 ];
  then
    INFILE=$(readlink -m "$1")
    PARAMS+=" -i /data/"$(basename "$INFILE")
    INDIR=$(dirname "$INFILE")
    iflag=0
  else
    PARAMS+=" "$i
  fi
  shift
  ;;
esac
done

if [[ "$OUTDIR" == "$INDIR" ]] && [[ -n "$OUTDIR" ]];
then
  docker run -v $(echo "$OUTDIR"):/data pbest:Dockerfile pbest $(echo $PARAMS)
else
  echo "Please, be careful. Input & Output files must be in the same local folder"
fi