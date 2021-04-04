
import sys
import os
import configparser

global mat_data
mat_data = {}

def gen_mtl(mtlname, tex):
	output = ""
	output += "\n"
	output += "newmtl {}\n".format(mtlname)
	output += "Ns 225.000000\n"
	output += "Ka 1.000000 1.000000 1.000000\n"
	output += "Kd 0.800000 0.800000 0.800000\n"
	output += "Ks 0.500000 0.500000 0.500000\n"
	output += "Ke 0.000000 0.000000 0.000000\n"
	output += "Ni 1.450000\n"
	output += "d 1.000000\n"
	output += "illum 2\n"
	output += "map_Kd {} \n".format(tex)
	output += "\n"
	#open("examples/ZZ/{}.mtl".format(tex),"w").writelines(output)
	return output

def mat_reader(filepath):
	print("MATREAD {}...".format(filepath))
	data = open(filepath,"r").readlines()
	for i in range(len(data)):
		data[i] = data[i].rstrip()
	counter = 0
	result = 0
	endpoint = 0
	chunks = []
	for line in data:
		line = line.rstrip()
		counter = counter + 1
		if line == "[MaterialBegin]":
			startpoint = counter
		if line == "[MaterialEnd]":
			endpoint = counter-1
			chunk = data[startpoint:endpoint]
			chunks.append(chunk)

	result = {}
	output = ""
	for chunk in chunks:
		for item in chunk:
			item = item.split(" ")
			if len(item) < 2:
				continue
			result[item[0]] = item[1]
			#print("{} : {}".format(item.split(" ")[0], item.split(" ")[1]))
		#mat_data[result["Name="]] = result["Texture="]
		output+=(gen_mtl(result["Name="],result["Texture="]))
	filepath = filepath[:-4]
	open("{}.mtl".format(filepath), "w").writelines(output)
	pass

def convert_sco_to_obj(filepath, normalised):
	basename = filepath[:-4]
	print("reading {}...".format(basename))
	data = open(filepath,"r").readlines()

	vertline = data[3]
	vertCount = int(vertline.split(" ")[1])  #get used to this ugly mess, lots of random string parsing in here with stray \n and \t
 
	centrepointdata = data[2].rstrip().split(" ") #there much be a better way of doing this, surely
	centrepoint = (centrepointdata[1], centrepointdata[2], centrepointdata[3])
	print("CentrePoint at {}".format(centrepoint))

	data = data[4:]

	out = []

	#Vert section
	verts = []
	print("contains {} verts".format(vertCount))
	for i in range(vertCount):
		vertexData = (data[i].rstrip().split())

		# So because the model format has it's positions baked into the vertex data, the 'normalised' option will take away the centrepoints so the model loads in at the origin
		if normalised:
			vertexData[0] = float(vertexData[0]) - float(centrepoint[0])
			vertexData[1] = float(vertexData[1]) - float(centrepoint[1])
			vertexData[2] = float(vertexData[2]) - float(centrepoint[2])

		verts.append("v {} {} {}".format(vertexData[0], vertexData[1], vertexData[2]))
		pass

	faceCount = int(data[vertCount].split(" ")[1].rstrip()) #Dear mother of god
	print("contains {} faces".format(faceCount))

	#Changing the data chunk to be just the faces to make it easier
	data = data[vertCount+1:]

	#face section
	vts = []
	fs = []
	for i in range(faceCount):
		line = data[i]
		lineprim = (line.split("\t"))
		for x in range(len(lineprim)):
			lineprim[x] = lineprim[x].rstrip()
		#print(lineprim[2])
		mtlname = lineprim[2]
		#tex = (mat_data[texname])
		#gen_mtl(tex[:-4], tex, texname)

		#Get the texture coords data
		vtlinedata = (lineprim[-1].rstrip().split(" "))
		#the Y coords are messed up and need to be made positive for some reason
		vtlinedata[1] = float(vtlinedata[1]) * -1
		vtlinedata[3] = float(vtlinedata[3]) * -1
		vtlinedata[5] = float(vtlinedata[5]) * -1

		vts.append("vt {} {}".format(vtlinedata[0], vtlinedata[1]))
		vts.append("vt {} {}".format(vtlinedata[2], vtlinedata[3]))
		vts.append("vt {} {}".format(vtlinedata[4], vtlinedata[5]))

		#This data comes in horribly messed up
		#first line sanitises the line to be just the data we want
		#second line is just a faster way of removing any blank items, since the spaces are messed up and the list usually returns a bunch of blanks in the middle which mess up indexing 
		vlinedata = (lineprim[1].rstrip().split(" "))
		vlinedata = list(filter(None, vlinedata))

		#SCO stars indexing at 0, obj starts at 1.
		for v in range(len(vlinedata)):
			vlinedata[v] = int(vlinedata[v]) + 1

		fs.append("usemtl {}".format(mtlname))

		#The 'len(vts)-2' stuff here is just my stupid way of indexing backwards.
		fs.append("f {}/{} {}/{} {}/{}".format(
			vlinedata[0], len(vts)-2,
			vlinedata[1], len(vts)-1,
			vlinedata[2], len(vts)-0,
		))

	##Combine verts and faces
	out.append("mtllib {}.mtl".format(mat_name))
	for i in range(len(verts)):
		out.append(verts[i])
	for i in range(len(vts)):
		out.append(vts[i])
	for i in range(len(fs)):
		out.append(fs[i])

	#Write section
	with open("{}.obj".format(basename),"w") as outfile:
		outfile.write("#{}.obj \n".format(basename))
		outfile.write("#CentrePoint: {} \n".format(centrepoint))
		for line in out:
			outfile.write(line)
			outfile.write("\n")
		print("outputted to {}.obj".format(basename))
	return out

global mat_name
mat_name = ""

#point to folder
if len(sys.argv) > 1:
	folderpath = (sys.argv[1])
	for file in os.listdir(folderpath):
		filepath = folderpath + "/" + file
		if file.endswith(".mat"):
			mat_reader(filepath)
			mat_name = file[:-4]
			print("\n")
	for file in os.listdir(folderpath):
		filepath = folderpath + "/" + file
		if file.endswith(".sco"):
			convert_sco_to_obj(filepath, True)
			print("\n")
			pass

##Args for CLI
#if len(sys.argv) > 1:
	#filepath = (sys.argv[1])
	#convert_sco_to_obj(filepath, True)