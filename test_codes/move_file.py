import shutil
import os
from datetime import datetime
file_path = "A/"
target_path = "B/C"

#check if dir exists
#if not os.path.exists(target_path):
#	os.makedirs(target_path)
#	shutil.move(file_path,target_path)
#	print("moved file")
	#create dir and copy 
arrays= []
for x in range(1,9):
	if(x%2 == 0):
		side = 'Left'
	else:
		side = 'Right'
	arrays.append({
		'frame_name': x,
		'side': side,
		'phase':f'{x}',
		'image_path': f'{x}.png',
		'rom_h': '3.6°',
		'rom_k': '4.7°',
		'rom_a': '5.8°',
		'insole': f'00{x}'
		 })
for x in arrays:
	print(x)
print("\n")
#filter array
for x in enumerate([d for d in arrays if d['side'] == 'Right' and d['insole'] == '003']):
	print(x)

#print(datetime.today().strftime('%Y-%m-%d'))
