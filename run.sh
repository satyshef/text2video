IMAGE=text2video
NAME=t2v
PORT=5000
CURRENT_DIR=$(pwd)
SOURCE_DIR=$CURRENT_DIR/source/
OUT_DIR=$CURRENT_DIR/out/

docker run -d --rm --name $NAME -p $PORT:5000 -v $CURRENT_DIR/app/:/app -v $SOURCE_DIR:/app/source/ -v $OUT_DIR:/app/out/ $IMAGE
