import pygame
import time 
import random
import os
from points import Point
#Map
import folium
#Geolocation
import json
from geopy.distance import geodesic


#window setting
pygame.font.init()
os.environ['SDL_VIDEO_CENTERED']='1'
pygame.init()
width, height = 900, 500
pygame.display.set_caption("Traveling salesman ")
screen = pygame.display.set_mode((width, height))
fps = 100
clock = pygame.time.Clock()


#Colors and BackGround
black = (0, 0, 0)
white = (255, 255, 255)
Red = (234, 67, 53)
yellow = (255, 255, 0)
Bleu = (102, 157, 246)
green = (0, 138, 78)
bg = pygame.image.load("bg.png")


#variables
points = []
offset_screen = 50
number_of_point = 10
smallest_path = []
record_distance = 0

#Map

#morrocco [31.791702, -7.092620]
m = folium.Map(location=[35.770390, -5.803610], zoom_start=13)
overlay = os.path.join('data','overlay.json')
locations = os.path.join('data','locations.json')
coordinates = []
nodes = ()
Lnodes = list(nodes)

distances = {}

with open(locations) as f:
    d = json.load(f)
    for location in d['features']:
        #print(location['geometry']['coordinates'][1])
        Lnodes.append(len(coordinates)+1)
        nodes = tuple(Lnodes)
        if(len(coordinates)==0):
            folium.Marker([location['geometry']['coordinates'][1],location['geometry']['coordinates'][0]],
            popup="<strong>'Start Point '</strong>",
            tooltip=len(coordinates)+1,
            icon=folium.Icon(color='green')).add_to(m)
        
        else:
            folium.Marker([location['geometry']['coordinates'][1],location['geometry']['coordinates'][0]],popup="<strong>Location Number :{}</strong>".format(len(coordinates)+1),tooltip=len(coordinates)+1).add_to(m)

        coordinates.append([location['geometry']['coordinates'][1],location['geometry']['coordinates'][0]])
#print(coordinates)
coordinates.append(coordinates[0])
Lnodes.append(len(coordinates))
nodes = tuple(Lnodes)
#print(coordinates)

#print(nodes)
for dn in nodes:
    nodd = {}
    for nd in nodes:
        if nd !=dn:
            start = coordinates[nodes.index(dn)]
            end = coordinates[nodes.index(nd)]
            distBtwn = geodesic(start, end).kilometers
            nodd.update({nd:distBtwn })
            distances.update({dn:nodd})

#print(distances)
#print(geodesic(coordinates[0], coordinates[1]).kilometers)


unvisited = {node: None for node in nodes} #using None as +inf
visited = {}
current = 1
currentDistance = 0
unvisited[current] = currentDistance

while True:
    for neighbour, distance in distances[current].items():
        if neighbour not in unvisited: continue
        newDistance = currentDistance + distance
        if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
            unvisited[neighbour] = newDistance
    visited[current] = currentDistance
    del unvisited[current]
    if not unvisited: break
    candidates = [node for node in unvisited.items() if node[0]]
    current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

print(visited)
cords = []
for visit in visited.keys():
    cords.append(coordinates[visit-1])
    print(list(visited).index(visit))
    my_PolyLine=folium.PolyLine(locations=cords,weight=5).add_to(m)
#print(json.dumps(locations))
folium.GeoJson(overlay,name='morrocco').add_to(m)
m.save('map.html')

#Generate points
for n in range(number_of_point):
    x = random.randint(offset_screen, width-offset_screen)
    y = random.randint(offset_screen, height-offset_screen)

    point = Point(x, y)
    points.append(point)



#shuffle points list
def shuffle(a, b, c):
    temp = a[b]
    a[b] = a[c]
    a[c] = temp
print(range(len(points)-1))
#distance betweenpoints
def calculate_distance(points_list):
    total = 0
    for n in range(len(points)-1):
        distance = ((points[n].x - points[n+1].x )**2 + (points[n].y - points[n+1].y )**2) ** 0.5
        total += distance
    return total

dist= calculate_distance(points)
record_distance = dist
print(dist)
slice_object = slice(number_of_point)
smallest_path = points.copy()

myfont = pygame.font.SysFont('Comic Sans MS', 20)
a =[]
for n in range(len(smallest_path)):
    a.append((smallest_path[n].x, smallest_path[n].y))

textsurface = myfont.render("the smallest path is: " , False, (255, 255, 255))
textsurface1 = myfont.render(str(a), False, (255, 255, 255))
textsurface3 = myfont.render("the distance is :", False, (25, 41, 255))
textsurface4 = myfont.render(str(record_distance), False, (255, 255, 0))


run = True
while run:
    screen.fill(black)
    screen.blit(bg, (0, 0))
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #draw lines between points

    for n in range(len(points)):
        pygame.draw.circle(screen, Red, (points[n].x, points[n].y), 8)

    a = random.randint(0, len(points)-1)
    b = random.randint(0, len(points)-1)
    shuffle(points, a, b)

    dist = calculate_distance(points)
    if dist < record_distance:
        record_distance = dist
        smallest_path = points.copy()

    for m in range(len(points)-1):
        pygame.draw.line(screen, white, (points[m].x, points[m].y), (points[m+1].x, points[m+1].y), 1)
    

    for m in range(len(smallest_path)-1):
        pygame.draw.line(screen, Bleu, (smallest_path[m].x, smallest_path[m].y), (smallest_path[m+1].x, smallest_path[m+1].y), 5)

    pygame.display.update()

screen.blit(textsurface,(0,0))
screen.blit(textsurface1,(20,20))
screen.blit(textsurface3,(20,40))
screen.blit(textsurface4,(130,60))
pygame.display.update()

time.sleep(5)
pygame.quit()
