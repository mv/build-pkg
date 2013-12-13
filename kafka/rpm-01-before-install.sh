#!/bin/bash
#
#

###
### BEFORE install
###

### RPM/CentOS version (%pre)

    # my id range
    uid=1019
    gid=1019
    com='Kafka User'
    user=kafka
    group=kafka
    shell=/sbin/nologin
    home=%{_sharedstatedir}/$user

    /usr/sbin/groupadd -g $gid $group &>/dev/null || :
    /usr/sbin/useradd  -g $gid -u $uid -c "$com" -s $shell -r -d $home $user &>/dev/null || :

# vim:ft=sh:

