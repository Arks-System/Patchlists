#!/bin/bash

#
# http://psumods.co.uk/viewtopic.php?f=4&t=206
#

set -e

VERSIONS_FILE="../versionpatcher.txt"
PSO2_VERSION="$(pso2version | grep "SEGA" | cut -f 2)"
TEMP_FOLDER="./temp"
PATCH_PAGE_URL="http://pso2.acf.me.uk/Manual/"
PATCH_BASE_URL="https://pso2.acf.me.uk/Manual/index.php?file="

PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"

ARCHIVE_FORMAT=(.zip .rar)

pushd `dirname $0` > /dev/null
MAIN_PATH=`pwd -P`
popd > /dev/null

cd ${MAIN_PATH}
mkdir -p ${TEMP_FOLDER}
cd ${TEMP_FOLDER}
rm *.zip *.rar -f

function most_recent() {
	PATTERN="s/.* ([A-Za-z]+) ([0-9]+) ([0-9]+)( preliminary)? \($1\).*/\\2 \\1 \\3/i"

	p_archive=$(echo $PATCH_PAGE  | grep "Most recent version: ") 
	p_archive="$(echo ${p_archive} | sed -r "${PATTERN}")"
	p_archive="$(date -d"${p_archive}" +"%Y_%m_%d")"
	
	echo $p_archive
}

#min_patch="patch_$(most_recent "main")"
#large_patch="$(most_recent "large files")_largefiles"

#echo $min_patch $large_patch

#for i in ${ARCHIVE_FORMAT[@]}; do
#	echo $i
#done

function get_link() {
	echo $PATCH_PAGE | sed -r "s/.*(<a href=\"?([^\">]+)\"?>$1<\/a>).*/\\2/i"
}

function isRar() {
	##echo ${1##*.}
	if [[ "${1##*.}" = "rar" ]]; then
		return 0 
	else
		return 1
	fi
}

function rarIt() {
	ARCHIVE="${1%.*}"

	mkdir -p "./${ARCHIVE}"
	cd ${ARCHIVE}
	unzip -o ../$1 -d ./
	rar a "../${ARCHIVE}.rar" ./*
	cd ..
	rm "$ARCHIVE" -rf
}

function updateFile() {
	isRar "$1" || rarIt "$1"
	cp "${1%.*}.rar" "/home/www-data/arks-system.tool/patch/${2}" -v
	chown :www-data "/home/www-data/arks-system.tool/patch/${2}" -v
}

if [ "$PATCH_PAGE" = "" ]; then
	echo Retrying just once
	PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"
fi

PATCH_MINI="$(get_link "Click here to download the latest patch.")"
#PATCH_LARG="$(get_link "Large files")"

#wget --quiet $PATCH_MINI $PATCH_LARG
echo "Mini:  $PATCH_MINI"
#echo "Large: $PATCH_LARG"
echo
#wget $PATCH_MINI $PATCH_LARG || exit 1
wget $PATCH_MINI || exit 1

updateFile "$(basename ${PATCH_MINI})" "P1.rar"
#updateFile "$(basename ${PATCH_LARG})" "P2.rar"

sed -r "s/DW=.*/DW=${PSO2_VERSION}/" -i "../${VERSIONS_FILE}"
cat -e ../${VERSIONS_FILE}
#truncate -s -1 ../${VERSIONS_FILE}

perl -pi -e 'chomp if eof' ../${VERSIONS_FILE}
