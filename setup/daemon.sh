#!/bin/bash

export NAME_GITHUB="_NAME_GITHUB_"
export NAME_PROJECT="_NAME_PROJECT_"
export CURR_DIR="_CURR_DIR_"
export HTTP_SERVER="_HTTP_SERVER_"
export FTP_SITE="_FTP_SITE_"
export FTP_USER="_FTP_USER_"
export FTP_PASSWORD="_FTP_PASSWORD_"
export ANDROIDSDK="_ANDROIDSDK_"
export ANDROIDNDK="_ANDROIDNDK_"
export ANDROIDAPI="_ANDROIDAPI_"  # Target API version of your application
export NDKAPI="_NDKAPI_"  # Minimum supported API version of your application
export ANDROIDNDKVER="_ANDROIDNDKVER_"  # Version of the NDK you installed
export COMPLETE_LOOP=20
export NAME_APP="_NAME_APP_"

while true; do

    cd $CURR_DIR || exit

    wget  --quiet --output-document=latest_new.txt "$HTTP_SERVER/latest/latest.txt"

    # OLD_VERSION=$(<latest.txt)
    NEW_VERSION=$(<latest_new.txt)

    if cmp latest_new.txt latest.txt
    then
        echo "Remote version equal local version"
    else
        echo "Find new version $NEW_VERSION"
        ./build.sh
        rm $CURR_DIR/latest_new.txt
        for ((i=1;i<=$COMPLETE_LOOP;i++)); do
            mpg123 -q complete.mp3
        done
    fi

    sleep 10s

done

read -r -p "Press ENTER for exit..."
