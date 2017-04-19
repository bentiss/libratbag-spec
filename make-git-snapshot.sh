#!/bin/sh

DIRNAME=libratbag-$( date +%Y%m%d )

rm -rf $DIRNAME
git clone https://github.com/libratbag/libratbag $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git log | head -1
else
    git checkout $1
fi
COMMIT_ID=$(git log | head -1 | awk '{ print $2 }')
echo ${COMMIT_ID} > ../commitid
echo ${COMMIT_ID:0:9} >> ../commitid
git repack -a -d
cd ..
tar jcf $DIRNAME.tar.xz $DIRNAME
rm -rf $DIRNAME
