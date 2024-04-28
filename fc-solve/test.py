import subprocess

with open('myfile.txt', "w") as outfile:
    # subprocess.run(my_cmd, stdout=outfile)
    subprocess.run(["fc-solve", "-m", "temp.txt"], stdout=outfile) 