Summary:	libwmf - library to convert wmf files
Summary(pl):	libwmf - biblioteka z funkcjami do konwersji plików wmf
Name:		libwmf
Version:	0.2.1
Release:	1
Epoch:		2
License:	GPL
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Group:		Applications/Text
Group(de):	Applikationen/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Aplikacje/Tekst
Source0:	ftp://download.sourceforge.net/pub/sourceforge/wvware/%{name}-%{version}.tar.gz
Patch0:		%{name}-fontmap-pld.patch
Patch1:		%{name}-gd.patch
Patch2:		%{name}-includes.patch
URL:		http://wvware.sourceforge.net/
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	XFree86-devel
BuildRequires:	expat-devel
BuildRequires:	libplot-devel
BuildRequires:	autoconf
BuildRequires:	automake
Prereq:		/sbin/ldconfig
Prereq:		sed
Prereq:		ghostscript-fonts-std
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
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
This package contains libwmf header files.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe do biblioteki libwmf.

%package static
Summary:	libwmf - static libraries
Summary(pl):	libwmf - biblioteki statyczne
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
This package contains libwmf static libraries.

%description static -l pl
Pakiet zawiera statyczn± wersjê biblioteki libwmf.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
libtoolize --copy --force
aclocal
automake -a -c
autoconf
%configure \
	--with-plot
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc ./html-doc
gzip -9nf CREDITS ChangeLog README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/libwmf-fontmap >/dev/null

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/libwmf-fontmap
%attr(755,root,root) %{_bindir}/wmf2eps
%attr(755,root,root) %{_bindir}/wmf2fig
%attr(755,root,root) %{_bindir}/wmf2gd
%attr(755,root,root) %{_bindir}/wmf2magick
%attr(755,root,root) %{_bindir}/wmf2plot
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
%attr(755,root,root) %{_libdir}/*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
