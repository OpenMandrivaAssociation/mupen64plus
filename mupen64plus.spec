
Name:           mupen64plus
Version:        1.99.5
Release:        %mkrel 1.2
Summary:        Plugin-Based Nintendo 64 Emulator
Group:          Emulators
License:        GPLv2+
Url:            http://code.google.com/p/mupen64plus/
AutoReqProv:    on
BuildRequires:  gcc-c++ libSDL-devel libpng-devel libsamplerate-devel
BuildRequires:  freetype2-devel zlib-devel lirc-devel
Source:         %{name}-bundle-src-%{version}.tar.gz
Source100:      %{name}-rpmlintrc
Patch0:		mupen64plus-zlib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

%package -n libmupen64plus2
Summary:        Shared Library Interface to the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
Requires:       fonts-ttf-dejavu
AutoReqProv:    on

%description -n libmupen64plus2
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games. It includes four MIPS R4300 CPU emulators, with dynamic
recompilers for 32-bit x86 and 64-bit amd64 systems.  It supports plugins for
audio, graphical rendering (RDP), the signal co-processor (RSP), and input.

This package contains the shared library interface for frontends.

%package -n libmupen64plus-devel
Summary:        Include Files for Mupen64plus Development
License:        GPLv2+
Group:          Development/C
Requires:       libmupen64plus2 = %{version}
AutoReqProv:    on

%description -n libmupen64plus-devel
This package contains all necessary include files to develop frontends against
the Mupen64plus shared library interface.

%package ui-console
Summary:        Command Line Frontend for the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
AutoReqProv:    on
Requires:       libmupen64plus2
Requires:       mupen64plus-plugin-audio
Requires:       mupen64plus-plugin-video
Requires:       mupen64plus-plugin-input
Requires:       mupen64plus-plugin-rsp-hle

%description ui-console
Mupen64Plus is a plugin-based N64 emulator which is capable of accurately
playing many games.

This package contains a command line frontend.

%package plugin-audio-sdl
Summary:        SDL Audio Plugin for the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
Provides:       mupen64plus-plugin-audio
AutoReqProv:    on

%description plugin-audio-sdl
This package contains the SDL audio plugin for the Mupen64plus Nintendo 64
Emulator.

%package plugin-input-sdl
Summary:        SDL Input Plugin for the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
Provides:       mupen64plus-plugin-input
AutoReqProv:    on

%description plugin-input-sdl
This package contains the SDL input plugin for the Mupen64plus Nintendo 64
Emulator. It has LIRC Infrared remote control interface and Rumble Pak support.

%package plugin-rsp-hle
Summary:        RSP High-Level Emulation Plugin For the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
AutoReqProv:    on

%description plugin-rsp-hle
This package contains the RSP High-Level emulation plugin for the Mupen64plus
Nintendo 64 Emulator.


%package plugin-video-rice
Summary:        Rice Video Plugin for the Mupen64plus Nintendo 64 Emulator
License:        GPLv2+
Group:          Emulators
Provides:       mupen64plus-plugin-video
AutoReqProv:    on

%description plugin-video-rice
This package contains the Rice Video Plugin for the Mupen64plus Nintendo 64
Emulator. It provides Hi-resolution texture support.

%prep
%setup -q -n %{name}-bundle-src-%{version}
%patch0 -p1


%build
export CFLAGS="%{optflags}"
make %{?_smp_mflags} -C source/mupen64plus-core/projects/unix all SHAREDIR=%{_datadir}/mupen64plus2/ LIRC=1 NO_ASM=1 V=1
make %{?_smp_mflags} -C source/mupen64plus-ui-console/projects/unix all COREDIR=%{_libdir}/ SHAREDIR=%{_datadir}/mupen64plus2/ PLUGINDIR=%{_libdir}/mupen64plus2/ NO_ASM=1 V=1
make %{?_smp_mflags} -C source/mupen64plus-audio-sdl/projects/unix all NO_ASM=1 V=1
make %{?_smp_mflags} -C source/mupen64plus-input-sdl/projects/unix all NO_ASM=1 V=1
make %{?_smp_mflags} -C source/mupen64plus-rsp-hle/projects/unix all NO_ASM=1 V=1
make %{?_smp_mflags} -C source/mupen64plus-video-rice/projects/unix all NO_ASM=1 V=1

%install
make -C source/mupen64plus-core/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/ INCDIR=%{_includedir}/mupen64plus/ LIRC=1 NO_ASM=1
pushd %{buildroot}%{_libdir}
ln -sf libmupen64plus.so.2.0.0 libmupen64plus.so.2
ln -sf libmupen64plus.so.2.0.0 libmupen64plus.so
popd
make -C source/mupen64plus-ui-console/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" BINDIR=/usr/bin/ MANDIR=%{_mandir}/man6/ NO_ASM=1
rm %{buildroot}%{_datadir}/mupen64plus2/font.ttf
make -C source/mupen64plus-audio-sdl/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" LIBDIR=%{_libdir}/mupen64plus2/ NO_ASM=1
make -C source/mupen64plus-input-sdl/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/mupen64plus2/ NO_ASM=1
make -C source/mupen64plus-rsp-hle/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" LIBDIR=%{_libdir}/mupen64plus2/ NO_ASM=1
make -C source/mupen64plus-video-rice/projects/unix install PREFIX="%{_prefix}" DESTDIR="%{buildroot}" SHAREDIR=%{_datadir}/mupen64plus2/ LIBDIR=%{_libdir}/mupen64plus2/ NO_ASM=1
chmod -R 0755 %{buildroot}%{_libdir}

%post -n libmupen64plus2 -p /sbin/ldconfig

%postun -n libmupen64plus2 -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n libmupen64plus2
%defattr(-,root,root,-)
%dir %{_datadir}/mupen64plus2
%dir %{_libdir}/mupen64plus2
%{_libdir}/libmupen64plus.so.*
%{_datadir}/mupen64plus2/mupen64plus.cht
%{_datadir}/mupen64plus2/mupencheat.txt
%{_datadir}/mupen64plus2/mupen64plus.ini

%files -n libmupen64plus-devel
%defattr(-,root,root,-)
%doc source/mupen64plus-core/INSTALL
%doc source/mupen64plus-core/LICENSES
%doc source/mupen64plus-core/README
%doc source/mupen64plus-core/RELEASE
%dir %{_includedir}/mupen64plus
%{_includedir}/mupen64plus/*
%{_libdir}/libmupen64plus.so

%files ui-console
%defattr(-,root,root,-)
%doc source/mupen64plus-ui-console/INSTALL
%doc source/mupen64plus-ui-console/LICENSES
%doc source/mupen64plus-ui-console/README
%doc source/mupen64plus-ui-console/RELEASE
%doc %{_mandir}/man6/man6/mupen64plus.*
%{_bindir}/mupen64plus

%files plugin-audio-sdl
%defattr(-,root,root,-)
%doc source/mupen64plus-audio-sdl/INSTALL
%doc source/mupen64plus-audio-sdl/LICENSES
%doc source/mupen64plus-audio-sdl/RELEASE
%{_libdir}/mupen64plus2/%{name}/mupen64plus-audio-sdl.so

%files plugin-input-sdl
%defattr(-,root,root,-)
%doc source/mupen64plus-input-sdl/AUTHORS
%doc source/mupen64plus-input-sdl/COPYING
%doc source/mupen64plus-input-sdl/INSTALL
%doc source/mupen64plus-input-sdl/LICENSES
%doc source/mupen64plus-input-sdl/README
%doc source/mupen64plus-input-sdl/RELEASE
%{_datadir}/mupen64plus2/InputAutoCfg.ini
%{_libdir}/mupen64plus2/%{name}/mupen64plus-input-sdl.so

%files plugin-rsp-hle
%defattr(-,root,root,-)
%doc source/mupen64plus-rsp-hle/INSTALL
%doc source/mupen64plus-rsp-hle/LICENSES
%doc source/mupen64plus-rsp-hle/RELEASE
%{_libdir}/mupen64plus2/%{name}/mupen64plus-rsp-hle.so

%files plugin-video-rice
%defattr(-,root,root,-)
%doc source/mupen64plus-video-rice/INSTALL
%doc source/mupen64plus-video-rice/LICENSES
%doc source/mupen64plus-video-rice/README
%doc source/mupen64plus-video-rice/RELEASE
%{_datadir}/mupen64plus2/RiceVideoLinux.ini
%{_libdir}/mupen64plus2/%{name}/mupen64plus-video-rice.so
