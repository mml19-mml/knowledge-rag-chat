param(
    [string]$SdkPath = '',
    [string]$JdkPath = ''
)
$ErrorActionPreference = 'Stop'

if (-not $SdkPath) {
    $SdkPath = $env:ANDROID_HOME
    if (-not $SdkPath) { $SdkPath = Join-Path $env:LOCALAPPDATA 'Android\Sdk' }
}
if (-not (Test-Path -LiteralPath (Join-Path $SdkPath 'platforms\android-36\android.jar'))) {
    throw '请先安装 Android SDK Platform 36，或用 -SdkPath 指定已有 SDK。'
}
if (-not $JdkPath) {
    $JdkPath = $env:JAVA_HOME
    if (-not $JdkPath) { $JdkPath = Join-Path $env:ProgramFiles 'Android\Android Studio\jbr' }
}
if (-not (Test-Path -LiteralPath (Join-Path $JdkPath 'bin\java.exe'))) {
    throw '未找到 Java。请用 -JdkPath 指向 Android Studio 的 jbr 或 JDK 17 及更新版本。'
}

# Use a short runtime-only directory for Java's Windows local socket paths.
$buildTemp = Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'KnowledgeChatBuild\tmp'
New-Item -ItemType Directory -Path $buildTemp -Force | Out-Null
$previousJavaHome = $env:JAVA_HOME
$previousAndroidHome = $env:ANDROID_HOME
$previousJavaOptions = $env:JAVA_TOOL_OPTIONS
try {
    $env:JAVA_HOME = $JdkPath
    $env:ANDROID_HOME = $SdkPath
    $env:JAVA_TOOL_OPTIONS = '-Djava.io.tmpdir="' + $buildTemp + '" -Djdk.net.unixdomain.tmpdir="' + $buildTemp + '"'
    $properties = 'sdk.dir=' + $SdkPath.Replace('\','/').Replace(':','\:')
    [IO.File]::WriteAllText((Join-Path $PSScriptRoot 'local.properties'), $properties, [Text.UTF8Encoding]::new($false))
    Push-Location -LiteralPath $PSScriptRoot
    try {
        & (Join-Path $PSScriptRoot 'gradlew.bat') --no-daemon assembleDebug
        if ($LASTEXITCODE -ne 0) { throw '构建失败，请查看上面的报错。' }
        Write-Host ('APK 已生成：' + (Join-Path $PSScriptRoot 'app\build\outputs\apk\debug\app-debug.apk'))
    } finally { Pop-Location }
} finally {
    $env:JAVA_HOME = $previousJavaHome
    $env:ANDROID_HOME = $previousAndroidHome
    $env:JAVA_TOOL_OPTIONS = $previousJavaOptions
}
