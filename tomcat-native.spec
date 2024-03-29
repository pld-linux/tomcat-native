Summary:	Native Tomcat Connector based on APR
Summary(pl.UTF-8):	Natywny Connector Tomcata oparty o APR
Name:		tomcat-native
Version:	1.2.31
Release:	1
License:	Apache v2
Group:		Libraries
Source0:	http://www.apache.org/dist/tomcat/tomcat-connectors/native/%{version}/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	a6943e123b1eca0795e106af132df93d
URL:		http://tomcat.apache.org/native-doc/
BuildRequires:	ant
BuildRequires:	apr-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	jdk >= 1.7.0
BuildRequires:	jpackage-utils
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildConflicts:	java-gcj-compat
Requires:	nss
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

%description -l pl.UTF-8
Tomcat może wykorzytać Apache Portable Runtime aby zapewnić najwyższą,
skalowalność, wydajność i lepszą integrację z natywnymi technologiami
serwerowymi.

Apache portable Runtime jest wysoce przenośną biblioteką, która jest
sercem serwera Apache HTTPD 2.x. APR ma wiele zestosowań, m. in.
dostępd do zaawansowanych funkcjonalnośći IO (takich jak sendfile,
epoll i OpenSSL), funkcjonalności posiomu systemu operacyjnego
(generacja liczb losowych, stan systemu, itp.) i natywną obsługę
procesów (współdzielona pamięć, potoki NT i gniazda uniksowe).

Te cechy pozwalają na wykorzystanie Tomcata jako sewera www do
zastosowań ogólnych, pozwalają na o wiele lepszą integrację z innymi
natywnymi technologiami www i w ogólności pozwalają na traktowanie
Javy jako zaawansowanej i kompletnej platformy www a nie tylko
technologii backendowej.

%package devel
Summary:	Header files for tcnative library
Summary(pl.UTF-8):	Pliki nagłówwkowe biblioteki tcnative
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for tcnative library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tcnative.

%package static
Summary:	Static tcnative library
Summary(pl.UTF-8):	Statyczna biblioteka tcnative
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static tcnative library.

%description static -l pl.UTF-8
Statyczna biblioteka tcnative.

%prep
%setup -q -n %{name}-%{version}-src

%build
# build java part
%ant clean jar \
	-Dcompile.source=1.7 \
	-Dcompile.target=1.7 \
	%{nil}

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
cp -p dist/tomcat-native-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/tomcat-native-%{version}.jar
ln -s tomcat-native-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/tomcat-native.jar

cd native
%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# Why Makefile doesn't do that?
install -d $RPM_BUILD_ROOT/%{_includedir}
cp -p include/*.h $RPM_BUILD_ROOT/%{_includedir}

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
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtcnative-1.a
