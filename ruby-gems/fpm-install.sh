#!/bin/bash
#
# fpm-install.sh
#
#    Uses fpm to create a rpm package for
#    a gem and its dependencies
#
#
# Marcus Vinicius Fereira            ferreira.mv[ at ].gmail.com
# 2013-01
#


[ -z "$2" ] && {

    echo
    echo "Usage: $0  gem_name  pkg_release"
    echo
    echo "    fpm: rpm create 'gem_name' using 'pkg_release'"
    echo
    exit 1

}

gem="$1"
iteration="$2"

epoch=1

# workdir
dir=./tmp_gems_${gem}
mkdir -p ${dir}

# download all gems
gem install --no-ri --no-rdoc --install-dir $dir $gem

# package all gems found inside 'cache' dir
find ${dir}/cache -name '*.gem' | while read gem_file
do

  fpm -s gem -t rpm --verbose \
      -m            "$maintainer" \
      --vendor      "$vendor"     \
      --iteration   "$iteration"  \
      --epoch       "$epoch"      \
      --provides    "${gem}"      \
      $gem_file

done

# /bin/mv ${dir} ${dir}_$( /bin/date +'%F_%X' )
/bin/rm -rf $dir

# vim:ft=sh:

