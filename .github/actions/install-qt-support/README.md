# Install Qt dependencies

This action uses `apt-get` to install the OS packages needed to import Qt on
Linux. It does nothing on non-Linux runners.

It installs `libegl1`, a link-time dependency of `libQt6Gui`, and
`libopengl0`, needed by EDM's PySide6 build though not by the PyPI wheel. The
packages that the xcb platform plugin needs are not installed: workflows use
`QT_QPA_PLATFORM=offscreen` in place of a display.

## Inputs

There are no inputs.

## Outputs

There are no outputs.

## Example usage

```yml
jobs:

  test-with-edm:
    strategy:
      matrix:
        os: ['ubuntu-latest', 'macos-latest', 'windows-latest']

    runs-on: ${{ matrix.os }}
    steps:
    - uses: actions/checkout@v7
    - uses: ./.github/actions/install-qt-support
```
