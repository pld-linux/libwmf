Summary:	libwmf - library to convert wmf files
Summary:	libwmf - biblioteka z funkcjami do konwersji plików wmf
Name:		libwmf
Version:	0.1.21
Release:	1
Epoch:		2
License:	GPL
Group:		Applications/Text
Group(de):	Applikationen/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Aplikacje/Tekst
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Source0:	http://download.sourceforge.net/wvware/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-shared.patch
URL:		http://wvware.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libtool
BuildRequires:	libpng-devel
BuildRequires:	freetype-devel
BuildRequires:	zlib-devel
BuildRequires:	XFree86-devel
#BuildRequires:	xpm-devel		# if XFree86-devel < 4.0.1-7

%description
libwmf is a library for unix like machines that can convert wmf files
into other formats, currently it supports a gd binding to convert to
png, and an X one to draw direct to an X window or pixmap.

%package devel
Summary:	libwmf - header files
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
This package contains libwmf header files.

%package static
Summary:	libwmf - static libraries
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
This package contains libwmf static libraries.


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS} -I/usr/include/freetype"
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/xgd}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_includedir}/{gd.h,gd_io.h,gdf*,gdc*} $RPM_BUILD_ROOT%{_includedir}/xgd

rm -rf notes/testprogram
gzip -9nf winepatches/* notes/*.txt CHANGELOG CREDITS README

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches *.gz
# only these binaries - other conflicts with gd
%attr(755,root,root) %{_bindir}/bdftogd
%attr(755,root,root) %{_bindir}/wmftofig
%attr(755,root,root) %{_bindir}/wmftopng
%attr(755,root,root) %{_bindir}/xwmf
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
