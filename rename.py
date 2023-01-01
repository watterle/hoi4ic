
import os

os.chdir(r'C:\\Users\\cero\\Documents\\Paradox Interactive\\savefilecheck\\save\\')
print(os.getcwd())

for count, f in enumerate(os.listdir()):
	f_name, f_ext = os.path.splitext(f)
	f_name = "save" + str(count+1)

	new_name = f'{f_name}{f_ext}'
	os.rename(f, new_name)
