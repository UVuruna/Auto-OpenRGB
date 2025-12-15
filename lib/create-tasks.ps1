# create-tasks.ps1 - Create Task Scheduler tasks

# Autoprofile task (at log on + resume from sleep)
Write-Host "Creating autoprofile task..." -ForegroundColor Yellow

$autoprofileAction = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$autoprofilePath`""

# Trigger 1: At Log On
$logonTrigger = New-ScheduledTaskTrigger -AtLogOn
$logonTrigger.UserId = "$env:USERDOMAIN\$env:USERNAME"

# Trigger 2: Resume from sleep (Event ID 1 from Power-Troubleshooter)
$CIMTriggerClass = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$sleepTrigger = New-CimInstance -CimClass $CIMTriggerClass -ClientOnly
$sleepTrigger.Subscription = '<QueryList><Query Id="0" Path="System"><Select Path="System">*[System[Provider[@Name=''Microsoft-Windows-Power-Troubleshooter''] and EventID=1]]</Select></Query></QueryList>'
$sleepTrigger.Enabled = $true

$autoprofileSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$autoprofilePrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

$autoprofileTask = New-ScheduledTask -Action $autoprofileAction -Trigger @($logonTrigger, $sleepTrigger) -Settings $autoprofileSettings -Principal $autoprofilePrincipal
$autoprofileTask.Author = "UV"

Register-ScheduledTask -TaskName "OpenRGB autoprofile" -InputObject $autoprofileTask -Force | Out-Null
Write-Host "Created task: OpenRGB autoprofile (at log on + resume from sleep)" -ForegroundColor Green

# Daily tasks
Write-Host "Creating daily tasks..." -ForegroundColor Yellow

$items = $config.schedules.items
$startHour = [int]$config.schedules.startHour
$count = $items.Count
$duration = [int][math]::Floor(24 / $count)

for ($i = 0; $i -lt $count; $i++) {
    $item = $items[$i]
    $taskName = $item.taskName
    $prof = $item.profile

    # Calculate time from startHour and position
    $hour = [int](($startHour + $duration * $i) % 24)
    $time = "{0:D2}:00" -f $hour

    $action = New-ScheduledTaskAction -Execute $openRGBPath -Argument "-p `"$prof`""
    $trigger = New-ScheduledTaskTrigger -Daily -At $time
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

    $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal
    $task.Author = "UV"

    Register-ScheduledTask -TaskName $taskName -InputObject $task -Force | Out-Null
    Write-Host "Created task: $taskName at $time -> $prof" -ForegroundColor Green
}
