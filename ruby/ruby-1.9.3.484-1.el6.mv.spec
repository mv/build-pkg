###
### SECTION: Macros: pre-reqs
###

# Ignoring automatic setting of 'provides'
# (I will manually set any of them below)
%define __find_provides   %{nil}

# Ignoring automatic setting of requirements
%define __find_requires   %{nil}
%define _use_internal_dependency_generator           0

#define _binaries_in_noarch_packages_terminate_build 0
#define _missing_doc_files_terminate_build           0
%define _unpackaged_files_terminate_build            0
#define _transaction_color                           1

#define packager    %{getenv:RPM_PACKAGER}
#define packager    %{_gpg_name}
%define vendor      Mv (http://about.me/ferreira.mv)
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

# list of files
%define list_of_files %{_srcrpmdir}/%{name}-%{version}-%{release}.txt

###
### SECTION: Introduction
###

# this build
%define ruby_version  1.9.3
%define patchlevel    484
%define release       1

Name:    ruby
Version: %{ruby_version}.%{patchlevel}
Release: %{release}%{?dist}

%define irb_version       %{ruby_version}.%{patchlevel}
%define rake_version       0.9.2.2
%define rdoc_version       3.9.5
%define minitest_version   2.5.1
%define json_version       1.5.5
%define io_console_version 0.3
%define bigdecimal_version 1.1.0

%define rubygems_version   1.8.23

%define ruby_abi           1.9.1
%define ruby_archive %{name}-%{ruby_version}-p%{patchlevel}

Source: http://cache.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p484.tar.gz

Provides: %{name}
Provides: ruby(abi) = %{ruby_abi}

Provides: ruby-libs, ruby-devel
Provides: rubygems, rubygems-devel

Provides: ri = %{version}-%{release}

Provides: gem = %{version}-%{release}
Provides: ruby(rubygems) = %{version}-%{release}

#rovides: irb = %{irb_version}
#rovides: ruby(irb) = %{irb_version}

#rovides: rake = %{rake_version}
#rovides: rdoc = %{rdoc_version}
#rovides: rubygem(rake) = %{rake_version}
#rovides: rubygem(rdoc) = %{rdoc_version}

#rovides: rubygem(bigdecimal) = %{bigdecimal_version}
#rovides: rubygem(io-console) = %{io_console_version}
#rovides: rubygem(json) = %{json_version}
#rovides: rubygem(minitest) = %{minitest_version}

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc, make, autoconf
BuildRequires: zlib-devel, openssl-devel
BuildRequires: gdbm-devel, db4-devel, libffi-devel, libyaml-devel, readline-devel
BuildRequires: ncurses-devel, tk-devel
BuildRequires: procps
BuildRequires: libxml2, libxml2-devel
BuildRequires: libxslt, libxslt-devel
BuildRequires: libyaml

# This was set manually after a test install...
Requires: libyaml
Requires: libc.so.6()(64bit)
Requires: rpmlib(CompressedFileNames) <= 3.0.4-1
Requires: rpmlib(PartialHardlinkSets) <= 4.0.4-1
Requires: rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires: rtld(GNU_HASH)

Packager: %{_gpg_name}
Vendor:   %{vendor}

Group:    Development/Languages
Summary:  Ruby - An object-oriented scripting language
URL:      http://ruby-lang.org/
License:  (Ruby or BSD) and Public Domain

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.



###
### SECTION: Prepare
###

%prep

%setup -q -n %{ruby_archive}

#   echo "prep: $(pwd) "  > /tmp/pwd.log
#   /bin/cp %{SOURCE1} .

###
### SECTION: Build
###

%build

#   echo "build: $(pwd) " >> /tmp/pwd.log

#define optflags -O2 -g
#define optflags -O2 -march=native -pipe
#define optflags -O2 -march=native # native: bug on gcc: Illegal instruction
%define optflags -O2

    %{configure} \
        --enable-shared           \
        --disable-pthread         \
        --disable-install-doc     \
        --disable-rpath           \
        2>&1 | tee %{_builddir}/%{name}-%{version}-configure.my.log

    make %{?_smp_mflags}
        2>&1 | tee %{_builddir}/%{name}-%{version}-make.my.log


###
### SECTION: Install
###

%install

    rm -rf $RPM_BUILD_ROOT

    # no doc for system ruby, please.
    HOME_ROOT="$(echo ~root)"
    mkdir -p ${RPM_BUILD_ROOT}/${HOME_ROOT}
    printf "#\ngem: --no-ri --no-rdoc\n\n" > ${RPM_BUILD_ROOT}/${HOME_ROOT}/.gemrc

    # install, please...
    make install DESTDIR=$RPM_BUILD_ROOT \
         2>&1 | tee %{_builddir}/%{name}-%{version}-make.my.install.log

#   # end-of-install: get list of files
#   cd %{buildroot}
#   find * > %{list_of_files}


###
### SECTION: Clean up
###

%clean

#   echo "clean: $(pwd) " >> /tmp/pwd.log

    # bye,bye tmp-installed-tree....
    %{__rm} -rf $RPM_BUILD_ROOT

    # final rpm: up one level
    %{__mv} %{_rpmdir}/%{_arch}/*.rpm %{_rpmdir}

    # after one level up: remove dir
    rmdir   %{_rpmdir}/%{_arch} || :

###
### SECTION: Files
###

#files -f %{list_of_files}
%files
%defattr(-,root,root,-)

%{_bindir}/ri
%{_bindir}/rdoc
%{_bindir}/ruby
%{_bindir}/testrb

%{_bindir}/erb
%{_bindir}/gem
%{_bindir}/irb
#{_bindir}/rake

%{_includedir}/*
#{_includedir}/ruby-%{ruby_abi}

%{_libdir}/libruby*
%{_libdir}/pkgconfig/ruby*pc
%{_libdir}/ruby/%{ruby_abi}
%{_libdir}/ruby/site_ruby/%{ruby_abi}
%{_libdir}/ruby/vendor_ruby/%{ruby_abi}
%{_libdir}/ruby/gems


%{_mandir}/man1/erb*
%{_mandir}/man1/irb*
%{_mandir}/man1/rake*
%{_mandir}/man1/ri*
%{_mandir}/man1/ruby*

%config(noreplace) /root/.gemrc

%doc ChangeLog README COPYING GPL LEGAL
%doc README.EXT
%doc NEWS
%doc doc/NEWS-*
%doc doc/ChangeLog-*
%lang(ja) %doc README.ja
%lang(ja) %doc COPYING.ja
%lang(ja) %doc README.EXT.ja


###
### SECTION: History of this spec
###

%changelog
* Thu Nov 21 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-484-1
- Heap Overflow in Floating Point Parsing (CVE-2013-4164)

* Thu Nov 12 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-448-2
- not using "optflags: -march=native"

* Thu Jun 27 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-448.

* Sat Feb 23 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-392.

* Wed Feb 05 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-385.

* Tue Jan 17 2013 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-374.

* Tue Dec 25 2012 Marcus Vinicius Ferreira <ferreira.mv@gmail.com>
- ruby 1.9.3-362.
- ruby by edenbr.

# vim:ft=spec:

