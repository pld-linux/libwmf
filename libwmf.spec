#
# Conditional build:
# _without_gtk	- without gtk-loader package (which requires gtk+2-devel)
#
Summary:	libwmf - library to convert wmf files
Summary(pl):	libwmf - biblioteka z funkcjami do konwersji plików wmf
Name:		libwmf
Version:	0.2.8
Release:	1
Epoch:		2
License:	GPL
Group:		Applications/Text
Source0:	http://dl.sourceforge.net/wvware/%{name}-%{version}.tar.gz
# Source0-md5:	269fb225cd44f40cc877fb6c63706112
Patch0:		%{name}-fontmap-pld.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-segv.patch
URL:		http://wvware.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.0
%{!?_without_gtk:BuildRequires:	gtk+2-devel >= 2.1.2}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool >= 1:1.4.2-9
PreReq:		ghostscript-fonts-std
Requires(post):	/sbin/ldconfig
Requires(post):	sed
Requires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libwmf is a library for unix like machines that can convert wmf files
into other formats, currently it supports fig, eps, a gd binding to
convert to png, and an X one to draw direct to an X window or pixmap.

%description -l pl
libwmf jest bibliotek± dla systemów uniksowych, która konwertuje pliki
wmf na inne formaty. Aktualnie obs³uguje formaty fig i eps, format png
poprzez bibliotekê gd oraz - poprzez biblioteki X Window - rysowanie w
okienku oraz format xpm.

%package devel
Summary:	libwmf - header files
Summary(pl):	libwmf - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains libwmf header files.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe do biblioteki libwmf.

%package static
Summary:	libwmf - static libraries
Summary(pl):	libwmf - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This package contains libwmf static libraries.

%description static -l pl
Pakiet zawiera statyczn± wersjê biblioteki libwmf.

%package gtk-loader
Summary:	WMF loader for gdk_pixbuf 2.x library
Summary(pl):	Modu³ wczytuj±cy WMF dla biblioteki gdk_pixbuf 2.x
Group:		X11/Libraries
Requires:	%{name} = %{version}

%description gtk-loader
WMF loader for gdk_pixbuf 2.x library.

%description gtk-loader -l pl
Modu³ wczytuj±cy WMF dla biblioteki gdk_pixbuf 2.x

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc ./html-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/libwmf-fontmap >/dev/null

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/libwmf-fontmap
%attr(755,root,root) %{_bindir}/wmf2eps
%attr(755,root,root) %{_bindir}/wmf2fig
%attr(755,root,root) %{_bindir}/wmf2gd
%attr(755,root,root) %{_bindir}/wmf2svg
%attr(755,root,root) %{_bindir}/wmf2x
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_datadir}/libwmf
%dir %{_datadir}/libwmf/fonts
%ghost %{_datadir}/libwmf/fonts/fontmap

%files devel
%defattr(644,root,root,755)
%doc html-doc examples
%attr(755,root,root) %{_bindir}/libwmf-config
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%if %{?_without_gtk:0}%{!?_without_gtk:1}
%files gtk-loader
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gtk-2*/*/loaders/*.so
%{_libdir}/gtk-2*/*/loaders/*.la
%endif
