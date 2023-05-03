# Jrunner
Java runner using json configuration file.
It's intended to provide more flexibility when it comes to launch java applications.

## Dependencies
1. Pyinstaller
```Powershell
pip install pyinstaller 
```

## Compilation
```Powershell
pyinstaller --onefile -i jrunner.ico jrunner.py 
```

## Basic usage
```Powershell
jrunner [file] [options...]
```

## Run file template

You can use the following template or create one (-create command)

```Powershell
jrunner -create
```
```json
{
    "javaHome": "",
    "vmArgs": [], //arguments must be separated as strings
    "program": "your_file", 
    "programArgs": [],
    "useJavaw": false,
    "cwd": "",
    "useExe": false,
    "log": false,
    "logDir": ""
}
```
