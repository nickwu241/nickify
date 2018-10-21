#!/bin/sh

rsync --filter=':- .gitignore' -ave ssh /Users/nickwu/src/github.com/nickwu241/nickify "$(terraform output ip)":~/