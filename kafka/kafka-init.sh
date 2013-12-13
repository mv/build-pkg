#!/bin/sh
#
# kafka
#
# Author:	Marcus Vinicius Ferreira,   <ferreira.mv@gmail.com>
#
# chkconfig:    2345 98 02
# description:  Kafka: A high-throughput distributed messaging system.
# processname:  kafka
# pidfile:      /var/run/kafka.pid
# config:       /etc/kafka/kafka.cfg

# Source function library.
. /etc/rc.d/init.d/functions


#
# my service
#
prog="kafka"
exec="/usr/bin/kafka.sh"
user="kafka"
pid="/var/lib/${prog}/${prog}.pid"

syscfg="/etc/sysconfig/${prog}"

touch $pid && chown $user $pid

#
# my helpers
#
endnow() {
  echo "$1" && exit 1
}

sig() {
  test -s "${pid}" && kill -${1} `cat ${pid}` 2>/dev/null
}


###
### functions!
###

f_start() {
    # sanity check
    [ -f ${exec} ] || endnow "Cannot find prog: [${prog}]"

    # # Source 'prog' configuration.
    # if [ -f /etc/sysconfig/${prog} ]
    # then . /etc/sysconfig/${prog}
    # fi

    sig 0 && echo "${prog}: Already running" && exit 0

    echo
    echo -n "Starting ${prog}: "

    runuser $user -m -s /bin/bash \
    -c "${exec} -c ${syscfg} -p ${pid} start" # 2>&1 > /dev/null &
    RETVAL=$?
    if [ $RETVAL = 0 ]
    then
        echo_success
        touch /var/lock/subsys/${prog}
    else
        echo_failure
    fi
}

f_stop() {
    echo
    echo -n "Stopping ${prog}: "

    runuser $user -m -s /bin/bash \
    -c "${exec} -c ${syscfg} -p ${pid} stop" # 2>&1 > /dev/null &
    RETVAL=$?
    if [ $RETVAL = 0 ]
    then
        echo_success
        rm -f /var/lock/subsys/${prog}
    else
        echo_failure
    fi
}

f_restart() {
    f_stop
    f_start
    echo
}

f_condrestart() {
    if [ -e /var/lock/subsys/${prog} ]
    then
        f_restart
    else
        echo "Not started: ${prog}"
    fi
}

f_status() {
    status -p ${pid} ${prog}
}

###
### Do it.
###

case "$1" in
    start|stop|restart|condrestart|status)
        f_${1}
        echo
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|condrestart|status}"
        exit 1
esac

# vim:ft=sh:


