###
### SECTION: Macros: pre-reqs
###

# Ignoring automatic setting of requirements
# (I will manually set requirements below)
%define __find_requires   %{nil}
%define _use_internal_dependency_generator           0

#define _binaries_in_noarch_packages_terminate_build 0
#define _missing_doc_files_terminate_build           0
#define _unpackaged_files_terminate_build            0
#define _transaction_color                           1

#define packager    %{getenv:RPM_PACKAGER}
#define packager    %{_gpg_name}
%define vendor      mv (http://about.me/ferreira.mv)
%define vendor_tag  mv

# if rhel: rhel5 define el5, rhel5 define el6, ....
%define dist        %{?rhel:.el%{rhel}}.%{vendor_tag}

# centos: replacing 'unknown' for 'redhat' as a target
%if %{centos}
%define _host        x86_64-redhat-linux-gnu
%define _host_vendor redhat
%endif


# building using a vagrant machine
%define _specdir    /vagrant/%{name}
%define _sourcedir  /vagrant/%{name}/src
%define _rpmdir     /vagrant/%{name}
%define _srcrpmdir  /vagrant/%{name}


###
### SECTION: Introduction
###

# this build
%define version 3.4.5
%define release 1
#define _arch noarch
%define user  zk

Name:    zookeeper
Version: %{version}
Release: %{release}%{?dist}

Provides: %{name}

Source0:  http://ftp.unicamp.br/pub/apache/zookeeper/%{name}-%{version}.tar.gz
Source1:  zoo.cfg
Source2:  log4j.properties

Source3:  zookeeper-sysconfig.sh
Source4:  zookeeper-init.sh
Source5:  zookeeper.sh

Source6:  zkEnv.sh
Source7:  zktop.py
#ource8:  zookeeper-monit.conf


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: make, sed


# This was set manually after a test install...
#equires: rpmlib(CompressedFileNames) <= 3.0.4-1
#equires: rpmlib(PartialHardlinkSets) <= 4.0.4-1
#equires: rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires: rtld(GNU_HASH)


Packager: %{_gpg_name}
Vendor:   %{vendor}

Group:    Applications/System
Summary:  A high-performance coordination service for distributed applications
URL:      http://zookeeper.apache.org/
License:  APL2

%description
ZooKeeper: Because Coordinating Distributed Systems is a Zoo

ZooKeeper is a high-performance coordination service for distributed
applications. It exposes common services - such as naming, configuration
management, synchronization, and group services - in a simple interface so you
don't have to write them from scratch. You can use it off-the-shelf to
implement consensus, group management, leader election, and presence protocols.
And you can build on it for your own, specific needs.


###
### SECTION: Prepare
###

%prep

%setup -q



###
### SECTION: Build
###

%build

    # A '.jar' file is already built. But I must create the dirtree that
    # will hold this file, its configs, its log files and remaining
    # artifacts

    mkdir -p %{buildroot}%{_bindir}
    mkdir -p %{buildroot}%{_prefix}/lib/%{name}
    mkdir -p %{buildroot}%{_sysconfdir}/%{name}
    mkdir -p %{buildroot}%{_initrddir}
    mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
    mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
    mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/txlog
#   mkdir -p %{buildroot}%{_mandir}/man1



###
### SECTION: Install
###

%install

    %{__install} -Dp -m0644 dist-maven/%{name}-%{version}.jar   %{buildroot}%{_prefix}/lib/%{name}/
    %{__install} -Dp -m0644 lib/jline*.jar                      %{buildroot}%{_prefix}/lib/%{name}/
    %{__install} -Dp -m0644 lib/log4j*.jar                      %{buildroot}%{_prefix}/lib/%{name}/
    %{__install} -Dp -m0644 lib/netty*.jar                      %{buildroot}%{_prefix}/lib/%{name}/
    %{__install} -Dp -m0644 lib/slf4j*.jar                      %{buildroot}%{_prefix}/lib/%{name}/

    %{__install} -Dp -m0644 conf/configuration.xsl  %{buildroot}%{_sysconfdir}/%{name}/
    %{__install} -Dp -m0644 %{SOURCE1}              %{buildroot}%{_sysconfdir}/%{name}/
    %{__install} -Dp -m0644 %{SOURCE2}              %{buildroot}%{_sysconfdir}/%{name}/

    %{__install} -Dp -m0644 %{SOURCE3}              %{buildroot}%{_sysconfdir}/sysconfig/%{name}
    %{__install} -Dp -m0755 %{SOURCE4}              %{buildroot}%{_initrddir}/%{name}
    %{__install} -Dp -m0755 %{SOURCE5}              %{buildroot}%{_bindir}/

    # extras:
    %{__install} -Dp -m0755 bin/zkCleanup.sh  %{buildroot}%{_bindir}/
    %{__install} -Dp -m0755 bin/zkCli.sh      %{buildroot}%{_bindir}/
    %{__install} -Dp -m0644 bin/zkServer.sh   %{buildroot}%{_bindir}/
    %{__install} -Dp -m0755 %{SOURCE6}        %{buildroot}%{_bindir}/
    %{__install} -Dp -m0755 %{SOURCE7}        %{buildroot}%{_bindir}/



###
### SECTION: Files
###

%files

###
# Main files
###
%defattr(-,root,root)

%{_bindir}/*
%{_initrddir}/*
%{_prefix}/lib/%{name}

%config(noreplace) %{_sysconfdir}/%{name}/zoo.cfg
%config(noreplace) %{_sysconfdir}/%{name}/configuration.xsl
%config(noreplace) %{_sysconfdir}/%{name}/log4j.properties
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%doc CHANGES.txt LICENSE.txt NOTICE.txt README.txt

%defattr( 0755, %{user}, %{user} )
%{_localstatedir}/log/%{name}
%{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/data
%{_localstatedir}/lib/%{name}/txlog

###
### SECTION: Scripts
###

%pre

    # edenbr id range
    uid=1018
    gid=1018
    com='Zookeeper User'
    user=%{user}
    group=%{user}
    shell=/sbin/nologin
    home=%{_sharedstatedir}/$user

    /usr/sbin/groupadd -g $gid $group &>/dev/null || :
    /usr/sbin/useradd  -g $gid -u $uid -c "$com" -s $shell -r -d $home $user &>/dev/null || :


%post

    # add service
    /sbin/service   %{name} start
    /sbin/chkconfig --add %{name}
    /sbin/chkconfig --level 2345 %{name} on

%preun

    # stop and remove service
    if [ "$1" == 0 ]
    then
        /sbin/chkconfig --del %{name}
        /sbin/service %{name} stop &>/dev/null
    fi


%postun

    # upgrade
    if [ "$1" -ge 1 ]
    then
        if /sbin/service  %{name} status &>/dev/null
        then
            /sbin/service %{name} condrestart &>/dev/null
        fi
    fi

    # remove
    if [ "$1" == 0 ]
    then
        /usr/sbin/userdel %{user} &>/dev/null
    fi


###
### SECTION: Clean up
###

%clean

   # bye,bye work-installed-tree....
   %{__rm} -rf %{buildroot}

   # final rpm: up one level
   %{__mv} %{_rpmdir}/%{_arch}/%{name}-%{version}-%{release}.%{_arch}.rpm %{_rpmdir}

   # after one level up: remove dir
   rmdir   %{_rpmdir}/%{_arch} || :

###
### SECTION: ChangeLog
###

%changelog
* Sat Nov 23 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- 3.4.5-1
- Zookeeper by Mv

# vim:ft=spec:

