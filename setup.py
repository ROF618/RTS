from cx_Freeze import setup, Executable

setup(
    name = "clientSideScript",
    version = "0.1",
    description = "Client side script to that connects to server for remote control of machine for a small period of time",
    executables = [Executable("client.py")]
)