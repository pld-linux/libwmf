Summary:	libwmf, library to convert wmf files.
Name:		libwmf
Version:	0.1.11
Release:	1
Serial:		2
Copyright:	GPL
Group:		Utilities/Text
Vendor:		Caolan McNamara <Caolan.McNamara@ul.ie>
Source:		http://www.csn.ul.ie/~caolan/publink/libwmf/%{name}-%{version}.tar.gz
URL:		http://www.csn.ul.ie/~caolan/docs/libwmf.html
Requires:	freetype
BuildRoot:	/tmp/%{name}-%{version}-root

%description
libwmf is a library for unix like machines that can convert wmf files into
other formats, currently it supports a gd binding to convert to gif, and an
X one to draw direct to an X window or pixmap.

%prep
%setup -q -n %{name}
LDFLAGS="-s"; export LDFLAGS
%configure

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc examples notes winepatches CHANGELOG CREDITS README TODO libwmf.lsm
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*
