# create-tasks.ps1 - Kreiraj Task Scheduler taskove

# Autoprofile task (at log on)
Write-Host "Kreiram autoprofile task..." -ForegroundColor Yellow

$autoprofileAction = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$autoprofilePath`""
$autoprofileTrigger = New-ScheduledTaskTrigger -AtLogOn
$autoprofileTrigger.UserId = "$env:USERDOMAIN\$env:USERNAME"
$autoprofileSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$autoprofilePrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

$autoprofileTask = New-ScheduledTask -Action $autoprofileAction -Trigger $autoprofileTrigger -Settings $autoprofileSettings -Principal $autoprofilePrincipal
$autoprofileTask.Author = "UV"

Register-ScheduledTask -TaskName "OpenRGB autoprofile" -InputObject $autoprofileTask -Force | Out-Null
Write-Host "Kreiran task: OpenRGB autoprofile (at log on)" -ForegroundColor Green

# Dnevni taskovi
Write-Host "Kreiram dnevne taskove..." -ForegroundColor Yellow

$items = $config.schedules.items
$startHour = [int]$config.schedules.startHour
$count = $items.Count
$duration = [int][math]::Floor(24 / $count)

for ($i = 0; $i -lt $count; $i++) {
    $item = $items[$i]
    $taskName = $item.taskName
    $prof = $item.profile

    # Izracunaj vreme iz startHour i pozicije
    $hour = [int](($startHour + $duration * $i) % 24)
    $time = "{0:D2}:00" -f $hour

    $action = New-ScheduledTaskAction -Execute $openRGBPath -Argument "-p `"$prof`""
    $trigger = New-ScheduledTaskTrigger -Daily -At $time
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

    $task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal
    $task.Author = "UV"

    Register-ScheduledTask -TaskName $taskName -InputObject $task -Force | Out-Null
    Write-Host "Kreiran task: $taskName u $time -> $prof" -ForegroundColor Green
}
