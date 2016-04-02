#!/bin/bash

minute=$(date +%M)
if [ $(($minute % 5)) -eq 0 ]; then
	#python $OPENSHIFT_REPO_DIR/promocao_items.py
fi
