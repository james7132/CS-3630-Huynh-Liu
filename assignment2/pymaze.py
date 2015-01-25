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

    def get_path(self,start,exit):
        import heapq
        width, height = self.size
        dead_end = [4 - sum(x) for x in self]
        old_direction = [2, 3, 0, 1]
        offsets = [1, width, -1, -width]

        #useDeadEnd = True       # change to test

        # if useDeadEnd:
        #     # DEAD END START
        #     width = 50
        #     height = 50
        #
        #     dead_end = [4 - sum(x) for x in self]
        #
        #     dead_end[start] = 50*50+1
        #     dead_end[exit] = 50*50+1
        #
        #     unprocessed = [i for i,v in enumerate(dead_end) if v == 1]
        #     random.shuffle(unprocessed)
        #
        #     while unprocessed:
        #         current = unprocessed.pop()
        #         if 0 < dead_end[current] <= 2:
        #             neighbor = [current + 1, current + width, current - 1, current - width]
        #             valid_successors = []
        #             for i,v in enumerate(self[current]):
        #                 n = neighbor[i]
        #                 if v == 0 and 0 <= n < width * height and dead_end[n] > 1:
        #                     valid_successors.append(n)
        #             unprocessed += valid_successors
        #             dead_end[current] = 1
        #             #screen.fill(0x444444,rectslist[current])
        #             #display.update(rectslist[current])
        #         else:
        #             dead_end[current] -= 1
        #
        #     dead_path = []
        #     current =  start
        #     old = -1
        #     useAStar = False
        #     while current != exit:
        #         n = [current + 1, current + width, current - 1, current - width]
        #         valid = [v for i,v in enumerate(n) if self[current][i] == 0 and dead_end[v] > 1 and v != old]
        #         dead_path.append(current)
        #         old = current
        #         if len(valid) == 1:
        #             current = valid[0]
        #         elif valid:
        #             print "Using AStar Instead"
        #             useAStar = True
        #             break
        #         else:
        #             print "Path Not Found"
        #             return []
        #     if not useAStar:
        #         dead_path.append(current)
        #         return dead_path
        #

            # DEAD END END

        def heuristic(s, e):
            return abs(s % width - e % width) + abs(s / width - e / width)

        def rebuildPath(rebuild):
            solution = [rebuild]
            while rebuild in ancestor:
                #screen.fill(0xFF00FF, rectslist[current])
                #display.update(rectslist[current])
                #zprint rebuild
                prev = ancestor[rebuild]
                addedPoints = None
                if prev < rebuild:
                    if (prev - rebuild) % width == 0:
                        addedPoints = range(prev, rebuild, width)
                    else:
                        addedPoints = range(prev, rebuild)
                else:
                    if (prev - rebuild) % width == 0:
                        addedPoints = range(prev, rebuild, -width)
                    else:
                        addedPoints = range(prev, rebuild, -1)
                solution = addedPoints + solution
                rebuild = prev
            return solution

        g = {start: 0}

        closedList = set()
        openList = [(heuristic(start, exit), start)]     # (f, location)
        ol = set([start])
        heapq.heapify(openList)
        ancestor = {}

        while openList:
            node = heapq.heappop(openList)[1]
            #screen.fill(0x00FFFF,rectslist[node[1]])
            #display.update(rectslist[node[1]])
            ol.remove(node)
            if node == exit:
                #print "Path found!"
                return rebuildPath(exit)

            closedList.add(node)
            # [right, up, left, down]
            for i, dir in enumerate(self[node]):
                if dir == 1:
                    continue
                neighbor = node + offsets[i]
                if neighbor in closedList or neighbor < 0 or neighbor > width * height: # if out of bounds, continue
                    continue

                current = neighbor      # explore along corridor until a junction or dead end is hit
                old = node
                pathLength = 1
                lastNode = node
                currentDirection = i
                while dead_end[current] == 2:
                    if current == exit:
                        ancestor[current] = lastNode
                        return rebuildPath(exit)
                    #screen.fill(0xFFFF00, rectslist[current])
                    #display.update(rectslist[current])
                    old = current
                    neighbors = self[current]
                    if neighbors[currentDirection] == 0:
                        current += offsets[currentDirection]
                    else:
                        ancestor[current] = lastNode
                        lastNode = current
                        n = [current + 1, current + width, current - 1, current - width]
                        for j, v in enumerate(n):
                            # Old Direction = Opposite of Current Direction
                            # Right (0) <-> Left (2), 0000 <-> 0010
                            # Up (1) <-> Down (3),    0001 <-> 0011
                            # Thus if j == currentDirection XOR 2, then v == old
                            if neighbors[j] == 0 and currentDirection ^ 0x2 != j:
                                currentDirection = j
                                current = v
                                break
                    pathLength += 1
                ancestor[current] = lastNode

                #screen.fill(0x0000FF, rectslist[current])
                #display.update(rectslist[current])

                if pathLength > 1:
                    closedList.add(old)

                if dead_end[current] == 1:
                    #screen.fill(0x000000, rectslist[current])
                    #display.update(rectslist[current])
                    if current == exit:
                        return rebuildPath(exit)
                elif current not in ol:
                    g[current] = g[node] + pathLength
                    currentF = g[current] + heuristic(current, exit)
                    ol.add(current)
                    heapq.heappush(openList, (currentF, current))

        #print "Path not found!"
        return []


    def get_image_and_rects(self,cellulesize,wallcolor=(0,0,0),celcolor=(255,255,255)):
        x,y = cellulesize
        image = Surface((x*(self.size[0]),y*self.size[1]))
        image.fill(wallcolor)
        rects = []
        for e,i in enumerate(self):
            rects.append(image.fill(celcolor,(e%(self.size[0])*cellulesize[0]+1-(not i[2]),e/(self.size[0])*cellulesize[1]+1-(not i[3]),cellulesize[0]-2+(not i[2])+(not i[0]),cellulesize[1]-2+(not i[1])+(not i[3]))))
        return image,rects

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
    start = 0#random.randrange(len(L))
    exit = 50*50-1#random.randrange(len(L))
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
    notFound = 0
    w, h = 50, 50
    incorrect = 0
    for i in range(tests):
        l = labyrinthe((w, h))
        s = random.randrange(len(l))
        e = random.randrange(len(l))
        while e == s:
            e = random.randrange(len(l))
        timeStart = time.time()
        path = l.get_path(s, e)
        times.append(time.time() - timeStart)
        if len(path) == 0:
            notFound += 1
        else:
            last = s
            i = 1
            marked = False
            while i < len(path):
                if not ((last - path[i]) % w != 0 or abs(last - path[i]) != 1):
                    print "Movement: ", last, path[i], (last - path[i]) % w
                    marked = True
                    break
                if path[i] < last:
                    if (last - path[i]) % w == 0:
                        if l[last][3] == 1:
                            print "Up Movment: ", last, path[i], l[last][3]
                            marked = True
                            break
                    else:
                        if l[last][2] == 1:
                            print "Left Movment: ", last, path[i], l[last][2]
                            marked = True
                            break
                else:
                    if (last - path[i]) % w == 0:
                        if l[last][1] == 1:
                            print "Down Movement: ", last, path[i], l[last][2]
                            marked = True
                            break
                    else:
                        if l[last][0] == 1:
                            print "Right Movment: ", last, path[i], l[last][2]
                            marked = True
                            break
                last = path[i]
                i += 1
            if path[0] != s:
                print "Start: ", path[0], s
                marked = True
            if path[-1] != e:
                print "End: ", path[-1], e
                marked = True
            if marked:
                print path
                incorrect += 1

        ed = abs(s % l.size[0] - e % l.size[0]) + abs(s / l.size[0] - e / l.size[0])
        pl = len(path)
        crs.append(pl / (float(ed)))
    print "Average time:", sum(times) / float(len(times))
    print "Average CR:", sum(crs) / float(len(crs))
    print "Unsolvable mazes (%):", (notFound / float(len(times)))
    print "incorrect: ", incorrect
