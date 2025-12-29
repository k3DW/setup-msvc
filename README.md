# setup-msvc

A composite GitHub Action to download, install, and setup the environment for a particular version of MSVC on Windows.

## Usage example

This example uses Visual Studio 17.13.3, as described in [this article](https://blog.ganets.ky/MsvcGha).

```yml
- name: Setup MSVC
  uses: k3DW/setup-msvc@v1
  with:
    vs-version: "17.13.3"
```

* `vs-version` is a required input, denoting the specific version of Visual Studio to install.
  * The patch version can be omitted, which will install the most recent patch in the minor release series. For example specifying `17.13` will install `17.13.7`.
  * Note, you should quote this input, otherwise you may get unexpected results. `17.13.0` will be sent as `17.13`, which will install `17.13.7`. Instead, `"17.13.0"` will successfully install `17.13.0`.
* `install-path` is an optional input, denoting the path at which Visual Studio is installed.
  * It defaults to `..\vs-install`.

## Future development

### Caching

At the moment, this action does not work with [`actions/cache@v4`](https://github.com/actions/cache). There is currently no known working caching solution for this action.
