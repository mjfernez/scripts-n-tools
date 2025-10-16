# Adapted from: https://itpro-tips.com/test-ad-authentication-with-powershell/
# The interesting bit about this one is that it doesn't seem to get logged by AD,
# so you won't end up with false positives from testing creds

function Test-ADAuthentication {
        Param(
                [Parameter(Mandatory)]
                [string]$User,
                [Parameter(Mandatory)]
                $Password,
                [Parameter(Mandatory = $false)]
                $Server,
                [Parameter(Mandatory = $false)]
                [string]$Domain = $env:USERDOMAIN
        )

        Add-Type -AssemblyName System.DirectoryServices.AccountManagement

        $contextType = [System.DirectoryServices.AccountManagement.ContextType]::Domain

        $argumentList = New-Object -TypeName "System.Collections.ArrayList"
        $null = $argumentList.Add($contextType)
        $null = $argumentList.Add($Domain)

        if($null -ne $Server){
                $argumentList.Add($Server)
        }

        $principalContext = New-Object System.DirectoryServices.AccountManagement.PrincipalContext -ArgumentList $argumentList -ErrorAction SilentlyContinue

        if ($null -eq $principalContext) {
                Write-Warning "$Domain\$User - AD Authentication failed"
        }

        if ($principalContext.ValidateCredentials($User, $Password)) {
                Write-Output "$Domain\$User - AD Authentication OK"
        }
        else {
                Write-Warning "$Domain\$User - AD Authentication failed"
        }
}

$csv = Import-Csv $args[0]
ForEach ($userpass in $csv) {
        Test-ADAuthentication -User $userpass.user -Password $userpass.password
}

