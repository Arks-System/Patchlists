#!/bin/bash

#
# http://psumods.co.uk/viewtopic.php?f=4&t=206
#

set -e

alias errcho='>&2 echo'

VERSIONS_FILE="../versionpatcher.txt"
#PSO2_VERSION="$(pso2version | grep "SEGA" | cut -f 2)"
PATCH_PAGE_URL="http://pso2.acf.me.uk/Manual/"
PATCH_BASE_URL="https://pso2.acf.me.uk/Manual/index.php?file="

PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"

ARCHIVE_FORMAT=(.zip .rar)

TODAY="$(date +"%Y_%m_%d")"

pushd `dirname $0` > /dev/null
MAIN_PATH=`pwd -P`
popd > /dev/null

cd ${MAIN_PATH}

function get_link() {
	echo $PATCH_PAGE | sed -r "s/.*(<a href=\"?([^\">]+)\"?>$1<\/a>).*/\\2/i"
}

function parse_date_frompatch() {
	D="$(echo $1 | sed -r 's/.*patch_([0-9]+)_([0-9]+)_([0-9]+)\.zip/\1\/\2\/\3/gi')"
	date -d "$D"  +"%Y_%m_%d"
}

function date_scoreless() {
	echo $1 | sed 's/_//g'
}

if [ "$PATCH_PAGE" = "" ]; then
	echo Retrying just once
	PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"
fi

PATCH_MINI="$(get_link "Click here to download the latest patch.")"
PARSED_DATE="$(parse_date_frompatch $PATCH_MINI)"


echo "Mini:  $PATCH_MINI"
echo "Patch date: $PARSED_DATE"
echo "Today: $TODAY"

ARCHIVE_DATE=""
if [ -f "./P1.rar" ]; then
	ARCHIVE_DATE="$(date -d"$(stat ./P1.rar |grep Modify|cut -d' ' -f2-)" +"%Y_%m_%d")"
	echo "P1.rar: $ARCHIVE_DATE"
else
	echo No P1 file, go ahead and install it
fi

function update_available() {
	ret=0
	T="$(date_scoreless $1)"
	P="$(date_scoreless $2)"
	A="$(date_scoreless $3)"

	#echo T:$T P:$P A:$A 
	#>&2 echo $T $P $A 
	if !([ -f "./P1.rar" ]); then
		ret=1
	elif [ $T -gt $P ] && [ $P -gt $A ]; then
		ret=1
	elif [ $T -gt $A ] && [ $P -gt $A ] && [ $T == $P ]; then
		ret=1
	fi
	#elif [ $(date_scoreless $1) -gt $(date_scoreless $3) ]; then
		#ret=0
	#elif [ $(date_scoreless $1) -gt $(date_scoreless $2) ]; then
		#ret=0
	#fi
	echo $ret
}

if [ "$(update_available $TODAY $PARSED_DATE $ARCHIVE_DATE)" = "1" ]; then
	echo Update available
	./update.sh
fi
exit 1
