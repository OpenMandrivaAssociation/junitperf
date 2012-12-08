# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Name:           junitperf
Version:        1.9.1
Release:        %mkrel 2.2.1
Epoch:          0
Summary:        JUnit extension for performance and scalability testing
License:        BSD
Group:          Development/Java
Source0:        http://www.clarkware.com/software/junitperf-1.9.1.zip
URL:            http://www.clarkware.com/software/JUnitPerf.html
BuildRequires:  ant, ant-junit, junit >= 0:3.2, java-rpmbuild >= 0:1.6, java-devel
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Requires:       jpackage-utils
Requires:       junit >= 0:3.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

# -----------------------------------------------------------------------------

%build
CLASSPATH=$(build-classpath junit) %{ant} -Dbuild.sysclasspath=first jar test javadoc

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -m 0644 dist/%{name}-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc LICENSE README docs/JUnitPerf.html
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

# -----------------------------------------------------------------------------


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.1-2.1.9mdv2011.0
+ Revision: 606119
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.1-2.1.8mdv2010.1
+ Revision: 523408
- bump release
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.9.1-2.1.5mdv2010.0
+ Revision: 425477
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:1.9.1-2.1.4mdv2009.0
+ Revision: 140829
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.9.1-2.1.4mdv2008.1
+ Revision: 120957
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.9.1-2.1.3mdv2008.0
+ Revision: 87452
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Tue Jul 03 2007 David Walluck <walluck@mandriva.org> 0:1.9.1-2.1.2mdv2008.0
+ Revision: 47401
- gcj support
- BuildRequires: java-devel
- remove Requires: java
- Import junitperf



* Thu Feb 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.9.1-2jpp.1
- Fixed per Fedora spec

* Wed Nov 09 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.9.1-1jpp
- Upgrade to 1.9.1
- Add javadoc ghost symlink and post/postun

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.8-3jpp
- Rebuild with ant-1.6.2
* Thu Mar 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.8-2jpp
- Adapted to JPackage 1.5.

* Wed Mar  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.8-1jpp
- Update to 1.8.
- Fix Group tags.
- Run unit tests during build.

* Tue Jul 16 2002 Ville Skyttä <ville.skytta at iki.fi> 1.7-1jpp
- Update to 1.7.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag.

* Mon Feb 04 2002 Guillaume Rousse <rousse@ccr.jussieu.fr> 1.6-1jpp
- first jpp release
