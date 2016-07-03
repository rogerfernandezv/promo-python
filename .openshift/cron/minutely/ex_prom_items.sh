#!/bin/bash

minute=$(date +%M)
#minute2=echo $minute | sed -e 's/^0//'

if [ $(($minute % 3)) -eq 0 ]; then
	python $OPENSHIFT_REPO_DIR/promocao_items.py
fi
