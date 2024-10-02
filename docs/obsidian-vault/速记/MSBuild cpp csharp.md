# MSBuild cpp csharp

## utf8 问题

MSVC 是通过文件前面的 BOM 来识别 Unicode 编码的，如果没有 BOM 就使用 [[ANSI 字符集|ANSI]]。[^1] 如果使用没有 BOM 的 UTF-8 编码保存代码文件，编译时必须加上 `/utf-8` 参数。

## `*_s()` 函数问题

在项目设置里关闭 SDL checks。[^2]

## Conformance mode

开启后会禁止 MSVC 的扩展语法，严格遵循 C++ 标准。[^3]DX12 龙书里的示例需要关掉 Conformance mode 才能编译。

## Windows app

- [/SUBSYSTEM (Specify Subsystem) | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/subsystem-specify-subsystem?view=msvc-170)

## 重用 C++ 项目配置

- [Share or reuse Visual Studio project settings - C++ | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/create-reusable-property-configurations?view=msvc-170)

## 编译后复制文件

- [Copying Visual Studio project file(s) to output directory during build - Stack Overflow](https://stackoverflow.com/questions/10827024/copying-visual-studio-project-files-to-output-directory-during-build)
- WinSDK 路径：[Visual Studio 2019 Windows SDK executable path macro has multiple paths - Stack Overflow](https://stackoverflow.com/questions/68350812/visual-studio-2019-windows-sdk-executable-path-macro-has-multiple-paths)
- post-build-event 在 project up-to-date 时不会执行，就算 dependency 变了也不执行。可以把命令放到 custom build event 里，然后指定 additional inputs 和 outputs，如果 msbuild 发现文件变了就会自动执行。如果希望它始终执行，可以不指定输入，然后给一个永远不会出现的 `$(TargetDir)dummy_output` 作为输出。

## CLR 寄宿

- [Write a custom .NET runtime host - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting)
- [samples/core/hosting at main · dotnet/samples (github.com)](https://github.com/dotnet/samples/tree/main/core/hosting)
- [Deep-dive into .NET Core primitives: deps.json, runtimeconfig.json, and dll's (natemcmaster.com)](https://natemcmaster.com/blog/2017/12/21/netcore-primitives/)
- [sdk/documentation/specs/runtime-configuration-file.md at main · dotnet/sdk (github.com)](https://github.com/dotnet/sdk/blob/main/documentation/specs/runtime-configuration-file.md)
- [runtime/docs/design/features/native-hosting.md at main · dotnet/runtime (github.com)](https://github.com/dotnet/runtime/blob/main/docs/design/features/native-hosting.md)
- `<EnableDynamicLoading>true</EnableDynamicLoading>` 出处 [dotnet publish does not generate runtimeconfig.json · Issue #10506 · dotnet/sdk (github.com)](https://github.com/dotnet/sdk/issues/10506)
- [Interoperating with unmanaged code - .NET Framework | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/framework/interop/)
- [c++ - Get path of executable - Stack Overflow](https://stackoverflow.com/questions/1528298/get-path-of-executable)

### mixed debugger

- [Debug in Mixed Mode (managed and native code) - Visual Studio (Windows) | Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/debugger/how-to-debug-in-mixed-mode?view=vs-2022)

### 修改 dotnet 构建目录

- [windows - Completely change obj folder location in c# project - Stack Overflow](https://stackoverflow.com/questions/63536867/completely-change-obj-folder-location-in-c-sharp-project)
- [Common MSBuild Project Properties - MSBuild | Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/msbuild/common-msbuild-project-properties?view=vs-2022)
- [.NET project SDK overview | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview)
- [Artifacts output layout - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/sdk/artifacts-output)

### interop

- [Native interoperability best practices - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/best-practices)

### internal call

CLR 默认不支持 mono 那种 internal call。

- [c++ - Can I export functions of a static library when building a dynamic library linking against that static library? - Stack Overflow](https://stackoverflow.com/questions/47791319/can-i-export-functions-of-a-static-library-when-building-a-dynamic-library-linki)
- [c++ - How do you identify exported functions in a Windows static library? - Stack Overflow](https://stackoverflow.com/questions/50978611/how-do-you-identify-exported-functions-in-a-windows-static-library)
- `NativeLibrary.GetEntryPointModuleHandle`：[Support for Mono's DllImport(@"__Internal") ? · Issue #7267 · dotnet/runtime (github.com)](https://github.com/dotnet/runtime/issues/7267)

链接静态库时，需要加上 `/WHOLEARCHIVE` 参数。

另一种方案：[swig/swig: SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages. (github.com)](https://github.com/swig/swig)

### hostfxr 意义

fxr stands for hostfxr.dll is responsible for determining the correct version of the .NET Core runtime and framework libraries needed based on the application's configuration and the available runtime installations on the host system. [^4]

[^1]: [/utf-8 (Set source and execution character sets to UTF-8) | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/utf-8-set-source-and-executable-character-sets-to-utf-8?view=msvc-170)
[^2]: [/sdl (Enable Additional Security Checks) | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/sdl-enable-additional-security-checks?view=msvc-170)
[^3]: [/permissive- (Standards conformance) | Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance?view=msvc-170)
[^4]: [.net - what is meaning (full form) of fxr in hostfxr.dll? - Stack Overflow](https://stackoverflow.com/questions/78178615/what-is-meaning-full-form-of-fxr-in-hostfxr-dll)
