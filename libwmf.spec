Summary:	libwmf - library to convert wmf files
Summary:	libwmf - biblioteka z funkcjami do konwersji plików wmf
Name:		libwmf
Version:	0.1.17
Release:	2
Epoch:		2
License:	GPL
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Group:		Applications/Text
Group(de):	Applikationen/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Aplikacje/Tekst
Source0:	http://www.csn.ul.ie/~caolan/publink/libwmf/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.csn.ul.ie/~caolan/docs/libwmf.html
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel
BuildRequires:	libpng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libwmf is a library for unix like machines that can convert wmf files
into other formats, currently it supports a gd binding to convert to
gif, and an X one to draw direct to an X window or pixmap.

%prep
%setup -q -n %{name}
%patch -p1

%build
CFLAGS="%{?debug:-O -g}%{!?debug:$RPM_OPT_FLAGS} -I/usr/include/freetype"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf winepatches/* CHANGELOG CREDITS README libwmf.lsm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches/*.gz *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_includedir}/*
