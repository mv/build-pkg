#!/bin/bash
#
#

###
### AFTER install
###

### RPM/CentOS version (%post)


name=kafka

user=kafka
group=kafka


    # add service
    /sbin/service   ${name} start
    /sbin/chkconfig --add ${name}
    /sbin/chkconfig --level 2345 ${name} on

    # enforce permissions
    chown -R ${user}:${group}  /var/lib/kafka
    chown -R ${user}:${group}  /var/log/kafka


# vim:ft=sh:


