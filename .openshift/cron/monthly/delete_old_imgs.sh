#!/bin/bash
find $OPENSHIFT_REPO_DIR/static/imgs/ -mtime +60 -delete
