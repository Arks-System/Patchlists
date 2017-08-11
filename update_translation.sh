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
PATCH_PAGE_URL="http://pso2.acf.me.uk/Manual/"
PATCH_BASE_URL="https://pso2.acf.me.uk/Manual/index.php?file="

PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"

cd ${MAIN_PATH}
rm -rf "${OUTPUT_FOLDER}"
mkdir -p "${OUTPUT_FOLDER}/data/win32"
mkdir -p "${TEMP_FOLDER}"

function most_recent() {
	PATTERN="s/.* ([A-Za-z]+) ([0-9]+) ([0-9]+)( preliminary)? \($1\).*/\\2 \\1 \\3/i"

	p_archive=$(echo $PATCH_PAGE  | grep "Most recent version: ") 
	p_archive="$(echo ${p_archive} | sed -r "${PATTERN}")"
	p_archive="$(date -d"${p_archive}" +"%Y_%m_%d")"
	
	echo $p_archive
}

function get_link() {
	echo $PATCH_PAGE | sed -r "s/.*(<a href=\"?([^\">]+)\"?>$1<\/a>).*/\\2/i"
}


if [ "$PATCH_PAGE" = "" ]; then
	echo Retrying just once
	PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"
fi

PATCH_MINI="$(get_link "Click here to download the latest patch.")"

echo "Archive:  $PATCH_MINI"
wget "${PATCH_MINI}" -O "${TEMP_FOLDER}/patch.zip" || exit 1
echo $MAIN_PATH
unzip "${TEMP_FOLDER}/patch.zip" -d "${OUTPUT_FOLDER}/data/win32/"

./translation.py
