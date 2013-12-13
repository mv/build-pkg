#!/bin/bash

export maintainer="Marcus Vinicius Ferreira <ferreira.mv@gmail.com>"
export     vendor="mv (http://about.me/ferreira.mv)"

    gem="capistrano_colors"
release='1.mv'

./fpm-install.sh $gem $release

# vim:ft=sh:

