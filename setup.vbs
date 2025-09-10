Set objShell = CreateObject("WScript.Shell")
command = WScript.Arguments(0)
objShell.Run command, 0, True ' 0 for hidden window, True to wait for the command to complete
