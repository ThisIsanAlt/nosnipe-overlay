from cx_Freeze import setup, Executable
  
setup(name = "nosnipe" ,
      version = "0.0.1" ,
      description = "sweting's NoSnipe Overlay" ,
      executables = [Executable("main.py")])