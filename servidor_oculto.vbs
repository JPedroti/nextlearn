' Liga o site local (runserver) sem abrir janela. Usado pela tarefa "NextLearn servidor".
Set fso = CreateObject("Scripting.FileSystemObject")
pasta = fso.GetParentFolderName(WScript.ScriptFullName)
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = pasta
sh.Run "cmd /c venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 > servidor.log 2>&1", 0, False
