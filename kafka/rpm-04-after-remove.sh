#!/bin/bash
#
#

###
### AFTER remove
###

### RPM/CentOS version (%postun)


name=kafka
user=kafka


    # upgrade
    if [ "$1" -ge 1 ]
    then
        if /sbin/service  ${name} status &>/dev/null
        then
            /sbin/service ${name} condrestart &>/dev/null
        fi
    fi

    # remove
    if [ "$1" == 0 ]
    then
        /usr/sbin/userdel ${user} &>/dev/null
    fi


# vim:ft=sh:

