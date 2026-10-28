%{?use_default_jdk:%use_default_jdk 21}

Summary:	Native Tomcat library providing TLS support via OpenSSL
Summary(pl.UTF-8):	Natywna biblioteka Tomcata obsługująca TLS przez OpenSSL
Name:		tomcat-native
Version:	2.0.16
Release:	1
License:	Apache v2
Group:		Libraries
Source0:	https://archive.apache.org/dist/tomcat/tomcat-connectors/native/%{version}/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	8c17d3332bf1cfaa4139b546451a4216
URL:		https://tomcat.apache.org/native-doc/
BuildRequires:	ant >= 1.10.2
BuildRequires:	apr-devel >= 1.7.0
BuildRequires:	autoconf
BuildRequires:	automake
%buildrequires_jdk
BuildRequires:	jpackage-utils
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 3.0.0
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tomcat Native is a JNI wrapper that allows Tomcat to use OpenSSL
instead of JSSE for TLS support. It uses the Apache Portable Runtime as
an operating system abstraction layer.

The APR based HTTP connector was removed in Tomcat 10.1, so this
version only provides OpenSSL support for the NIO and NIO2 connectors.
It is meant for Tomcat 10.1 and newer; Tomcat 9 needs the 1.3.x branch,
packaged as tomcat9-native.

%description -l pl.UTF-8
Tomcat Native to nakładka JNI pozwalająca Tomcatowi obsługiwać TLS
przez OpenSSL zamiast JSSE. Jako warstwy abstrakcji systemu
operacyjnego używa biblioteki Apache Portable Runtime.

Konektor HTTP oparty na APR został usunięty w Tomcacie 10.1, więc ta
wersja udostępnia obsługę OpenSSL wyłącznie dla konektorów NIO i NIO2.
Jest przeznaczona dla Tomcata 10.1 i nowszych; Tomcat 9 wymaga gałęzi
1.3.x, dostarczanej jako tomcat9-native.

%package devel
Summary:	Header files for tcnative library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tcnative
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
cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
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
%attr(755,root,root) %{_libdir}/libtcnative-2.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtcnative-2.so.0
%{_libdir}/libtcnative-2.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtcnative-2.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libtcnative-2.a
