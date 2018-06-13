#!/bin/bash

#
# http://psumods.co.uk/viewtopic.php?f=4&t=206
#

set -e

pushd `dirname $0` > /dev/null
MAIN_PATH=`pwd -P`
popd > /dev/null


alias errcho='>&2 echo'

PATCHLIST="${MAIN_PATH}/patch_prod/translation/patchlist.txt"

PATCH_PAGE_URL="https://pso2.acf.me.uk/Manual/"
#PATCH_BASE_URL="https://pso2.acf.me.uk/Manual/index.php?8613985ec49eb8f757ae6439e879bb2a="

PATCH_PAGE="$(curl -s "${PATCH_PAGE_URL}"| sed -r 's/<br ?\/?>/\n/gi')"

TODAY="$(date +"%Y_%m_%d")"


cd ${MAIN_PATH}

function get_link() {
	echo $PATCH_PAGE | sed -r "s/.*(<a href=\"?([^\">]+)\"?>$1<\/a>).*/\\2/i"
}

function parse_date_frompatch() {
	D="$(echo $1 | sed -r 's/.+patch_([0-9]+)_([0-9]+)_([0-9]+)\..+/\1\/\2\/\3/gi')"
	#D="$(echo $1 | sed -r 's/.*patch_([0-9]+)_([0-9]+)_([0-9]+)\.zip/\1\/\2\/\3/gi')"
	date -d "$D"  +"%Y_%m_%d"
}

function date_scoreless() {
	echo $1 | sed 's/_//g'
}

function update_available() {
	ret=0
	T="$(date_scoreless $1)"
	P="$(date_scoreless $2)"
	A="$(date_scoreless $3)"

	#echo T:$T P:$P A:$A 
	#>&2 echo $T $P $A 
	if !([ -f "${PATCHLIST}" ]); then
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
if [ -f "${PATCHLIST}" ]; then
	ARCHIVE_DATE="$(date -d"$(stat ${PATCHLIST} |grep Modify|cut -d' ' -f2-)" +"%Y_%m_%d")"
	echo "${PATCHLIST}: $ARCHIVE_DATE"
else
	echo No patchlist.txt file, go ahead and install it
fi

if [ "$(update_available $TODAY $PARSED_DATE $ARCHIVE_DATE)" = "1" ]; then
	echo Update available
	./update_translation.sh
fi
exit 1
