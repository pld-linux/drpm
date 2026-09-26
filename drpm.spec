#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# tests
%bcond_without	valgrind	# valgrind tests
#
# valgrind archs without x32 (x32 valgrind is actually x86_64)
%ifnarch %{ix86} %{x8664} %{armv7} ppc ppc64 s390x aarch64
%undefine	with_valgrind
%endif
Summary:	Library for making, reading and applying deltarpm packages
Summary(pl.UTF-8):	Biblioteka do tworzenia, odczytu i aplikowania pakietów deltarpm
Name:		drpm
Version:	0.5.3
Release:	1
# drpm_{diff,search}.c are BSD; the rest LGPL v3+
License:	LGPL v3+ with BSD parts
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/drpm/releases
Source0:	https://github.com/rpm-software-management/drpm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5b917b66ed242fc517f077ab9db7aa9a
Patch0:		%{name}-cmake.patch
URL:		https://github.com/rpm-software-management/drpm
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.5
%{?with_apidocs:BuildRequires:	doxygen}
# no option to enable
#BuildRequires:	lzlib-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
# which exactly? not specified, but rpm5 is not supported
BuildRequires:	rpm-devel >= 1:4.16
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
%if %{with tests}
BuildRequires:	cmocka-devel
BuildRequires:	deltarpm
%if %{with valgrind}
BuildRequires:	glibc-debuginfo
BuildRequires:	valgrind
%endif
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
BuildArch:	noarch

%description apidocs
API documentation for drpm library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki drpm.

%prep
%setup -q
%patch -P 0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{!?with_tests:-DENABLE_TESTS=OFF}

%{__make}

%if %{with tests}
ctest \
	%{!?with_valgrind:-E drpm_memcheck}
%endif

%if %{with apidocs}
%{__make} -C doc doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.BSD
%{_libdir}/libdrpm.so.*.*.*
%ghost %{_libdir}/libdrpm.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdrpm.so
%{_includedir}/drpm.h
%{_pkgconfigdir}/drpm.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
