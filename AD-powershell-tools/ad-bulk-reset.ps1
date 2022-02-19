# Usage: ad-bulk-reset.ps1 <user-list-file>
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
	 
	# Force user to reset password at next logon.
	# Remove this line if not needed for you
	#Set-AdUser -Identity $user -ChangePasswordAtLogon $true
	Write-Host $user"'s password has been reset"
}
