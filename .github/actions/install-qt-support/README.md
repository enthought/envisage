# Install Qt dependencies

This action uses `apt-get` to install necessary packages for Qt support on
Linux. It does nothing on non-Linux runners.

## Inputs

There are no inputs.

## Outputs

There are no outputs.

## Example usage

```yml
jobs:

  # Test against EDM packages
  test-with-edm:
    strategy:
      matrix:
        os: ['ubuntu-latest', 'macos-latest', 'windows-latest']

    runs-on: ${{ matrix.os }}
    steps:
    - uses: actions/checkout@v3
    - uses: ./.github/actions/install-qt-support
```
