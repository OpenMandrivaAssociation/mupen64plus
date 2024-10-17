%define major 2
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Plugin-Based Nintendo 64 Emulator
Name:		mupen64plus
Version:	2.0
Release:	2
License:	GPLv2+
Group:		Emulators
Url:		https://code.google.com/p/mupen64plus/
Source0:	%{name}-bundle-src-%{version}.tar.gz
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)
Requires:	%{libname} = %{EVRD}
Requires:	fonts-ttf-dejavu
Suggests:	%{name}-ui-console
Suggests:	%{name}-ui-m64py

%description
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

This package contains only common files for Mupen64Plus. You need to install
a frontend application to run games. For example, mupen64plus-ui-console or
mupen64plus-ui-m64py.

%files
%dir %{_datadir}/mupen64plus2
%dir %{_libdir}/mupen64plus2
%{_datadir}/mupen64plus2/mupen64plus.cht
%{_datadir}/mupen64plus2/mupencheat.txt
%{_datadir}/mupen64plus2/mupen64plus.ini
%{_datadir}/mupen64plus2/font.ttf

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared Library Interface to Mupen64plus
Group:		System/Libraries

%description -n %{libname}
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

This package contains the shared library interface for frontends.

%files -n %{libname}
%{_libdir}/libmupen64plus.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Include Files for Mupen64plus Development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains all necessary include files to develop frontends against
the Mupen64plus shared library interface.

%files -n %{devname}
%doc source/mupen64plus-core/INSTALL
%doc source/mupen64plus-core/LICENSES
%doc source/mupen64plus-core/README
%doc source/mupen64plus-core/RELEASE
%dir %{_includedir}/mupen64plus
%{_includedir}/mupen64plus/*
%{_libdir}/libmupen64plus.so

#----------------------------------------------------------------------------

%package ui-console
Summary:	Command Line Frontend for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Requires:	%{libname} = %{EVRD}
Requires:	mupen64plus-plugin-audio
Requires:	mupen64plus-plugin-video
Requires:	mupen64plus-plugin-input
Requires:	mupen64plus-plugin-rsp-hle

%description ui-console
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games.

This package contains a command line frontend.

%files ui-console
%doc source/mupen64plus-ui-console/INSTALL
%doc source/mupen64plus-ui-console/LICENSES
%doc source/mupen64plus-ui-console/README
%doc source/mupen64plus-ui-console/RELEASE
%doc %{_mandir}/man6/mupen64plus.6*
%{_bindir}/mupen64plus

#----------------------------------------------------------------------------

%package plugin-audio-sdl
Summary:	SDL Audio Plugin for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	mupen64plus-plugin-audio

%description plugin-audio-sdl
This package contains the SDL audio plugin for the Mupen64plus Nintendo 64
Emulator.

%files plugin-audio-sdl
%doc source/mupen64plus-audio-sdl/INSTALL
%doc source/mupen64plus-audio-sdl/LICENSES
%doc source/mupen64plus-audio-sdl/RELEASE
%{_libdir}/mupen64plus2/mupen64plus-audio-sdl.so

#----------------------------------------------------------------------------

%package plugin-input-sdl
Summary:	SDL Input Plugin for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	mupen64plus-plugin-input

%description plugin-input-sdl
This package contains the SDL input plugin for the Mupen64plus Nintendo 64
Emulator. It has LIRC Infrared remote control interface and Rumble Pak support.

%files plugin-input-sdl
%doc source/mupen64plus-input-sdl/AUTHORS
%doc source/mupen64plus-input-sdl/COPYING
%doc source/mupen64plus-input-sdl/INSTALL
%doc source/mupen64plus-input-sdl/LICENSES
%doc source/mupen64plus-input-sdl/README
%doc source/mupen64plus-input-sdl/RELEASE
%{_datadir}/mupen64plus2/InputAutoCfg.ini
%{_libdir}/mupen64plus2/mupen64plus-input-sdl.so

#----------------------------------------------------------------------------

%package plugin-rsp-hle
Summary:	RSP High-Level Emulation Plugin For the Mupen64plus
Group:		Emulators
Provides:	mupen64plus-plugin-rsp-hle

%description plugin-rsp-hle
This package contains the RSP High-Level emulation plugin for the Mupen64plus
Nintendo 64 Emulator.

%files plugin-rsp-hle
%doc source/mupen64plus-rsp-hle/INSTALL
%doc source/mupen64plus-rsp-hle/LICENSES
%doc source/mupen64plus-rsp-hle/RELEASE
%{_libdir}/mupen64plus2/mupen64plus-rsp-hle.so

#----------------------------------------------------------------------------

%package plugin-video-rice
Summary:	Rice Video Plugin for the Mupen64plus Nintendo 64 Emulator
Group:		Emulators
Provides:	mupen64plus-plugin-video

%description plugin-video-rice
This package contains the Rice Video Plugin for the Mupen64plus Nintendo 64
Emulator. It provides Hi-resolution texture support.

%files plugin-video-rice
%doc source/mupen64plus-video-rice/INSTALL
%doc source/mupen64plus-video-rice/LICENSES
%doc source/mupen64plus-video-rice/README
%doc source/mupen64plus-video-rice/RELEASE
%{_datadir}/mupen64plus2/RiceVideoLinux.ini
%{_libdir}/mupen64plus2/mupen64plus-video-rice.so

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-bundle-src-%{version}

%build
%make -C source/mupen64plus-core/projects/unix all \
	OPTFLAGS="%{optflags}" \
	SHAREDIR=%{_datadir}/mupen64plus2/ \
	LIRC=1 \
	V=1

%make -C source/mupen64plus-ui-console/projects/unix all \
	OPTFLAGS="%{optflags}" \
	COREDIR=%{_libdir}/ \
	SHAREDIR=%{_datadir}/mupen64plus2/ \
	PLUGINDIR=%{_libdir}/mupen64plus2/ \
	V=1

%make -C source/mupen64plus-audio-sdl/projects/unix all \
	OPTFLAGS="%{optflags}" \
	V=1

%make -C source/mupen64plus-input-sdl/projects/unix all \
	OPTFLAGS="%{optflags}" \
	V=1

%make -C source/mupen64plus-rsp-hle/projects/unix all \
	OPTFLAGS="%{optflags}" \
	V=1

%make -C source/mupen64plus-video-rice/projects/unix all \
	OPTFLAGS="%{optflags}" \
	V=1

%install
%makeinstall_std -C source/mupen64plus-core/projects/unix \
	PREFIX="%{_prefix}" \
	SHAREDIR=%{_datadir}/mupen64plus2/ \
	LIBDIR=%{_libdir}/ \
	INCDIR=%{_includedir}/mupen64plus/ \
	LIRC=1 \
	INSTALL_STRIP_FLAG=

pushd %{buildroot}%{_libdir}
ln -sf libmupen64plus.so.%{major} libmupen64plus.so
popd

%makeinstall_std -C source/mupen64plus-ui-console/projects/unix \
	PREFIX="%{_prefix}" \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir}/ \
	NO_ASM=1 \
	INSTALL_STRIP_FLAG=

%makeinstall_std -C source/mupen64plus-audio-sdl/projects/unix \
	PREFIX="%{_prefix}" \
	LIBDIR=%{_libdir}/mupen64plus2/ \
	INSTALL_STRIP_FLAG=

%makeinstall_std -C source/mupen64plus-input-sdl/projects/unix \
	PREFIX="%{_prefix}" \
	SHAREDIR=%{_datadir}/mupen64plus2/ \
	LIBDIR=%{_libdir}/mupen64plus2/ \
	INSTALL_STRIP_FLAG=

%makeinstall_std -C source/mupen64plus-rsp-hle/projects/unix \
	PREFIX="%{_prefix}" \
	LIBDIR=%{_libdir}/mupen64plus2/ \
	INSTALL_STRIP_FLAG=

%makeinstall_std -C source/mupen64plus-video-rice/projects/unix \
	PREFIX="%{_prefix}" \
	SHAREDIR=%{_datadir}/mupen64plus2/ \
	LIBDIR=%{_libdir}/mupen64plus2/ \
	INSTALL_STRIP_FLAG=

chmod -R 0755 %{buildroot}%{_libdir}

mv %{buildroot}%{_libdir}/mupen64plus2/%{name}/mupen64plus*.so %{buildroot}%{_libdir}/mupen64plus2/
rmdir %{buildroot}%{_libdir}/mupen64plus2/%{name}

