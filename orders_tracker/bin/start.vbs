Dim i
Dim strComputer
Dim FindProc
 
strComputer = "."

FindProc = "orders-tracker.exe"

Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set colProcessList = objWMIService.ExecQuery _
    ("Select Name from Win32_Process WHERE Name LIKE '" & FindProc & "%'")
Set WshShell = CreateObject("WScript.Shell") 

If colProcessList.count>0 then
    MsgBox "Already running!", 64, "orders-tracker"
    WshShell.Run "http://localhost:5000"
else
    WshShell.Run chr(34) & "orders-tracker.exe" & Chr(34), 0
End if

Set WshShell = Nothing
Set objWMIService = Nothing
Set colProcessList = Nothing
