import math
import os


def make_time(num):
	hour = str(int(num / 3600))
	if len(hour) == 1:
		hour = "0" + hour
	minu = str(int(num % 3600 / 60))
	if len(minu) == 1:
		minu = "0" + minu
	seco = str(int(num % 60))
	if len(seco) == 1:
		seco = "0" + seco
	return f"{hour}:{minu}:{seco}"


def cut(file, step=30):
	start = 0
	count = 1
	i = 0
	while i < count:
		start_time = make_time(start)
		p, ext = file.rsplit(".", 1)
		output = f"{p}-{i+1}.{ext}"
		cmd = f"ffmpeg -i {file} -ss {start_time} -t {step} {output}"
		print(cmd, count)
		os.system(cmd)
		if i == 0:
			total = os.path.getsize(file)
			size = os.path.getsize(output)
			count = math.ceil(total / size)

		start += step 
		i += 1


if __name__ == "__main__":
	file = "9ad6ba91243791579843741011-f0.aac"
	cut(file)
