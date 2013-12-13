#!/bin/sh
#
# kafka
#
# Author:   Marcus Vinicius Ferreira,   <ferreira.mv@gmail.com>
#

###
### defaults
###
user="kafka"
prog="kafka"
pid="/tmp/${prog}.pid"
syscfg="/etc/sysconfig/${prog}"

###
### script options
###
usage() {
    echo
    echo "Usage: $0 [-p pidfile] [-c sysconfigfile] start|stop|restart|status"
    echo
    echo "    sysconfigfile: '/etc/sysconfig/file' or similar containing"
    echo "                   environment variables to be used by this start/stop"
    echo "                   script."
    echo
    exit 1
}

[ -z "$1" ] && usage

while [ "$1" != "" ]
do
    case "$1" in
        start|stop|restart|status)
            action="f_${1}"
            shift
            ;;
        -c)
            syscfg="$2"
            shift 2
            ;;
        -p)
            pid="$2"
            shift 2
            ;;
        *)
            usage
    esac
done

# must not be null
[ $action ] || usage

# use it
if [ -f ${syscfg} ]
then
    logger -i -t $0 "sysconfigfile: [$syscfg]"
    source $syscfg
else
    logger -i -t $0 "sysconfigfile: NOT FOUND: [$syscfg]"
fi


#
# my helpers
#
endnow() {
  echo "$1" && exit 1
}

sig() {
  test -s "${pid}" && kill -${1} `cat ${pid}` 2>/dev/null
}

log() {
  logger -i -t $0 "$@"
}


###
### Specifics
###

basedir="/opt/${prog}"

scala_version=2.8.0

# classpath addition for release
CLASSPATH=/opt/kafka/config
for file in ${basedir}/libs/*.jar ${basedir}/kafka*.jar
do
    #echo $file
    [ -f $file ] && CLASSPATH=$CLASSPATH:$file
done
CLASSPATH=${CLASSPATH}:/etc/kafka
CLASSPATH=${CLASSPATH}:/opt/kafka/config

JVMFLAGS=${JVMFLAGS:-"-Xmx512M"}

JMX_PORT=${JMX_PORT:-9999}
jmx="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false  -Dcom.sun.management.jmxremote.ssl=false"
jmx="${jmx} -Dcom.sun.management.jmxremote.port=${JMX_PORT}"

LOG_DIR=${LOG_DIR:-"/tmp"}

CFG_FILE=${CFG_FILE:-"config/server.properties"}

LOG4J_FILE=${LOG4J_FILE:-"conf/log4j.properties"}

[ -e $LOG_DIR ]    || logger -i -t $0 "log dir: DOES NOT EXIST [$LOG_DIR]"
[ -e $CFG_FILE ]   || logger -i -t $0 "cfg file: DOES NOT EXIST [$CFG_FILE]"
[ -e $LOG4J_FILE ] || logger -i -t $0 "log4j file: DOES NOT EXIST [$LOG4J_FILE]"

###
### Kafka stuff
###

#onf="${basedir}/config/server.properties"
conf="${CFG_FILE}"

logp="-Dkafka.log.dir=${LOG_DIR}"
logp="${logp} -Dlog4j.configuration=file:///etc/kafka/kafka-log.cfg"

main="kafka.Kafka"


###
### Tasks
###

f_start() {
    sig 0 && echo "Already running" && exit 0

    logger -i -t $0 "Starting ${prog}. "
    if ! touch ${pid}
    then
        logger -i -t $0 "pidfile: CANNOT CREATE: [$pid]"
        exit 3
    fi

    logger -i -t $0 \
    "java ${JVMFLAGS} -server ${logp} ${jmx} -cp ${CLASSPATH} ${main} ${conf}"

    # scenario 2: java program does not daemonize by itself
    java ${JVMFLAGS} -server ${logp} ${jmx} -cp ${CLASSPATH} ${main} ${conf} \
         2>&1 > /dev/null &
    echo $! > ${pid}
}

f_stop() {
    if sig 0
    then
        log "Stopping... "
        sig TERM && log "Stop OK."
    else
        log "Stopped."
        /bin/rm -f ${pid}
        exit 0
    fi

    # just in case
    log "Sleeping..."
    sleep 2
    f_stop
}

f_restart() {
    f_stop
    f_start
}

f_status() {
    if [ ! -f ${pid} ]
    then
        echo "Pidfile does not exist: [${pid}]"
        exit
    fi

    if sig 0
    then
        echo "${prog} is running with pid: [$(cat ${pid})]"
    else
        echo "${prog} error: cannot find process."
    fi
}


###
### Main
###

# echo "action: [$action]"
# echo "syscfg: [$syscfg]"
# echo "   pid: [$pid]"

$action


# vim:ft=sh:

