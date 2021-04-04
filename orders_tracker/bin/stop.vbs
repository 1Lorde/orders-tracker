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
    WshShell.run "cmd.exe /C taskkill /IM" & FindProc, 0
    MsgBox "Successfully stopped!", 64, "orders-tracker"
End if

Set WshShell = Nothing
Set objWMIService = Nothing
Set colProcessList = Nothing
