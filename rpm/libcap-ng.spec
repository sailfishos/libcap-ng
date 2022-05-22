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

Summary: An alternate posix capabilities library
Name: libcap-ng
Version: 0.8.3
Release: 1
License: LGPLv2+
URL: http://people.redhat.com/sgrubb/libcap-ng
Source: %{name}-%{version}.tar.bz2
BuildRequires: kernel-headers >= 2.6.11 
BuildRequires: libattr-devel
BuildRequires: automake autoconf libtool
BuildRequires: python3-base

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel
Summary: Header files for libcap-ng library
Requires: kernel-headers >= 2.6.11
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.
%package python3
Summary: Python3 bindings for libcap-ng library
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
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
./autogen.sh
%configure --libdir=/%{_libdir} --with-python=no --with-python3
%make_build

%install
%make_install

# Remove a couple things so they don't get picked up
rm -f $RPM_BUILD_ROOT%{_libdir}/libcap-ng.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libcap-ng.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{python3_version}/site-packages/_capng.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{python3_version}/site-packages/_capng.la


%check
make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%{_libdir}/libcap-ng.so.*
%{_libdir}/libdrop_ambient.so.*
%attr(0644,root,root) %{_mandir}/man7/*

%files devel
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_libdir}/libdrop_ambient.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files python3
%attr(755,root,root) %{python3_sitearch}/*
%{python3_sitearch}/capng.py*

%files utils
%license COPYING
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
