#!/bin/bash

read -r -p "Enter exists path for local installation [$HOME/PycharmProjects]:" CURR_DIR
CURR_DIR=${CURR_DIR:-$HOME/PycharmProjects}

read -r -p "Enter you login on github [xayam]: " NAME_GITHUB
NAME_GITHUB=${NAME_GITHUB:-xayam}

read -r -p "Enter name you github project [syncbookerkivy]: " NAME_PROJECT
NAME_PROJECT=${NAME_PROJECT:-syncbookerkivy}
GITHUB="https://raw.githubusercontent.com/$NAME_GITHUB/$NAME_PROJECT/main"

read -r -p "Enter name you application [syncbooker]: " NAME_APP
NAME_APP=${NAME_APP:-syncbooker}

cd "$CURR_DIR" || exit

echo "Installing depends..."
apt install mpg123
apt-get install beep

wget  --quiet --output-document=daemon.sh "$GITHUB/daemon.sh"
chmod +x daemon.sh
wget  --quiet --output-document=build.sh "$GITHUB/build.sh"
chmod +x build.sh
wget  --quiet --output-document=complete.mp3 "$GITHUB/res/complete.mp3"

echo "Testing complete.mp3..."
mpg123 -q complete.mp3

printf "v1.0\n" > latest.txt
printf "\nOptions +Indexes\nIndexOptions NameWidth=*\nIndexOptions FancyIndexing\nIndexOrderDefault Descending Date\n" > .htaccess

echo "Setup options. This require only once."
read -r -p "Enter URL you http server in format 'http://you.domain.zone': " HTTP_SERVER
read -r -p "Enter you ftp site for server '$HTTP_SERVER': " FTP_SITE
read -r -p "Enter ftp user for login on ftp site '$FTP_SITE': " FTP_USER
read -r -s -p "Enter ftp password for login on ftp site '$FTP_SITE': " FTP_PASSWORD
read -r -p "Enter path to Android SDK [$HOME/Documents/SDK]: " ANDROIDSDK
ANDROIDSDK=${ANDROIDSDK:-$HOME/Documents/SDK}
read -r -p "Enter path to Android NDK [$HOME/Documents/ndk]: " ANDROIDNDK
ANDROIDNDK=${ANDROIDNDK:-$HOME/Documents/ndk}
read -r -p "Enter target API version of your application [27]: " ANDROIDAPI
ANDROIDAPI=${ANDROIDAPI:-27}
read -r -p "Enter minimum supported API version of your application [21]: " NDKAPI
NDKAPI=${NDKAPI:-21}
read -r -p "Enter version of the NDK you installed [r25c]: " ANDROIDNDKVER
ANDROIDNDKVER=${ANDROIDNDKVER:-r25c}

sed -i "s|_NAME_GITHUB_|$NAME_GITHUB|g" daemon.sh
sed -i "s|_NAME_PROJECT_|$NAME_PROJECT|g" daemon.sh
sed -i "s|_CURR_DIR_|$CURR_DIR|g" daemon.sh
sed -i "s|_HTTP_SERVER_|$HTTP_SERVER|g" daemon.sh
sed -i "s|_FTP_SITE_|$FTP_SITE|g" daemon.sh
sed -i "s|_FTP_USER_|$FTP_USER|g" daemon.sh
sed -i "s|_FTP_PASSWORD_|$FTP_PASSWORD|g" daemon.sh
sed -i "s|_ANDROIDSDK_|$ANDROIDSDK|g" daemon.sh
sed -i "s|_ANDROIDNDK_|$ANDROIDNDK|g" daemon.sh
sed -i "s|_ANDROIDAPI_|$ANDROIDAPI|g" daemon.sh
sed -i "s|_NDKAPI_|$NDKAPI|g" daemon.sh
sed -i "s|_ANDROIDNDKVER_|$ANDROIDNDKVER|g" daemon.sh
sed -i "s|_NAME_APP_|$NAME_APP|g" daemon.sh
echo "Setup options is completed. All options write to file '$CURR_DIR/daemon.sh'"

echo "Connecting to '$FTP_SITE'..."
ftp -n "$FTP_SITE"<<EOF
quote USER $FTP_USER
quote PASS $FTP_PASSWORD
mkdir "latest"
binary
put latest.txt latest/latest.txt
put .htaccess
quit
EOF

echo "Now daemon.sh be waiting while make new commit on github with new version in config.sh and run script build.py on Windows..."
echo "Running daemon.sh"
./daemon.sh

read -r -p "Press ENTER for exit..."
