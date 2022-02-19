# PLEASE READ SCRIPT BEFORE RUNNING

# Based largely on https://activedirectorypro.com/find-remove-old-computer-accounts-active-directory/
# but changed his brack/object syntax to a string query

# Usage
# \inactive-ad-device-report.ps1 "OU=Workstations,DC=example,DC=com" "dd/MM/yyyy" [-report] [-disable]

# Report and disable are optional switches to print the results to a CSV 
# and disable the computer accounts, respectively

# A cutoff date and a search base, must be provided.

# All computers with Login times before
# the cutoff date are included in the results of the report

# The search base is an LDAP filter that must (at a minimum) specify
# your domain controller. And probably an OU you want to search, like:
#
# "OU=Workstations,DC=example,DC=com"

# See here for an example: https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-adcomputer?view=windowsserver2022-ps#example-4--get-computer-accounts-in-a-specific-location-using-an-ldapfilter
param (
    [Parameter(Mandatory)][string]$searchbase,
    [Parameter(Mandatory)][string]$cutoff,
    [switch]$report,
    [switch]$disable
)
Import-Module ActiveDirectory
$today=(get-date -Format "yyyy-MM-dd")
try {
    $filter = "(LastLogonDate -lt `"$cutoff`") -and (Enabled -eq `"$true`")"
    $devices = Get-ADcomputer -filter $filter -properties LastLogonDate,Enabled,DistinguishedName `
    -SearchBase $searchbase `
    | select name, LastLogonDate, DistinguishedName
    | sort LastLogonDate
}
catch {
    write-error "Bad input. Usage: '.\inactive-ad-device-report.ps1 `"ldap-filter`" `"dd/MM/yyyy`" [-report] [-disable]'"
}

if ($disable) {
    ForEach ($device in $devices) {
        Set-ADComputer -Identity $device.Name -Enabled $false -Verbose -WhatIf
    }
    
    [Console]::Error.WriteLine("All devices disabled")
}

if($report) {
    $fn = "old-computers-$today.csv"
    $devices | export-csv .\$fn
    [Console]::Error.WriteLine("Saved result list to $fn")
} else {
    [Console]::Error.WriteLine("Writing device list to stdout")
    write-output $devices
}
