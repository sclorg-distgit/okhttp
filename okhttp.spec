%{?scl:%scl_package okhttp}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:           %{?scl_prefix}okhttp
Version:        2.7.4
Release:        1.%{baserelease}%{?dist}
Summary:        An HTTP+SPDY client for Java applications

License:        ASL 2.0
URL:            http://square.github.io/%{pkg_name}/
Source0:        https://github.com/square/%{pkg_name}/archive/parent-%{version}.tar.gz#/%{pkg_name}-%{version}.tar.gz
Patch0:         okhttp-2.7.4-airline-0.7.patch
Patch1:         okhttp-2.7.4-rm-android-stuff.patch

BuildArch:      noarch

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix_java_common}mvn(com.google.code.gson:gson)
BuildRequires: %{?scl_prefix}mvn(com.squareup.okio:okio)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires: %{?scl_prefix}mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires: %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)

Obsoletes:     %{name}-protocols < 2

%description
An HTTP+SPDY client for Android and Java applications.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%package parent
Summary:        Parent POM for OkHttp

%description parent
%{summary}.

%package apache
Summary:        OkHttp Apache HttpClient

%description apache
%{summary}.

%package samples
Summary:        OkHttp Samples (Parent)

%description samples
%{summary}.

%package samples-guide
Summary:        OkHttp Sample: Guide

%description samples-guide
%{summary}.

%package samples-simple-client
Summary:        OkHttp Sample: Simple Client

%description samples-simple-client
%{summary}.

%package logging-interceptor
Summary:        OkHttp Logging Interceptor

%description logging-interceptor
%{summary}.

%package ws
Summary:        OkHttp Web Sockets

%description ws
%{summary}.

%package ws-tests
Summary:        OkHttp Web Socket Tests

%description ws-tests
%{summary}.

%package testing-support
Summary:        OkHttp test support classes

%description testing-support
%{summary}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-parent-%{version}

# Plugin prevents build
%pom_remove_plugin org.codehaus.mojo:animal-sniffer-maven-plugin

# templating-maven-plugin is not available in Fedora. Filter sources
# manually before build.
%pom_remove_plugin :templating-maven-plugin okhttp
sed 's|\${project.version}|%{version}|' okhttp/src/main/java-templates/com/squareup/okhttp/internal/Version.java >okhttp/src/main/java/com/squareup/okhttp/internal/Version.java

%pom_disable_module mockwebserver
%pom_disable_module benchmarks
%pom_disable_module static-server samples
%pom_disable_module crawler samples
%pom_disable_module okhttp-tests
%pom_disable_module okhttp-urlconnection
%pom_disable_module okhttp-android-support
%pom_disable_module okcurl

%pom_remove_dep com.google.android:android okhttp

# Unwanted plugin
%pom_remove_plugin :maven-assembly-plugin okcurl
%pom_remove_plugin :maven-checkstyle-plugin
# Unavailable plugin
%pom_remove_plugin org.skife.maven:really-executable-jar-maven-plugin okcurl
# Fix main class
%pom_add_plugin "org.apache.maven.plugins:maven-jar-plugin:2.4" okcurl "
<configuration>
  <archive>
    <manifest>
      <mainClass>com.squareup.okhttp.curl.Main</mainClass>
    </manifest>
  </archive>
</configuration>"

%patch0 -p1
%patch1 -p1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# We don't have all test deps (e.g. npn-boot)
%mvn_build -s --skip-tests -- -P !alpn-when-jdk8
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles-%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc CHANGELOG.md CONTRIBUTING.md README.md
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%files parent -f .mfiles-parent
%doc LICENSE.txt

%files apache -f .mfiles-%{pkg_name}-apache

%files samples -f .mfiles-sample-parent

%files samples-guide -f .mfiles-guide

%files samples-simple-client -f .mfiles-simple-client

%files logging-interceptor -f .mfiles-logging-interceptor

%files testing-support -f .mfiles-okhttp-testing-support

%files ws -f .mfiles-okhttp-ws

%files ws-tests -f .mfiles-okhttp-ws-tests

%changelog
* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 2.7.4-1.2
- Don't build curl module

* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 2.7.4-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Feb 16 2016 Gerard Ryan <galileo@fedoraproject.org> - 2.7.4-1
- Update to version 2.7.4 for RHBZ 1308853

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 16 2015 gil cattaneo <puntogil@libero.it> 2.2.0-5
- enable okcurl module
- introduce license macro

* Thu Jun 18 2015 Mat Booth <mat.booth@redhat.com> - 2.2.0-4
- Add missing BR to fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.0-2
- Add obsoletes for {name}-protocols

* Wed Mar 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.0-1
- Update to upstream version 2.2.0

* Thu Sep 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.0-1
- Update to upstream version 2.0.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-2
- Use Requires: java-headless rebuild (#1067528)

* Sat Nov 23 2013 Gerard Ryan <galileo@fedoraproject.org> - 1.2.1-1
- Initial rpm
