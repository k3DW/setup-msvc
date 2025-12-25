# setup-msvc

A composite GitHub Action to download, install, and setup the environment for a particular version of MSVC on Windows.

## Usage example

This example uses Visual Studio 17.13.3, as described in [this article](https://blog.ganets.ky/MsvcGha).

```yml
- name: Setup MSVC
  uses: k3DW/setup-msvc@main
  with:
    vs-version: 14.43.17.13
    bootstrapper-url: https://download.visualstudio.microsoft.com/download/pr/9b2a4ec4-2233-4550-bb74-4e7facba2e03/00f873e49619fc73dedb5f577e52c1419d058b9bf2d0d3f6a09d4c05058c3f79/vs_BuildTools.exe
```

* `vs-version` is a required input, denoting part of the name of the "individual component" in the Visual Studio installation, `"Microsoft.VisualStudio.Component.VC.<vs-version>.x86.x64"`.
* `bootstrapper-url` is a required input, denoting the download location of the bootstrapper to install Visual Studio. See the [Release History page](https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history) for all the URLs.
* `install-path` is an optional input, denoting the path at which Visual Studio is installed. It defaults to `..\vs-install`.

## Future development

### Simplification

In the future, this action may be changed to simply map the input "17.13.3" onto both the `vs-version` "14.43.17.13" and the `bootstrapper-url` given above. That way, the user does not need to search for this information, and can simply input "17.13.3", for example. This would also work with all other version numbers.

### Caching

At the moment, this action does not work with [`actions/cache@v4`](https://github.com/actions/cache). There is currently no known working caching solution for this action.
