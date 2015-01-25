from pygame import*
quit
import random

class labyrinthe(list):
    ''
    def __init__(self,size):
        self.size = size
        labx,laby = size
        lx,ly = labx+2,laby+2
        ref = [1,lx,-1,-lx]
        l=[[random.randrange(lx+1,lx*(ly-1),lx)+random.randint(0,labx),random.choice(ref)]]
        L = list((0,0,0,0)*lx+((0,0,0,0)+(1,1,1,1)*labx+(0,0,0,0))*laby+(0,0,0,0)*lx)
        L = [L[i:i+4] for i in range(0,lx*ly*4,4)]
        self.extend(L)
        while l:
            for i in l:
                a = sum(i)
                b  = (1 if abs(i[1])==lx else lx)*random.choice((1,-1))
                if all(self[a]):
                    c = ref.index(i[1])
                    self[i[0]][c] = 0
                    i[0] = a
                    self[i[0]][c-2] = 0
                    if not random.randint(0,1): l.append([i[0],b])
                    if not random.randint(0,3): l.append([i[0],-b])
                else :
                    if all(self[i[0]+b]): l.append([i[0],b])
                    if all(self[i[0]-b]): l.append([i[0],-b])
                    l.remove(i)
        del(self[:lx])
        del(self[-lx:])
        del(self[::lx])
        del(self[lx-2::lx-1])

    # def get_path(self,start,exit):
        # pos = start
        # d = 1
        # path = [pos]
        # ref = [1,self.size[0],-1,-self.size[0]]
        # while pos != exit:
        # 	if self[pos][ref.index(d)-1] == 0: d = ref[ref.index(d)-1]
        # 	if self[pos][ref.index(d)] == 0:
        # 		pos = pos+d
        # 		path.append(pos)
        # 		i = path.index(pos)
        # 		if i != len(path)-1:
        # 			del(path[i:-1])
        # 	else: d = ref[ref.index(d)-3]
        # return path

    def get_path(self,start,exit):
        import heapq
        import time
        timeStart = time.time()

        def heuristic(start, end):
            return abs(start % 50 - end % 50) + abs(start / 50 - end / 50)

        def rebuildPath(current):
            timeSpent = time.time() - timeStart
            #print 'Rebuilding path...',
            solution = [current]
            while current in ancestor:
                current = ancestor[current]
                solution.append(current)
            #print 'done!'
            #print "Actual distance =", len(solution)
            #print "Euclidean distance =", heuristic(start, exit)
            #print "CR = ", len(solution) / float(heuristic(start, exit))
            #print "Time =", timeSpent, "secs"
            return solution[::-1]

        g = {start: 0}

        closedList = set()
        openList = [(g[start] + heuristic(start, exit), start)]     # (f, location)
        ol = [start]
        heapq.heapify(openList)
        ancestor = {}

        while openList:
            node = heapq.heappop(openList)
            ol.remove(node[1])
            if node[1] == exit:
                #print 'Path found!'
                return rebuildPath(exit)

            #screen.fill(0x7777FF - (len(closedList)),rectslist[node[1]])
            #display.update(rectslist[node[1]])

            closedList.add(node[1])
            neighbors = self[node[1]]
            # [right, up, left, down]
            for i, dir in enumerate(neighbors):
                if dir == 1:                                # if wall, continue
                    continue
                neighbor = node[1] + [1, 50, -1, -50][i]
                if neighbor < 0 or neighbor > 50 * 50:    # if out of bounds, continue
                    continue
                if neighbor in closedList:
                    continue
                if not neighbor in g.keys():
                    g[neighbor] = 0
                neighborG = g[neighbor] + 1
                #if neighbor not in openList or neighborG < g[neighbor]:
                if neighbor not in ol or neighborG < g[neighbor]:
                    ancestor[neighbor] = node[1]
                    g[neighbor] = neighborG
                    neighborF = g[neighbor] + heuristic(neighbor, exit)
                    #if neighbor not in openList:
                    if neighbor not in ol:
                        ol.append(neighbor)
                        heapq.heappush(openList, (neighborF, neighbor))

        print 'Path not found!'
        return []


    def get_image_and_rects(self,cellulesize,wallcolor=(0,0,0),celcolor=(255,255,255)):
        x,y = cellulesize
        image = Surface((x*(self.size[0]),y*self.size[1]))
        image.fill(wallcolor)
        rects = []
        for e,i in enumerate(self):
            rects.append(image.fill(celcolor,(e%(self.size[0])*cellulesize[0]+1-(not i[2]),e/(self.size[0])*cellulesize[1]+1-(not i[3]),cellulesize[0]-2+(not i[2])+(not i[0]),cellulesize[1]-2+(not i[1])+(not i[3]))))
        return image,rects


#****************************************************************************************
#****************************************************************************************
if __name__ == '__main__':
    me = Surface((5,5))
    me.fill(0xff0000)
    L = labyrinthe((50,50))
    labx,laby = 50,50
    screen = display.set_mode((L.size[0]*10,L.size[1]*10))
    image,rectslist = L.get_image_and_rects((10,10),wallcolor=0,celcolor=0xffffff)
    screen.blit(image,(0,0))
    start = random.randrange(len(L))
    exit = random.randrange(len(L))
    screen.fill(0x00ff00,rectslist[exit])
    screen.blit(me,rectslist[start])
    display.flip()
    while event.wait().type != QUIT:
        screen.fill(-1,rectslist[start])
        if key.get_pressed()[K_RIGHT] and not L[start][0]:
            start += 1
        if key.get_pressed()[K_LEFT] and not L[start][2]:
            start += -1
        if key.get_pressed()[K_UP] and not L[start][3]:
            start += -L.size[1]
        if key.get_pressed()[K_DOWN] and not L[start][1]:
            start += L.size[0]
        screen.fill(0xff0000,rectslist[start])
        display.flip()
        if start == exit : print 'YOU WIN'; break
        if key.get_pressed()[K_ESCAPE]:
            for i in L.get_path(start,exit)[1:-1]:
                screen.fill(0x0000ff,rectslist[i])
                display.update(rectslist[i])
                time.wait(20)


def test(tests):
    import time
    times = []
    crs = []
    for i in range(tests):
        l = labyrinthe((50,50))
        timeStart = time.time()
        s = random.randrange(len(l))
        e = random.randrange(len(l))
        while e == s:
            e = random.randrange(len(l))
        path = l.get_path(s, e)
        times.append(time.time() - timeStart)
        ed = abs(s % 50 - e % 50) + abs(s / 50 - e / 50)
        pl = len(path)
        crs.append(pl / (float(ed)))
    print "Average time:", sum(times) / float(len(times))
    print "Average CR:", sum(crs) / float(len(crs))