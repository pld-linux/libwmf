Summary:	libwmf - library to convert wmf files
Summary(pl):	libwmf - biblioteka z funkcjami do konwersji plików wmf
Name:		libwmf
Version:	0.1.21b
Release:	5
Epoch:		2
License:	GPL
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Group:		Applications/Text
Group(de):	Applikationen/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Aplikacje/Tekst
Source0:	ftp://download.sourceforge.net/pub/sourceforge/wvware/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-shared.patch
URL:		http://wvware.sourceforge.net/
BuildRequires:	libtool
BuildRequires:	libpng-devel
BuildRequires:	freetype1-devel
BuildRequires:	XFree86-devel
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
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%configure \
	--enable-shared \
	--with-ttf=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/xgd}

# avoid relinking
for f in *.la ; do
	sed -e '/^relink_command/d' $f > $f.new
	mv -f $f.new $f
done

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_includedir}/{gd.h,gd_io.h,gdf*,gdc*} \
	$RPM_BUILD_ROOT%{_includedir}/xgd

# remove unwanted paths from libtool scripts
for f in $RPM_BUILD_ROOT%{_libdir}/lib{X,eps,gd,xf,}wmf.la ; do
	cat $f | awk '/^dependency_libs/ { gsub("-L[ \t]*[^ \t]*/\.libs ","") } //' >$f.tmp
	mv -f $f.tmp $f
done

rm -rf notes/testprogram
gzip -9nf winepatches/* notes/*.txt CHANGELOG CREDITS README

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
# only these binaries - other conflicts with gd
%attr(755,root,root) %{_bindir}/bdftogd
%attr(755,root,root) %{_bindir}/wmftofig
%attr(755,root,root) %{_bindir}/wmftopng
%attr(755,root,root) %{_bindir}/wmftoeps
%attr(755,root,root) %{_bindir}/xwmf
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc examples notes winepatches
%{_includedir}/*
%{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
