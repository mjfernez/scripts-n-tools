# Simple user report script
param (
        [switch]$report
        )

Import-Module ActiveDirectory

$today=(get-date -Format "yyyy-MM-dd")
$users = Get-ADUser -filter * | Sort-Object name

if($report) {
        $fn = "users-$today.csv"
        $users | export-csv .\$fn
        [Console]::Error.WriteLine("Saved result list to $fn")
} else {
        [Console]::Error.WriteLine("Writing device list to stdout")
        write-output $users
}
