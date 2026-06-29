$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$JdkDir = Join-Path $Root ".tools\jdk-21"

if (Test-Path "$JdkDir\bin\java.exe") {
    & "$JdkDir\bin\java.exe" -version
    Write-Host "JDK 21 already installed at $JdkDir"
    exit 0
}

New-Item -ItemType Directory -Force -Path (Join-Path $Root ".tools") | Out-Null
$zip = Join-Path $Root ".tools\jdk21.zip"
$url = "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.11%2B10/OpenJDK21U-jdk_x64_windows_hotspot_21.0.11_10.zip"

Write-Host "Downloading JDK 21..."
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
Write-Host "Extracting..."
Expand-Archive -Path $zip -DestinationPath (Join-Path $Root ".tools") -Force
$extracted = Get-ChildItem (Join-Path $Root ".tools") -Directory | Where-Object { $_.Name -like "jdk-21*" } | Select-Object -First 1
if ($extracted -and $extracted.Name -ne "jdk-21") {
    Rename-Item $extracted.FullName "jdk-21"
}
Remove-Item $zip -Force -ErrorAction SilentlyContinue

# Import Maven Central cert for builds behind SSL inspection
$hostname = "repo.maven.apache.org"
$tcp = New-Object System.Net.Sockets.TcpClient($hostname, 443)
$ssl = New-Object System.Net.Security.SslStream($tcp.GetStream(), $false, ({ $true }))
$ssl.AuthenticateAsClient($hostname)
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($ssl.RemoteCertificate)
$certPath = Join-Path $Root ".tools\maven-central.cer"
[System.IO.File]::WriteAllBytes($certPath, $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert))
& "$JdkDir\bin\keytool.exe" -importcert -trustcacerts -alias maven-central -file $certPath -keystore "$JdkDir\lib\security\cacerts" -storepass changeit -noprompt | Out-Null
$ssl.Close(); $tcp.Close()

& "$JdkDir\bin\java.exe" -version
Write-Host "JDK 21 ready at $JdkDir"
