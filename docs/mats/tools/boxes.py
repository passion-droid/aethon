# Measurement boxes in the 1500x2000 display coordinates of each photo
PRADO = '/root/.claude/uploads/11291d80-3cfa-55af-b5f0-c668ea659755/5c94c8c0-image.jpg'
VINYL = '/root/.claude/uploads/11291d80-3cfa-55af-b5f0-c668ea659755/2bf618bc-image.jpg'
cols = [(100,390),(480,780),(860,1160)]
rows = [(110,290),(380,570),(650,840),(920,1110),(1195,1380)]
names = [['CIEL 5','LIGHT BLUE 10','DARK BLUE 15'],
         ['LIGHT GREY 4','LIGHT GREEN 9','DARK GREEN 14'],
         ['GOLD 3','YELLOW 8','DARK GREY 13'],
         ['BEIGE 2','ORANGE 7','BROWN 12'],
         ['WHITE 1','RED 6','BORDEAUX 11']]
PRADO_BOXES = {names[r][c]:(cols[c][0],rows[r][0],cols[c][1],rows[r][1]) for r in range(5) for c in range(3)}
PRADO_BOXES['BLACK 16'] = (1240,300,1400,1200)
PRADO_BOXES['_paper'] = (100,1480,580,1800)
PRADO_BOXES['_marble A'] = (720,1500,1150,1780)
PRADO_BOXES['_marble B'] = (1260,1500,1450,1800)
PRADO_BOXES['_marble C'] = (100,1900,1400,1980)
VINYL_BOXES = {
 'grey':(330,660,470,770), 'anthracite':(450,770,600,850), 'black':(380,930,620,1030),
 'black-grey mix':(400,1090,580,1180), 'beige':(418,1232,500,1292), 'beige-brown mix':(338,1282,386,1350),
 'brown':(190,1210,268,1380), 'green':(15,1110,110,1260),
 '_paper':(800,650,1350,1350), '_marble A':(800,1600,1400,1900), '_marble B':(500,60,1400,250)}
