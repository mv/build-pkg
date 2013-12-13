#!/bin/bash
#
# fpm: Java: building a package
#
# Marcus Vinicius Ferreira          ferreira.mv[ at ]gmail.com
# 2013-11
#

usage() {
  echo
  echo "$0 [rpm|deb]"
  echo
  echo "    Uses fpm to build a package. Default: rpm"
  echo
  exit 1
}

target="$1"
target=${target:-rpm}


pkg="kafka"
ver="0.8.0"
rel='1.mv'

work_dir=/tmp/work/
build_dir=/tmp/build/${pkg}-${ver}

src_dir=${work_dir}/${pkg}-${ver}
pkg_dir=${build_dir}/opt/${pkg}

src="./src/${pkg}_2.8.0-${ver}-beta1.tgz"
url="https://kafka.apache.org/downloads.html"
descr="Kafka: A high-throughput distributed messaging system."

maintainer="Marcus Vinicius Ferreira <ferreira.mv@gmail.com>"
vendor="Mv (https://github.com/mv/build-pkg)"


# prep
set -e

mkdir -p $src_dir
tar xvfz ${src} -C ${src_dir} 2>&1>/dev/null

# fix after opening tar file
tar_name=${src##*/}
tar_name=${tar_name%.*}
src_dir=${src_dir}/${tar_name}


# build

  install -d -m0755 ${build_dir}
  install -d -m0755 ${build_dir}/opt/${pkg}/bin
  install -d -m0755 ${build_dir}/opt/${pkg}/libs
  install -d -m0755 ${build_dir}/opt/${pkg}/config
  install -d -m0755 ${build_dir}/var/lib/${pkg}/data
  install -d -m0755 ${build_dir}/var/log/${pkg}/metrics
  install -d -m0755 ${build_dir}/etc/${pkg}
  install -d -m0755 ${build_dir}/etc/init.d
  install -d -m0755 ${build_dir}/etc/sysconfig
  install -d -m0755 ${build_dir}/usr/bin


# install

  # scripts
  /bin/cp ${src_dir}/bin/*.sh    ${pkg_dir}/bin/
  chmod 0755                     ${pkg_dir}/bin/{kafka,run}*.sh
  chmod 0644                     ${pkg_dir}/bin/zookeeper*.sh

  # jar
  /bin/cp ${src_dir}/*.jar       ${pkg_dir}/
  /bin/cp ${src_dir}/libs/*.jar  ${pkg_dir}/libs/
  chmod 0644                     ${pkg_dir}/*.jar ${pkg_dir}/libs/*.jar

  # configs
  /bin/cp ${src_dir}/config/*.properties   ${pkg_dir}/config/
  chmod 0644                               ${pkg_dir}/config/*.properties

  install -Dp -m0644 ./server.properties   ${build_dir}/etc/${pkg}/kafka.cfg
  install -Dp -m0644 ./log4j.properties    ${build_dir}/etc/${pkg}/kafka-log.cfg

  # extras
  install -Dp -m0755 ./kafka-init.sh       ${build_dir}/etc/init.d/kafka
  install -Dp -m0755 ./kafka-sysconfig.sh  ${build_dir}/etc/sysconfig/kafka
  install -Dp -m0755 ./kafka.sh            ${build_dir}/usr/bin/kafka.sh



# package!
set -x

  fpm -s dir -t $target \
      -v $ver --iteration "${rel}" -m "${maintainer}" --vendor "${vendor}" --url "${url}" \
      --config-files    opt/${pkg}/config/log4j.properties    \
      --config-files    opt/${pkg}/config/server.properties   \
      --before-install  ${target}-01-before-install.sh        \
      --after-install   ${target}-02-after-install.sh         \
      --before-remove   ${target}-03-before-remove.sh         \
      --after-remove    ${target}-04-after-remove.sh          \
      -n ${pkg}         \
      -C ${build_dir}   \
      opt etc usr var


# Cleanup
#/bin/rm -rf ${build_dir}

# vim:ft=sh

