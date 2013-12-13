#!/bin/bash
#
# puppet
#
#    This is a separate script so I can set dependencies.
#
#
# Marcus Vinicius Fereira            ferreira.mv[ at ].gmail.com
# 2013-01
#

export maintainer="Marcus Vinicius Ferreira <ferreira.mv@gmail.com>"
export     vendor="mv (http://about.me/ferreira.mv)"

    gem="puppet"
release='1.mv'

before_script=$( /bin/mktemp )

cat > $before_script <<'CAT'

    # edenbr id range
    gid=1015
    group=puppet

    /usr/sbin/groupadd -g $gid $group &>/dev/null || :
    #

CAT


# workdir
dir=tmp_gems_${gem}
mkdir -p ${dir}

# download all gems
gem install --no-ri --no-rdoc --install-dir $dir $gem

# package all gems found inside 'cache' dir
fpm -s gem -t rpm --verbose \
    -m               "$maintainer"    \
    --vendor         "$vendor"        \
    --iteration      "$release"       \
    --before-install $before_script   \
    --provides       'puppet'         \
    ${dir}/cache/puppet*gem


fpm_gem() {
  fpm -s gem -t rpm --verbose \
      -m               "$maintainer"    \
      --vendor         "$vendor"        \
      --iteration      "$release"       \
      --provides       "${1}"           \
      ${dir}/cache/${1}*gem
}

fpm_gem facter
fpm_gem hiera
fpm_gem json_pure
fpm_gem rgen

# /bin/rm -rf $before_script

# vim:ft=sh:

