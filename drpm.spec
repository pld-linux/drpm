# TODO: more rpm5 porting or use rpm.org
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# tests
#
Summary:	Library for making, reading and applying deltarpm packages
Summary(pl.UTF-8):	Biblioteka do tworzenia, odczytu i aplikowania pakietów deltarpm
Name:		drpm
Version:	0.3.0
Release:	0.1
# drpm_{diff,search}.c are BSD; the rest LGPL v3+
License:	LGPL v3+ with BSD parts
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/drpm/releases
Source0:	https://github.com/rpm-software-management/drpm/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	e1ca38e14f52d0f5229bba45ba8b8904
Patch0:		%{name}-cmake.patch
# not enough, drpm uses too many rpm4.6+ APIs
Patch1:		%{name}-rpm5.patch
URL:		https://github.com/rpm-software-management/drpm
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 2.8
BuildRequires:	doxygen
#BuildRequires:	lzlib-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if %{with tests}
BuildRequires:	cmocka-devel
BuildRequires:	deltarpm
BuildRequires:	valgrind
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for making, reading and applying deltarpm packages.

%description -l pl.UTF-8
Biblioteka do tworzenia, odczytu i aplikowania pakietów deltarpm.

%package devel
Summary:	Header files for drpm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki drpm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for drpm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki drpm.

%package apidocs
Summary:	API documentation for drpm library
Summary(pl.UTF-8):	Dokumentacja API biblioteki drpm
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for drpm library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki drpm.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
CFLAGS="%{rpmcflags} %{rpmcppflags} -I/usr/include/rpm"
%cmake .. \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_INSTALL_DIR=%{_lib}

%{__make}

%if %{with tests}
ctest
%endif

%if %{with apidocs}
%{__make} -C doc doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.BSD
%attr(755,root,root) %{_libdir}/libdrpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdrpm.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdrpm.so
%{_includedir}/drpm.h
%{_pkgconfigdir}/drpm.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
