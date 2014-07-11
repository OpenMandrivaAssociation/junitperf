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

Summary:	JUnit extension for performance and scalability testing
Name:		junitperf
Version:	1.9.1
Release:	2.2.7
License:	BSD
Group:		Development/Java
Source0:	http://www.clarkware.com/software/junitperf-1.9.1.zip
Url:		http://www.clarkware.com/software/JUnitPerf.html
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	junit >= 0:3.2
BuildRequires:	java-rpmbuild >= 0:1.6
Requires:	jpackage-utils
Requires:	junit >= 0:3.2

%description
JUnitPerf is a collection of JUnit test decorators used to measure the
performance and scalability of functionality contained within existing
JUnit tests.

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Java
Summary:	Demos for %{name}
Requires:	%{name} = %{EVRD}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
CLASSPATH=$(build-classpath junit) %{ant} -Dbuild.sysclasspath=first jar test javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 0644 dist/%{name}-%{version}.jar \
    %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
cp -pr samples %{buildroot}%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc LICENSE README docs/JUnitPerf.html
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}/*

%files demo
%{_datadir}/%{name}

