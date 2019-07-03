#!/bin/bash

mapfile -t i < <( youtube-dl -g --get-filename $1 )

# ffmpeg -ss $2 -i "${i[0]}" -ss $2 -i "${i[1]}" -t $3 "${i[2]}"

interval=""
if [ $3 != "-1" ]
then
    interval="-t $3"
fi

if [ "$4" = "mp3" ]
then
    ffmpeg -y -ss $2 -i "${i[1]}" $interval "$5${i[2]}.mp3"
else
    ffmpeg -y -ss $2 -i "${i[0]}" -ss $2 -i "${i[1]}" $interval "$5${i[2]}"
fi