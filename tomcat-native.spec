%define		orgname		tomcat-native

%{?use_default_jdk:%use_default_jdk 8}

Summary:	Native Tomcat Connector based on APR
Summary(pl.UTF-8):	Natywny konektor Tomcata oparty na APR
Name:		tomcat9-native
Version:	1.3.10
Release:	1
License:	Apache v2
Group:		Libraries
Source0:	https://archive.apache.org/dist/tomcat/tomcat-connectors/native/%{version}/source/%{orgname}-%{version}-src.tar.gz
# Source0-md5:	9e8230375b8fbb093f81ba7126ef31c8
URL:		https://tomcat.apache.org/native-1.3-doc/
BuildRequires:	ant
BuildRequires:	apr-devel >= 1.6.3
BuildRequires:	autoconf
BuildRequires:	automake
%buildrequires_jdk
BuildRequires:	jpackage-utils
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 3.0.0
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Obsoletes:	tomcat-native9 < 1.3.9-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tomcat can use the Apache Portable Runtime to provide superior
scalability, performance, and better integration with native server
technologies. The Apache Portable Runtime is a highly portable library
that is at the heart of Apache HTTP Server 2.x. APR has many uses,
including access to advanced IO functionality (such as sendfile, epoll
and OpenSSL), OS level functionality (random number generation, system
status, etc), and native process handling (shared memory, NT pipes and
Unix sockets).

These features allows making Tomcat a general purpose webserver, will
enable much better integration with other native web technologies, and
overall make Java much more viable as a full fledged webserver
platform rather than simply a backend focused technology.

This is the 1.3.x branch, which serves Tomcat 9. Tomcat 10.1 and newer
dropped the APR connector and need the 2.0.x branch, packaged as
tomcat-native.

%description -l pl.UTF-8
Tomcat może wykorzystać Apache Portable Runtime, aby zapewnić najwyższą
skalowalność, wydajność i lepszą integrację z natywnymi technologiami
serwerowymi.

Apache Portable Runtime jest wysoce przenośną biblioteką, która jest
sercem serwera Apache HTTPD 2.x. APR ma wiele zastosowań, m.in. dostęp
do zaawansowanych funkcji we/wy (takich jak sendfile, epoll i OpenSSL),
funkcji poziomu systemu operacyjnego (generowanie liczb losowych, stan
systemu itp.) oraz natywną obsługę procesów (pamięć współdzielona,
potoki NT i gniazda uniksowe).

Te cechy pozwalają na wykorzystanie Tomcata jako serwera WWW do
zastosowań ogólnych, pozwalają na o wiele lepszą integrację z innymi
natywnymi technologiami WWW i ogólnie pozwalają traktować Javę jako
zaawansowaną i kompletną platformę WWW, a nie tylko technologię
backendową.

To jest gałąź 1.3.x, przeznaczona dla Tomcata 9. Tomcat 10.1 i nowsze
nie mają już konektora APR i wymagają gałęzi 2.0.x, dostarczanej jako
tomcat-native.

%package devel
Summary:	Header files for tcnative library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tcnative
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	tomcat-native9-devel < 1.3.9-2

%description devel
Header files for tcnative library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tcnative.

%package static
Summary:	Static tcnative library
Summary(pl.UTF-8):	Statyczna biblioteka tcnative
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	tomcat-native9-static < 1.3.9-2

%description static
Static tcnative library.

%description static -l pl.UTF-8
Statyczna biblioteka tcnative.

%prep
%setup -q -n %{orgname}-%{version}-src

%build
# build java part
%ant clean jar

# build native part
cd native
./buildconf --with-apr=%{_datadir}/apr
%configure \
	--with-java-home=%{java_home} \
	--with-apr=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{orgname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

cd native
%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# Why Makefile doesn't do that?
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -p include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt README.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%attr(755,root,root) %{_libdir}/libtcnative-1.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtcnative-1.so.0
%{_libdir}/libtcnative-1.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtcnative-1.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libtcnative-1.a
