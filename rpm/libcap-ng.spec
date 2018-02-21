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

%define python3_sitearch /%{_libdir}/python3.?/site-packages

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
make DESTDIR="${RPM_BUILD_ROOT}" INSTALL='install -p' install

# Move the symlink
rm -f $RPM_BUILD_ROOT/%{_lib}/%{name}.so
mkdir -p $RPM_BUILD_ROOT%{_libdir}
VLIBNAME=$(ls $RPM_BUILD_ROOT/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME $RPM_BUILD_ROOT%{_libdir}/%{name}.so

# Move the pkgconfig file
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

# Remove a couple things so they don't get picked up
rm -f $RPM_BUILD_ROOT/%{_lib}/libcap-ng.la
rm -f $RPM_BUILD_ROOT/%{_lib}/libcap-ng.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_capng.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/python?.?/site-packages/_capng.la

%check
# test fails due to wrong linking path to shared libs. hopefully ok otherwise
#make check

%post
/sbin/ldconfig

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
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*

%changelog
* Wed Feb 07 2018 Steve Grubb <sgrubb@redhat.com> 0.7.9-1
- New upstream bugfix release

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.8-9
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.8-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.8-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.8-6
- Python 2 binary package renamed to python2-libcap-ng
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.8-2
- Rebuild for Python 3.6

* Sun Jul 24 2016 Steve Grubb <sgrubb@redhat.com> 0.7.8-1
- New upstream bugfix release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Steve Grubb <sgrubb@redhat.com> 0.7.7-4
- use python site arch macros (#1303610)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Steve Grubb <sgrubb@redhat.com> 0.7.7-1
- New upstream bugfix release

* Fri May 08 2015 Steve Grubb <sgrubb@redhat.com> 0.7.6-1
- New upstream release adding python3 support

* Thu May 07 2015 Steve Grubb <sgrubb@redhat.com> 0.7.5-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 0.7.4-6
- fix license handling

* Mon Jun 23 2014 Kyle McMartin <kyle@redhat.com> 0.7.4-5
- Clamp CAP_LAST_CAP at /proc/sys/kernel/cap_last_cap's value in the
  Python bindings test if possible, otherwise use the value from
  <linux/capability.h> since the kernel now has 37 capabilities upstream,
  but our builders are not that up to date.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-3
- Add PR_SET_NO_NEW_PRIVS call back to capng_lock

* Wed Apr 30 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-2
- Remove PR_SET_NO_NEW_PRIVS call in capng_lock

* Thu Apr 24 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-1
- New upstream release

* Thu Nov 14 2013 Steve Grubb <sgrubb@redhat.com> 0.7.3-6
- Rebuild to pickup current CAP_LAST_CAP

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Karsten Hopp <karsten@redhat.com> 0.7.3-4
- bump release and rebuild to fix dependencies on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-2
- Remove useless code in pscap causing EBADFD

* Fri Nov 09 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-1
- New upstream release

* Wed Oct 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7.1-1
- New upstream release

* Tue Jul 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 0.6.6-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Steve Grubb <sgrubb@redhat.com> 0.6.5-1
- New upstream release fixing 2.6.36 kernel header issue

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-3
- Only open regular files in filecap

* Mon May 24 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-2
- In utils subpackage added a requires statement.

* Thu May 06 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-1
- New upstream release fixing multi-threading issue

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-2
- filecap shows full capabilities if a file has any

* Thu Mar 11 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-1
- New upstream release

* Tue Feb 16 2010 Steve Grubb <sgrubb@redhat.com> 0.6.2-4
- Use global macro and require pkgconfig for devel subpackage

* Fri Oct 09 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-3
- Apply patch to retain setpcap only if clearing bounding set

* Sat Oct 03 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-2
- Apply patch correcting pscap and netcap acct detection

* Mon Sep 28 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-1
- New upstream release

* Sun Jul 26 2009 Steve Grubb <sgrubb@redhat.com> 0.6.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Steve Grubb <sgrubb@redhat.com> 0.6-1
- New upstream release

* Sun Jun 21 2009 Steve Grubb <sgrubb@redhat.com> 0.5.1-1
- New upstream release

* Fri Jun 19 2009 Steve Grubb <sgrubb@redhat.com> 0.5-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.2-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.1-1
- Initial build.

