#!/bin/bash

pushd `dirname $0` > /dev/null
MAIN_PATH=`pwd -P`
popd > /dev/null

cd "${MAIN_PATH}"

./main.py
./checktranslation.sh
