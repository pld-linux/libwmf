# TODO:
# - update fonts-Type1-urw.spec, revise system fonts usage
# - given sysfontmap file doesn't exist since 2007
#
# Conditional build:
%bcond_without	gtk		# gtk-loader package (requires gdk-pixbuf2)
%bcond_without	static_libs	# static library
#
Summary:	libwmf - library to convert WMF files
Summary(pl.UTF-8):	libwmf - biblioteka z funkcjami do konwersji plików WMF
Name:		libwmf
Version:	0.2.13
Release:	1
Epoch:		2
License:	LGPL v2+
Group:		Applications/Text
# original project seems dead
#Source0:	http://downloads.sourceforge.net/wvware/%{name}-%{version}.tar.gz
# RedHat supported fork
#Source0Download: https://github.com/caolanm/libwmf/releases
Source0:	https://github.com/caolanm/libwmf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1c95363fd3c2f7b92bb4f4026aeab8d6
Patch0:		%{name}-fontmap-pld.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-segv.patch
Patch3:		%{name}-png12.patch
Patch4:		%{name}-ah.patch
URL:		http://wvware.sourceforge.net/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.0
%{?with_gtk:BuildRequires:	gdk-pixbuf2-devel >= 2.1.2}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.4.0
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
Requires(post):	ghostscript-fonts-std
Requires(post):	sed
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	fonts-Type1-urw
Requires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer

%description
libwmf is a library for Unix like machines that can convert WMF files
into other formats, currently it supports fig, eps, a gd binding to
convert to png, and an X one to draw direct to an X Window or pixmap.

%description -l pl.UTF-8
libwmf jest biblioteką dla systemów uniksowych, która konwertuje pliki
WMF na inne formaty. Aktualnie obsługuje formaty fig i eps, format png
poprzez bibliotekę gd oraz - poprzez biblioteki X Window - rysowanie w
okienku oraz format xpm.

%package libs
Summary:	libwmf - libraries
Summary(pl.UTF-8):	libwmf - biblioteki
Group:		Libraries
Conflicts:	libwmf < 2:0.2.8.4

%description libs
This package contains libwmf libraries.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki libwmf.

%package devel
Summary:	libwmf - header files
Summary(pl.UTF-8):	libwmf - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
# libwmflite(.la) has no additional deps
# libwmf(.la) needs freetype-devel, expat-devel, libjpeg-devel, libpng-devel, xorg-lib-libX11-devel

%description devel
This package contains libwmf header files.

%description devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe do biblioteki libwmf.

%package static
Summary:	libwmf - static libraries
Summary(pl.UTF-8):	libwmf - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains libwmf static libraries.

%description static -l pl.UTF-8
Pakiet zawiera statyczną wersję biblioteki libwmf.

%package gtk-loader
Summary:	WMF loader for gdk_pixbuf 2.x library
Summary(pl.UTF-8):	Moduł wczytujący WMF dla biblioteki gdk_pixbuf 2.x
Group:		X11/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gtk-loader
WMF loader for gdk_pixbuf 2.x library.

%description gtk-loader -l pl.UTF-8
Moduł wczytujący WMF dla biblioteki gdk_pixbuf 2.x

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-sysfontmap=%{_fontsdir}/ghostscript-fonts-std.font \
	--with-gsfontmap=%{_fontsdir}/Type1/Fontmap \
	--with-gsfontdir=%{_fontsdir}/Type1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# no static modules and *.la for GTK+ loaders - shut up check-files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/libwmf-fontmap > /dev/null

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/libwmf-fontmap
%attr(755,root,root) %{_bindir}/wmf2eps
%attr(755,root,root) %{_bindir}/wmf2fig
%attr(755,root,root) %{_bindir}/wmf2gd
%attr(755,root,root) %{_bindir}/wmf2svg
%attr(755,root,root) %{_bindir}/wmf2x
%dir %{_datadir}/libwmf
%dir %{_datadir}/libwmf/fonts
%ghost %{_datadir}/libwmf/fonts/fontmap

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwmf-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwmf-0.2.so.7
%attr(755,root,root) %{_libdir}/libwmflite-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwmflite-0.2.so.7

%files devel
%defattr(644,root,root,755)
%doc doc/caolan doc/html/{*.html,*.css,*.gif,*.png} examples
%attr(755,root,root) %{_bindir}/libwmf-config
%attr(755,root,root) %{_libdir}/libwmf.so
%attr(755,root,root) %{_libdir}/libwmflite.so
%{_libdir}/libwmf.la
%{_libdir}/libwmflite.la
%{_includedir}/libwmf
%{_pkgconfigdir}/libwmf.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwmf.a
%{_libdir}/libwmflite.a
%endif

%if %{with gtk}
%files gtk-loader
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gdk-pixbuf-2.0/2.*/loaders/io-wmf.so
%endif
