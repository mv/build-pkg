#!/bin/bash
#
#
#
# Marcus Vinicius Ferreira <ferreira.mv at gmail.com>
# 2013-11
#

bucket='download.mvway.com'

rpm='rpm'
srpm='srpm'

for f in *.src.rpm
do
  [ -f $f ] && echo "SOURCE rpm: [$f]"
  s3cmd sync $f s3://${bucket}/${srpm}/${f}
  s3cmd setacl --acl-public s3://${bucket}/${srpm}/${f}
done

for f in *.rpm
do
  [ -f $f ] && echo "rpm: [$f]"
  s3cmd sync $f s3://${bucket}/${rpm}/${f}
  s3cmd setacl --acl-public s3://${bucket}/${rpm}/${f}
done


# vim:ft=sh:

