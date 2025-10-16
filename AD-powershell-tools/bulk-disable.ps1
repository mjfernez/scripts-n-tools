# Import users from CSV and disable them

Import-Module ActiveDirectory

$csv = Get-Content $args[0]

ForEach ($user in $csv) {
    Disable-ADAccount -Identity $user
    Write-Host $user"'s account has been fully disabled"
}
