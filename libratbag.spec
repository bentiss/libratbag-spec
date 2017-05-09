%global udevdir %(pkg-config --variable=udevdir udev)

Name:           libratbag
Version:        0.8
Release:        1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
Summary:        Programmable input device library
License:        MIT
URL:            https://github.com/libratbag/libratbag
Source0:        https://github.com/libratbag/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  git
BuildRequires:  meson pkgconfig
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  pkgconfig(udev)
BuildRequires:  check-devel

%description
libratbag is a library that allows to configure programmable
mice.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        -n liblur
Summary:        Logitech Unifying Receiver library

%description    -n liblur
The liblur package contains libraries and tools to access and
configure the Logitech Unifying Receivers. The functionality
are mainly listing, pairing and un-pairing Logitech devices
attached to a receiver.

%package        -n liblur-devel
Summary:        Development files for liblur
Requires:       liblur%{?_isa} = %{version}-%{release}

%description    -n liblur-devel
The liblur-devel package contains libraries and header files for
developing applications that use liblur.

%prep
%autosetup

# hack until rhbz#1409661 gets fixed
%{!?__global_cxxflags: %define __global_cxxflags %{optflags}}

%build
%meson -Dudev-dir=%{udevdir} -Denable-documentation=false
%meson_build

%check
%meson_test

%install
%meson_install


%post
/sbin/ldconfig
udevadm hwdb --update >/dev/null 2>&1 || :

%postun -p /sbin/ldconfig

%post -n liblur -p /sbin/ldconfig

%postun -n liblur -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/libratbag.so.*
%{_bindir}/ratbag-command
%dir %{_datadir}/libratbag
%{_datadir}/libratbag/*.svg
%{udevdir}/rules.d/70-libratbag-mouse.rules
%{udevdir}/hwdb.d/70-libratbag-mouse.hwdb
%{_mandir}/man1/ratbag-command.1*

%files devel
%{_includedir}/libratbag.h
%{_libdir}/libratbag.so
%{_libdir}/pkgconfig/libratbag.pc

%files -n liblur
%license COPYING
%{_libdir}/liblur.so.*
%{_bindir}/lur-command

%files -n liblur-devel
%{_includedir}/liblur.h
%{_libdir}/liblur.so
%{_libdir}/pkgconfig/liblur.pc

%changelog
* Tue May 09 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.8-1
- libratbag v0.8

* Tue May 09 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.7-3
- add a hack for F24 and F25 to compile

* Fri May 05 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.7-2
- Remove the generation of the documentation, we don't ship it

* Thu May 04 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.7-1
- Initial Fedora packaging (rhbz#1309703)
