Import-Module ActiveDirectory

function Gen-Random-Password {
    $str = ""
    for ($i = 0; $i -lt 24 ; $i++) {
        $rand = Get-Random -Minimum 32 -Maximum 127
        $str += [char]$rand
    }
    $newpwd = ConvertTo-SecureString -String [String]$str -AsPlainText -Force
    return $newpwd
}

# Import users from CSV
$csv = Get-Content $args[0]

ForEach ($user in $csv) {
    $newPassword = Gen-Random-Password

    # Reset user password.
    Set-ADAccountPassword -Identity $user -NewPassword $newPassword -Reset

    Write-Host $user"'s password has been reset"
    Write-Host $newPassword
}
