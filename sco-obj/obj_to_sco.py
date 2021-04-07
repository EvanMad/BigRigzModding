def convert_obj_to_sco(filepath):

	template = """[ObjectBegin]
Name= ZZ_Body
CentralPoint= 0 0 0
Verts= {}\n"""

	face_template = "3	 {}  {}  {}	Body                	{} {} {} {} {} {}\n"

	basename = filepath[:-4]
	data = open(filepath, "r").readlines()
	verts = []
	texcoords = {}
	faces = []
	out = []
	i = 0
	for line in data:
		line = line.rstrip()
		line = line.split(" ")
		opcode = line[0]
		#print(opcode)
		if line == "mtllib":
			pass
		if opcode == "v":
			verts.append((line[1], line[2], line[3]))
			#verts.append(line[2])
			#verts.append(line[3])
			pass
		if opcode == "vt":
			texcoords[i] = [line[1], line[2]]
			i+=1
			#texcoords.append(line[1])
			#texcoords.append(line[2])
			pass
	print(len(texcoords))
	print(len(verts))
	if len(texcoords) == 0:
		hastexcoords = False
	else:
		hastexcoords = True
	for line in data:
		line = line.rstrip()
		line = line.split(" ")
		opcode = line[0]
		if opcode == "f":

			faceindex1 = line[1].split("/")
			faceindex2 = line[2].split("/")
			faceindex3 = line[3].split("/")

			facevertindex1 = int(faceindex1[0])-1
			facevertindex2 = int(faceindex2[0])-1
			facevertindex3 = int(faceindex3[0])-1

			texcoordindex1 = int(faceindex1[1])-1
			texcoordindex2 = int(faceindex2[1])-1
			texcoordindex3 = int(faceindex3[1])-1
			if hastexcoords:
				texcoords[texcoordindex1][1] = float(texcoords[texcoordindex1][1])*-1
				texcoords[texcoordindex2][1] = float(texcoords[texcoordindex2][1])*-1
				texcoords[texcoordindex3][1] = float(texcoords[texcoordindex3][1])*-1
			else:
				texcoords[texcoordindex1] = [0,1]
				texcoords[texcoordindex2] = [0,1]
				texcoords[texcoordindex3] = [0,1]

			newline = face_template
			#print(facevertindex2)
			newline = newline.format(
				facevertindex1,
				facevertindex2,
				facevertindex3,
				texcoords[texcoordindex1][0],
				texcoords[texcoordindex1][1],
				texcoords[texcoordindex2][0],
				texcoords[texcoordindex2][1],
				texcoords[texcoordindex3][0],
				texcoords[texcoordindex3][1],
			)
			faces.append(newline)
			pass

	template = (template.format(len(verts)))
	#out.append(template)
	out.append(verts)
	#out.append(faces)
	with open("test.sco","w") as outfile:
		outfile.write(template)
		for vert in verts:
			outfile.write("{} {} {}\n".format(vert[0], vert[1], vert[2]))
		outfile.write("faces= {}\n".format(len(faces)))
		outfile.writelines(faces)
		outfile.write("[ObjectEnd]\n")


		#for chunk in out:
		#	print(type(chunk))
		#	for line in chunk:
		#		outfile.write(line)
		#		outfile.write("\n")
		#		pass
		pass
convert_obj_to_sco("Penis4.0.obj")