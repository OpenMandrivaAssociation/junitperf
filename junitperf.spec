%{?_javapackages_macros:%_javapackages_macros}
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

Name:           junitperf
Version:        1.9.1
Release:        15.1
Summary:        JUnit extension for performance and scalability testing
Group:		Development/Java
License:        BSD
Source0:        http://www.clarkware.com/software/junitperf-1.9.1.zip
Source1:        https://repository.jboss.org/nexus/content/repositories/thirdparty-uploads/junitperf/junitperf/%{version}/junitperf-%{version}.pom
URL:            http://www.clarkware.com/software/JUnitPerf.html
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-devel
BuildRequires:  javapackages-local
BuildRequires:  junit >= 3.2
BuildArch:      noarch
Requires:       junit >= 3.2

%description
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
%{summary}.

%package demo
Summary:        Demos and samples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
%{summary}.

%prep
%setup -q -n %{name}-%{version}

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%build
CLASSPATH=$(build-classpath junit) ant -Dbuild.sysclasspath=first jar test javadoc

# request maven artifact installation
%mvn_artifact %{SOURCE1} dist/junitperf-%{version}.jar

%install
%mvn_install

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -pr samples %{buildroot}%{_datadir}/%{name}

%files -f .mfiles
%doc LICENSE README docs/JUnitPerf.html
%dir %{_javadir}/%{name}

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%files demo
%doc LICENSE
%{_datadir}/%{name}

%changelog
* Mon Jun 09 2014 Mat Booth <mat.booth@redhat.com> - 1.9.1-15
- Install with maven
- Fix bogus date in changelog
- Drop ancient javadoc/rpm bug workaround

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.9.1-13
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 gil cattaneo <puntogil@libero.it> - 1.9.1-9
- added maven pom (#819199)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 31 2011 Mat Booth <fedora@matbooth.co.uk> 1.9.1-6
- Update for latest Java guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.9.1-2.2
- drop repotag

* Thu Feb 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.9.1-2jpp.1
- Fixed per Fedora spec

* Wed Nov 09 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.9.1-1jpp
- Upgrade to 1.9.1
- Add javadoc ghost symlink and post/postun

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.8-3jpp
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
