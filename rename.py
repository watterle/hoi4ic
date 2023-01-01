
import os

absolute_path = os.path.dirname(__file__)
relative_path = "save\\"
folderpath = os.path.join(absolute_path, relative_path)
os.chdir(folderpath)

for count, f in enumerate(os.listdir()):
	f_name, f_ext = os.path.splitext(f)
	f_name = "save" + str(count+1)

	new_name = f'{f_name}{f_ext}'
	os.rename(f, new_name)
