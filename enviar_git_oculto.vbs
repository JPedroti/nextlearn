' Roda o enviar_git.bat sem abrir janela (usado pela tarefa agendada).
Set fso = CreateObject("Scripting.FileSystemObject")
pasta = fso.GetParentFolderName(WScript.ScriptFullName)
CreateObject("WScript.Shell").Run "cmd /c """"" & pasta & "\enviar_git.bat"" silencioso""", 0, False
