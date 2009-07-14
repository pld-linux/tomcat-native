Summary:	Native Tomcat Connector based on APR
Summary(pl.UTF-8):	Natywny Connector Tomcata oparty o APR
Name:		tomcat-native
Version:	1.1.16
Release:	0.1
License:	Apache
Group:		Libraries
Source0:	http://www.apache.org/dist/tomcat/tomcat-connectors/native/%{version}/source/%{name}-%{version}-src.tar.gz
URL:		http://tomcat.apache.org/native-doc
BuildRequires:	apr-util-devel
BuildRequires:	jdk
BuildRequires:	openssl-devel
Requires:	apr
Requires:	openssl
Suggests:	jre
Suggests:	tomcat
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

Tomcat może wykorzytać Apache Portable Runtime aby zapewnić
najwyższą, saklowalność, wydajność i lepszą integrację z
natywnymi technologiami serwerowymi.

Apache portable Runtime jest wysoce przenośną biblioteką, która
jest sercem serwera Apache HTTPD 2.x. APR ma wiele zestosowań, m. in.
dostępd do zaawansowanych funkcjonalnośći IO (takich jak sendfile,
epoll i OpenSSL), funkcjonalności posiomu systemu operacyjnego
(generacja liczb losowych, stan systemu, itp.) i natywną obsługę
procesów (współdzielona pamięć, potoki NT i gniazda uniksowe).

Te cechy pozwalają na wykorzystanie Tomcata jako sewera www do
zastosowań ogólnych, pozwalają na o wiele lepszą integrację z
innymi natywnymi technologiami www i w ogólności pozwalają na
traktowanie Javy jako zaawansowanej i kompletnej platformy www s nie
tylko technologii backendowej.

%package devel
Summary:	Header files for tcnative library
Summary(pl.UTF-8):	Pliki nagłówwkowe biblioteki tcnative
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for tcnative library

%description devel -l pl.UTF-8
Pliki nag¿ówkowe biblioteki tcnative

%prep
%setup -q -n %{name}-%{version}-src/jni/native

%build
%configure \
	--with-apr=%{_bindir} \
	--with-java-home=%{java_home}\

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/tcnative.exp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc CHANGES LICENSE NOTICE
%attr(755,root,root) %{_libdir}/libtcnative-1.so*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtcnative-1.*a
%{_pkgconfigdir}/tcnative-1.pc
