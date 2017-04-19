%global udevdir %(pkg-config --variable=udevdir udev)

# global gitdate 20150917
# global gitversion e514da82

Name:           libratbag
Version:        0.6
Release:        5%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
Summary:        Programmable input device library
License:        MIT
URL:            https://github.com/libratbag/libratbag
%if 0%{?gitdate}
Source0:        %{name}-%{gitdate}.tar.xz
Source1:        make-git-snapshot.sh
Source2:        commitid
%else
Source0:        https://github.com/libratbag/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  git
BuildRequires:  meson pkgconfig
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  pkgconfig(udev)
BuildRequires:  doxygen graphviz
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


# hack until rhbz#1409661 gets fixed
%{!?__global_cxxflags: %define __global_cxxflags %{optflags}}

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
git add .
git commit --allow-empty -a -q -m "%{version} baseline."

# Apply all the patches.
git am -p1 %{patches} < /dev/null

%build
%meson -Dudev-dir=%{udevdir}
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
* Tue Apr 04 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.6-5
- disable the tests

* Tue Apr 04 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.6-4
- Add check too

* Tue Apr 04 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.6-3
- Add graphviz too

* Tue Apr 04 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.6-2
- Force doxygen as a requirement

* Wed Mar 22 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.6-1
- libratbag v0.6

* Fri Sep 16 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.5-1
- libratbag v0.5

* Mon Mar 14 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.4-1
- libratbag v0.4

* Sat Mar 12 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.3-5
- Bump the specfile for the autobuilder tests

* Sat Mar 12 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.3-4
- Bump the specfile for the autobuilder tests

* Sat Mar 12 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.3-3
- Bump the specfile for the autobuilder tests

* Sat Mar 12 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.3-2
- Bump the specfile for the autobuilder tests

* Tue Mar 08 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 0.3-1
- Initial Fedora packaging
