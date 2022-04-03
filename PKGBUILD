# Maintainer: Bruno Fauth <bvfauth@hotmail.com>

_name=yt_upload
_git_name=youtube-upload
pkgname="python-$_name-git"
pkgver='0.0.0a1'
pkgrel=3
pkgdesc="Upload videos to youtube, from the command line"

arch=('any')
url="https://github.com/brunofauth/$_git_name"
license=('MIT')

depends=('python' 'python-google-api-python-client' 'python-oauth2client' 'python-tqdm' 'python-click')
makedepends=('python-setuptools')

source=("git+https://github.com/brunofauth/$_git_name.git")
md5sums=('SKIP')


build() {
    cd "$_git_name"
    python setup.py build
}


package() {
    cd "$_git_name"
    python setup.py install --skip-build --root="$pkgdir" --optimize=1
    install -Dm644 "shared_files/fish_completion.fish" "$pkgdir/usr/share/fish/completions/$_name.fish"
}

