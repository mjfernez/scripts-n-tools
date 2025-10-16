Import-Module ActiveDirectory

$csv = Get-Content $args[0]

ForEach ($user in $csv) {
    Enable-ADAccount -Identity $user

    Write-Host $user"'s account has been re-enabled"
}
