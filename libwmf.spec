#
# Conditional build:
%bcond_without	gtk		# without gtk-loader package (which requires gtk+2-devel)
%bcond_without	static_libs	# don't build static version of library
#
Summary:	libwmf - library to convert WMF files
Summary(pl.UTF-8):	libwmf - biblioteka z funkcjami do konwersji plików WMF
Name:		libwmf
Version:	0.2.8.4
Release:	23
Epoch:		2
License:	LGPL v2+
Group:		Applications/Text
Source0:	http://downloads.sourceforge.net/wvware/%{name}-%{version}.tar.gz
# Source0-md5:	d1177739bf1ceb07f57421f0cee191e0
Patch0:		%{name}-fontmap-pld.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-segv.patch
Patch3:		%{name}-png12.patch
Patch4:		%{name}-0.2.8.4-useafterfree.patch
Patch5:		%{name}-0.2.8.4-CVE-2007-0455.patch
Patch6:		%{name}-0.2.8.4-CVE-2007-3472.patch
Patch7:		%{name}-0.2.8.4-CVE-2007-3473.patch
Patch8:		%{name}-0.2.8.4-CVE-2007-3477.patch
Patch9:		%{name}-0.2.8.4-CVE-2007-2756.patch
Patch10:	%{name}-0.2.8.4-CAN-2004-0941.patch
Patch11:	%{name}-0.2.8.4-CVE-2009-3546.patch
Patch12:	%{name}-pixbufloaderdir.patch
URL:		http://wvware.sourceforge.net/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.0
%{?with_gtk:BuildRequires:	gtk+2-devel >= 1:2.10.0}
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
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
%{__rm} configure.in
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
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

%{__rm} -rf html-doc
mv -f $RPM_BUILD_ROOT%{_datadir}/doc ./html-doc

# no static modules and *.la for GTK+ loaders - shut up check-files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.{a,la}

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
%doc html-doc examples
%attr(755,root,root) %{_bindir}/libwmf-config
%attr(755,root,root) %{_libdir}/libwmf.so
%attr(755,root,root) %{_libdir}/libwmflite.so
%{_libdir}/libwmf.la
%{_libdir}/libwmflite.la
%{_includedir}/libwmf

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwmf.a
%{_libdir}/libwmflite.a
%endif

%if %{with gtk}
%files gtk-loader
%defattr(644,root,root,755)
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.so
%endif
