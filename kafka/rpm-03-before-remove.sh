#!/bin/bash
#
#

###
### BEFORE remove
###

### RPM/CentOS version (%preun)


name=kafka

    # stop and remove service
    if [ "$1" == 0 ]
    then
        /sbin/chkconfig --del ${name}
        /sbin/service ${name} stop &>/dev/null
    fi


# vim:ft=sh:


