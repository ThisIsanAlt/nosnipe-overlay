from cx_Freeze import setup, Executable
  
setup(name = "nosnipe" ,
      version = "0.0.1" ,
      description = "" ,
      executables = [Executable("main.py")])