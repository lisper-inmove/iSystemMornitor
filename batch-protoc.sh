#!/bin/bash
path="`pwd`/proto"
ipath=`pwd`

function walk() {
    for d in `find ${1}`
    do
        if [[ $d = $1 ]];then
            continue
        elif [[ -f $d ]];then
            if [[ ${d#*.} = "proto" ]];then
                `protoc $d --python_out=. -I${ipath}`
            fi
        elif [[ -d $d ]];then
            walk $d
        fi
    done
}

walk $path
