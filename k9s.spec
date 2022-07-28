%define		vendor_version	0.26.0
Summary:	Kubernetes CLI To Manage Your Clusters In Style
Name:		k9s
Version:	0.26.0
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/derailed/k9s/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f80f0d730ab0b515d3e7cd9020a6a8d6
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	9dad04d72c0d74d44c904675c1b544ee
URL:		https://k9scli.io/
BuildRequires:	golang >= 1.14
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
K9s provides a terminal UI to interact with your Kubernetes clusters.
The aim of this project is to make it easier to navigate, observe and
manage your applications in the wild. K9s continually watches
Kubernetes for changes and offers subsequent commands to interact with
your observed resources.

%package -n bash-completion-k9s
Summary:	Bash completion for k9s command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-k9s
Bash completion for k9s command line.

%package -n fish-completion-k9s
Summary:	fish-completion for k9s
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-k9s
fish-completion for k9s.

%package -n zsh-completion-k9s
Summary:	ZSH completion for k9s command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-k9s
ZSH completion for k9s command line.

%prep
%setup -q -a1

%{__mv} %{name}-%{vendor_version}/vendor .

%build
ldflags=" -X github.com/derailed/k9s/cmd.version=%{version}
	-X github.com/derailed/k9s/cmd.commit=
	-X github.com/derailed/k9s/cmd.date=$(date +'%Y-%m-%dT%H:%M:%SZ')"
%__go build -v -mod=vendor -ldflags="$ldflags" -tags netgo -o target/k9s main.go

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{bash_compdir},%{fish_compdir},%{zsh_compdir}}
install -p target/k9s $RPM_BUILD_ROOT%{_bindir}

./target/k9s completion bash > $RPM_BUILD_ROOT%{bash_compdir}/k9s
./target/k9s completion fish > $RPM_BUILD_ROOT%{fish_compdir}/k9s.fish
./target/k9s completion zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_k9s

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/k9s

%files -n bash-completion-k9s
%defattr(644,root,root,755)
%{bash_compdir}/k9s

%files -n fish-completion-k9s
%defattr(644,root,root,755)
%{fish_compdir}/k9s.fish

%files -n zsh-completion-k9s
%defattr(644,root,root,755)
%{zsh_compdir}/_k9s
