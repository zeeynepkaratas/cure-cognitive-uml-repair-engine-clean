# Run locally in Windows PowerShell. The key is never echoed or written to source.
$ErrorActionPreference = 'Stop'
Write-Host 'Configure the OpenAI API key for this Windows user.'
Write-Host 'Create a project API key at https://platform.openai.com/api-keys if needed.'
Write-Host 'Paste the key at the hidden prompt. Do not paste it into chat.'
$secureApiKey = Read-Host 'OpenAI API key (hidden)' -AsSecureString
$apiKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureApiKey)
try {
    $localApiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($apiKeyPointer).Trim()
    if ([string]::IsNullOrWhiteSpace($localApiKey)) { throw 'No key entered; nothing was changed.' }
    [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $localApiKey, 'User')
    Write-Host 'Key saved for this Windows user. Its value has not been displayed.'
    Write-Host 'Return to the chat and say that the key is configured.'
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($apiKeyPointer)
    Remove-Variable localApiKey -ErrorAction SilentlyContinue
    $secureApiKey.Dispose()
}
Read-Host 'Press Enter to close'
