Summary:	Screen recorder for Linux
Summary(pl.UTF-8):	Nagrywarka ekranu dla Linuksa
Name:		simplescreenrecorder
Version:	0.3.6
Release:	2
License:	GPL v3
Group:		Applications
Source0:	https://github.com/MaartenBaert/ssr/archive/%{version}/ssr-%{version}.tar.gz
# Source0-md5:	3c0dcf288c0cc1b21f4cd2010c73d5ae
URL:		http://www.maartenbaert.be/simplescreenrecorder/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	Qt5Core-devel >= 5.1.0
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libtool
BuildRequires:	pulseaudio-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
Requires:	Qt5Gui-platform-xcb
Suggests:	%{name}-glinject = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SimpleScreenRecorder is a screen recorder for Linux. Despite the name,
this program is actually quite complex. It's 'simple' in the sense
that it's easier to use than ffmpeg/avconv or VLC :).

%package glinject
Summary:	SimpleScreenRecorder - wrapper library for recording OpenGL
Group:		Applications

%description glinject
A wrapper library and a script to inject screen recording calls into
OpenGL applications, for use with the SimpleScreenRecorder.

%prep
%setup -q -n ssr-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	CXXFLAGS="%{rpmcxxflags} -fPIC" \
	--with-qt5 \
	--with-pulseaudio \
	--with-jack

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libssr-glinject.la

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md *.txt
%attr(755,root,root) %{_bindir}/simplescreenrecorder
%dir %{_datadir}/simplescreenrecorder
%{_datadir}/simplescreenrecorder/output-profiles
%dir %{_datadir}/simplescreenrecorder/translations
%{_mandir}/man1/simplescreenrecorder.1*
%{_mandir}/man1/ssr-glinject.1*
%{_iconsdir}/*/*/apps/simplescreenrecorder*.png
%{_iconsdir}/hicolor/scalable/apps/simplescreenrecorder*.svg
%{_desktopdir}/simplescreenrecorder.desktop

%files glinject
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ssr-glinject
%attr(755,root,root) %{_libdir}/libssr-glinject.so
