# Install Qt dependencies

This action uses `apt-get` to install the OS packages needed to import Qt on
Linux. It does nothing on non-Linux runners.

It installs two packages, and only two: `libegl1`, a link-time dependency of
`libQt6Gui`, and `libopengl0`, which EDM's PySide6 build needs though the PyPI
wheel doesn't. Together they're what makes PySide6 importable. The packages
that the xcb platform plugin needs are deliberately not installed, because
workflows use `QT_QPA_PLATFORM=offscreen` in place of a display.

Without these, the failure is silent rather than loud — Pyface falls back to
its null toolkit, so GUI tests skip and autodoc documents placeholder classes,
with everything still reporting success.

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
