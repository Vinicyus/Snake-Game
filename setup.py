import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Snake",
    options={"build_exe":{"packages":["pygame"], "include_files":["apple.png","snakeHead.png","rock.png","background.mp3","AppleBite.wav","Smashing.wav"]}},
    description = "Snake Game",
    executables = executables
    )