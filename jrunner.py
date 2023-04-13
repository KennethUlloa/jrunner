import json
from argumentparser import parse_arguments
from sys import argv
import subprocess
import os

properties = {
    "version": "2.1.0",
    "logFile": "log.txt"
}


class RunConfiguration:
    def __init__(self, **kwargs) -> None:
        self.javaHome = self.get_property("javaHome", kwargs, "")
        self.vmArgs = self.get_property("vmArgs", kwargs, ["-jar"])
        self.program = self.get_property("program", kwargs, "")
        self.programArgs = self.get_property("programArgs", kwargs, [])
        self.useJavaw = self.get_property("useJavaw", kwargs, False)
        self.cwd = self.get_property("cwd", kwargs, "")
        self.useExe = self.get_property("useExe", kwargs, False)
    
    def get_command(self, command):
        if type(command) == list:
            return command
        
        if type(command) == str:
            return [command]
    
    def get_property(self, propertyName: str, source: dict, default):
        if propertyName in source: return source[propertyName]
        else: return default
    
    def create_command(self):
        runCommand = []
        #java path configuration
        java = "javaw" if self.useJavaw else "java"
        if self.useExe:
            java += ".exe" 
        javaCommand = java if self.javaHome == "" else f"{self.javaHome}/{java}"
        runCommand += self.get_command(javaCommand)
        #JVM arguments
        runCommand += self.get_command(self.vmArgs)
        #Setting path working directory
        programPath = self.program if self.cwd == "" else self.cwd + "/" + self.program
        runCommand += self.get_command(programPath)
        #Setting program arguments
        runCommand += self.get_command(self.programArgs)
        return runCommand


help = f"""JRUNNER v{properties['version']}

Usage:
    jrunner target_file [options]
if you want to specify a running configuration create a file called "run.json" containing the next keys:
- javaHome: string -> path to the java bin folder (Optional)
- vmArgs: list -> arguments for the JVM (Optional)
- program: string -> program file to be executed (Mandatory)
- programArgs list -> arguments for the java program (Optional)
- useJavaw: boolean -> flag representing whether or not to use javaw instead of java
- cwd: string -> path to append in the program path. 
    @Example: if 'program' has value 'helloworld.java' and 'cwd' has value 'E:/somepath' then 'E:/somepath/helloworld.java' would be executed.
- useExe: boolean -> determines whether or not append .exe to java command (helpful when calling an specific jdk path)
- log: boolean -> flag to enable logging stdout to a file (log.txt not modificable)
- logDir: string -> Path to the directory where log files will be stored (current directory by default)
Line commands:
    -h, it will display this message and then end the execution
    -v, it will display the version ({properties['version']})
    -create, it will create a template for run.json file called run_template.json
    -dir, the output directory to store:
        the created template [when -create is present]
    -log, determine whether or not to redirect the stdout from program to log file
"""

def run(lineargs, useLog = False):
    runFile = os.path.join(os.getcwd(),'run.json')
    arguments = {}
    logFile = properties['logFile']

    if os.path.exists(runFile):
        arguments = json.load(open(runFile,'r',encoding='utf-8'))
        
    config = RunConfiguration(**arguments)

    if len(lineargs['freeArgs']) > 1:
        config.program = lineargs['freeArgs'][1]

    exe_args = config.create_command()

    if 'log' in arguments:
        useLog = useLog or arguments['log']
    
    if 'logDir' in arguments:
        logFile = f"{arguments['logDir']}/{logFile}"

    if useLog:
        with open(logFile,'w', encoding='utf-8') as f:
                f.write("running:"+" ".join(exe_args)+"\n")
                f.write("== PROGRAM STDOUT\n")
                subprocess.Popen(exe_args, stdout=f, stderr=subprocess.STDOUT)
    else:
        print("running:"," ".join(exe_args))
        subprocess.Popen(exe_args)
    



if __name__ == "__main__":
    
    logFile = properties['logFile']
    useLog = True
    flags = ['-h','-v','-create','-log']

    try:
        lineargs = parse_arguments(argv,flags,'-')
        useLog = '-log' in lineargs
        if '-logdir' in lineargs:
            logFile = f"{lineargs['-dir']}/{properties['logFile']}"


        if '-h' in lineargs:
            print(help)
        elif '-v' in lineargs:
            print(properties['version'])
        elif '-create' in lineargs:
            outfile = "run_template.json"
            if "-dir" in lineargs:
                outfile = f"{lineargs['-dir']}/{outfile}"

            template = {
                "javaHome": "",
                "vmArgs":["-jar"],
                "program":"your_file",
                "programArgs":[],
                "useJavaw": False,
                "cwd":"",
                "useExe": False,
                "log": False,
                "logDir":"",
            }

            with open(outfile, 'w', encoding='utf-8') as f:
                f.write(json.dumps(template, indent=4))
            
        else:
            run(lineargs, useLog)
    except Exception as e:
        with open(logFile,'w', encoding='utf-8') as f:
                f.write("=====JRUNNER\n")
                f.write(str(e))
        if not useLog:
            raise


