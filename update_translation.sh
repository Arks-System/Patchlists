#!/bin/bash

#
# http://psumods.co.uk/viewtopic.php?f=4&t=206
#

set -e

pushd `dirname $0` > /dev/null
MAIN_PATH=`pwd -P`
popd > /dev/null

TEMP_FOLDER="${MAIN_PATH}/temp"
OUTPUT_FOLDER="${MAIN_PATH}/patch_prod/translation/"

cd ${MAIN_PATH}
rm -rf "${OUTPUT_FOLDER}"
mkdir -p "${OUTPUT_FOLDER}/data/win32"
mkdir -p "${TEMP_FOLDER}"

PATCH_MINI="$(./translationlink.py)"

echo "Archive:  $PATCH_MINI"
wget "${PATCH_MINI}" -O "${TEMP_FOLDER}/patch.zip" --user-agent 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' --header='Referer: https://pso2.acf.me.uk/Manual/' || exit 1
echo $MAIN_PATH
if (file "${TEMP_FOLDER}/patch.zip" | grep RAR); then
	unrar e "${TEMP_FOLDER}/patch.zip" "${OUTPUT_FOLDER}/data/win32/"
else
	unzip "${TEMP_FOLDER}/patch.zip" -d "${OUTPUT_FOLDER}/data/win32/" &> /dev/null
fi

./translation.py
