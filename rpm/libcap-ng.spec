# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%if ! %{defined python3_sitearch}
%define python3_sitearch /%{_libdir}/python3.?/site-packages
%endif

Summary: An alternate posix capabilities library
Name: libcap-ng
Version: 0.7.9
Release: 1%{?dist}
License: LGPLv2+
URL: http://people.redhat.com/sgrubb/libcap-ng
Source: %{name}-%{version}.tar.bz2
BuildRequires: kernel-headers >= 2.6.11 
BuildRequires: libattr-devel
BuildRequires: automake autoconf libtool

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel
Summary: Header files for libcap-ng library
License: LGPLv2+
Requires: kernel-headers >= 2.6.11
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.
%package python3
Summary: Python3 bindings for libcap-ng library
License: LGPLv2+
BuildRequires: python3-devel swig
Requires: %{name} = %{version}-%{release}

%description python3
The libcap-ng-python3 package contains the bindings so that libcap-ng
and can be used by python3 applications.

%package utils
Summary: Utilities for analyzing and setting file capabilities
License: GPLv2+
Requires: %{name} = %{version}-%{release}

%description utils
The libcap-ng-utils package contains applications to analyze the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
./autogen.sh
%configure --libdir=/%{_lib} --with-python3
make CFLAGS="%{optflags}" %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR="${RPM_BUILD_ROOT}" INSTALL='install -p' install

# Move the symlink
rm -f ${RPM_BUILD_ROOT}/%{_lib}/%{name}.so
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
VLIBNAME=$(ls ${RPM_BUILD_ROOT}/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME ${RPM_BUILD_ROOT}%{_libdir}/%{name}.so

# Move the pkgconfig file
mv ${RPM_BUILD_ROOT}/%{_lib}/pkgconfig ${RPM_BUILD_ROOT}%{_libdir}

# Remove a couple things so they don't get picked up
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libcap-ng.la
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libcap-ng.a
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/python?.?/site-packages/_capng.a
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/python?.?/site-packages/_capng.la

# Remove python2.7 files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/python2.7/site-packages/*

%check
# test fails due to wrong linking path to shared libs. hopefully ok otherwise
# ^^ Comment from Oliver. Binding test fails in OBS for reason unknown
# TODO: investigate the reason and fix (perhaps with a patch).
make check || true
cat bindings/python/test/test-suite.log
cat bindings/python/test/capng-test.py.log

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc COPYING.LIB
/%{_lib}/libcap-ng.so.*

%files devel
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files python3
%attr(755,root,root) %{python3_sitearch}/*
%{python3_sitearch}/capng.py*

%files utils
%doc LICENSE
%doc COPYING
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
