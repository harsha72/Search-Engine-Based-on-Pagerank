import pickle

inp = open("Database/thousand_names.txt",'r',encoding="utf8")
names = inp.read().splitlines()

dicto = {}

def add_to_index(word,name):
	lower_word = word.lower()
	if word in dicto:
		if name not in dicto[word]:
			dicto[word].append(name)
		if not(lower_word == word):
			if name not in dicto[lower_word]:
				dicto[lower_word].append(name)

	else:
		dicto[word] = [name]
		if not (lower_word == word):
			if lower_word in dicto:
				if name not in dicto[lower_word]:
					dicto[lower_word].append(name)
			else:
				dicto[lower_word] = [name]


for name in names:
	name_edit = name.replace('/','-')
	textin = open("Database/"+name_edit+".txt",'r',encoding="utf8")
	text = textin.read().splitlines()
	check = 0
	for lines in text:
		if(lines == "#######"):
			check+=1
		if(check == 2 and not lines == "#######"):
			words = lines.split()
			for word in words:
				add_to_index(word,name)

def save_obj(obj,name):
	with open('Database/'+name+'.pkl','wb') as f:
		pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

save_obj(dicto,"dicto")


