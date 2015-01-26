# Assignment 2
# Alexander Huynh - 902888855 - a.huynh@gatech.edu
# James Liu - 902813083 - jliu348@gatech.edu

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
        import heapq                            # used for priority queue in A*
        width, height = self.size               # store a reference to the size of the maze
        offsets = [1, width, -1, -width]        # used to determine the new location from an old location [R, U, L, D]

        dead_end = [4 - sum(x) for x in self]   # pre-process: compute the number of successors for each node

        # uncomment the DEAD END section to test dead end filling
        # DEAD END START
        # width = 50
        # height = 50
        #
        # dead_end = [4 - sum(x) for x in self]
        #
        # dead_end[start] = 50*50+1
        # dead_end[exit] = 50*50+1
        #
        # unprocessed = [i for i,v in enumerate(dead_end) if v == 1]
        # random.shuffle(unprocessed)
        #
        # while unprocessed:
        #     current = unprocessed.pop()
        #     if 0 < dead_end[current] <= 2:
        #         neighbor = [current + 1, current + width, current - 1, current - width]
        #         valid_successors = []
        #         for i,v in enumerate(self[current]):
        #             n = neighbor[i]
        #             if v == 0 and 0 <= n < width * height and dead_end[n] > 1:
        #                 valid_successors.append(n)
        #         unprocessed += valid_successors
        #         dead_end[current] = 1
        #         #screen.fill(0x444444,rectslist[current])
        #         #display.update(rectslist[current])
        #     else:
        #         dead_end[current] -= 1
        #
        # dead_path = []
        # current =  start
        # old = -1
        # useAStar = False
        # while current != exit:
        #     n = [current + 1, current + width, current - 1, current - width]
        #     valid = [v for i,v in enumerate(n) if self[current][i] == 0 and dead_end[v] > 1 and v != old]
        #     dead_path.append(current)
        #     old = current
        #     if len(valid) == 1:
        #         current = valid[0]
        #     elif valid:
        #         print "Using AStar Instead"
        #         useAStar = True
        #         break
        #     else:
        #         print "Path Not Found"
        #         return []
        # if not useAStar:
        #     dead_path.append(current)
        #     return dead_path
        #
        # DEAD END END

        # Manhattan Distance heuristic for use with A*
        def heuristic(s, e):
            return abs(s % width - e % width) + abs(s / width - e / width)

        # return the actual path, using the ancestor list, starting at parameter rebuild
        def rebuildPath(rebuild):
            solution = [rebuild]
            while rebuild in ancestor:
                prev = ancestor[rebuild]
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
            # uncomment to recolor the start and exit
            screen.fill(0xFF0000, rectslist[start])
            display.update(rectslist[start])
            screen.fill(0x00FF00, rectslist[exit])
            display.update(rectslist[exit])
            # end uncomment
            return solution

        # normal A-Star setup
        g = {start: 0}

        closedList = set()
        openList = [(heuristic(start, exit), start)]    # (f, location)
        ol = {start}                                    # sacrifice space to speed up checking membership in open list
        heapq.heapify(openList)
        ancestor = {}                                   # maps a location to a predecessor location

        # uncomment to see a time delay
        import time

        while openList:
            node = heapq.heappop(openList)[1]           # pop the location with the lowest f-cost
            ol.remove(node)

            # uncomment to see a time delay
            time.sleep(.1)

            # uncomment to see green for nodes that were popped from the open list
            screen.fill(0x22CC22, rectslist[node])
            display.update(rectslist[node])
            # end uncomment

            if node == exit:                            # check if the goal was reached
                return rebuildPath(exit)

            # [right, up, left, down]
            for i, dir in enumerate(self[node]):        # check all 4 directions
                if dir == 1:                            # if there is a wall, continue
                    continue
                neighbor = node + offsets[i]
                if neighbor in closedList or neighbor < 0 or neighbor > width * height: # if out of bounds, continue
                    continue

                # explore along corridor until a junction or dead end is hit
                current = neighbor
                old = node
                pathLength = 1
                lastNode = node
                currentDirection = i
                while dead_end[current] == 2:           # while we are in a corridor
                    # uncomment to see a time delay
                    time.sleep(.025)

                    if current == exit:                 # check for goal while traversing a corridor
                        ancestor[current] = lastNode
                        return rebuildPath(exit)
                    old = current
                    neighbors = self[current]
                    if neighbors[currentDirection] == 0:
                        # uncomment to see pink for straight corridors that were traversed through
                        screen.fill(0xFF7777, rectslist[current])
                        display.update(rectslist[current])
                        # end uncomment
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
                                # uncomment to see darker pink for corner corridors that were traversed through
                                screen.fill(0xFF4444, rectslist[current])
                                display.update(rectslist[current])
                                # end uncomment
                                current = v
                                break
                    pathLength += 1
                ancestor[current] = lastNode
                closedList.add(old)

                if dead_end[current] == 1:  # check for goal if we ended up in a dead end
                    # uncomment to see gray for corner corridors that were traversed through
                    screen.fill(0x777777, rectslist[current])
                    display.update(rectslist[current])
                    # end uncomment
                    if current == exit:
                        return rebuildPath(exit)
                elif current not in ol:     # normal A-Star update
                    currentG = g[current] = g[node] + pathLength
                    currentF = currentG + heuristic(current, exit)
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

# called from the python console with parameter tests = number of tests to run
def test(tests):
    import time
    times = []              # the time it takes for each get_path(...) to run
    crs = []                # the CR of each test
    branchingOne = []       # % of maze that is straight corridor or dead end
    branchingCorner = []    # % of maze that is corner corridor
    notFound = 0            # count of unsolvable maze
    w, h = 50, 50           # size of maze
    incorrect = 0           # count of incorrect solutions
    for t in range(tests):                      # run 'tests' number of tests
        l = labyrinthe((w, h))                  # generate a maze
        s = random.randrange(len(l))            # randomize the start location
        e = random.randrange(len(l))            # randomize the end location
        while e == s:                           # guarantee that the start and end location are not the same
            e = random.randrange(len(l))
        timeStart = time.time()                 # start timing get_path(...)
        path = l.get_path(s, e)                 # generate the path
        times.append(time.time() - timeStart)   # add the time it took for get_path(...) to run

        # collect statistics on this generated maze
        dead_end = [4 - sum(x) for x in l]
        corn = 0            # number of corners
        for d in l:
            if sum(d) == 2 and not (d[0] == d[2] and d[1] == d[3]):
                corn += 1
        branchingCorner.append(corn / float(len(l)))
        branchingOne.append((sum([1 if d <= 2 else 0 for d in dead_end]) - corn) / float(len(l)))

        if len(path) == 0:      # if get_path(...) returns [], a path was not found
            notFound += 1
        else:                   # otherwise, a path was found; validate it
            last = s
            j = 1
            marked = False
            while j < len(path):
                if not ((last - path[j]) % w != 0 or abs(last - path[j]) != 1):
                    print "Movement:", last, path[j], (last - path[j]) % w
                    marked = True
                    break
                if path[j] < last:
                    if (last - path[j]) % w == 0:
                        if l[last][3] == 1:
                            print "Up Movement:", last, path[j], l[last][3]
                            marked = True
                            break
                    else:
                        if l[last][2] == 1:
                            print "Left Movement:", last, path[j], l[last][2]
                            marked = True
                            break
                else:
                    if (last - path[j]) % w == 0:
                        if l[last][1] == 1:
                            print "Down Movement:", last, path[j], l[last][2]
                            marked = True
                            break
                    else:
                        if l[last][0] == 1:
                            print "Right Movement:", last, path[j], l[last][2]
                            marked = True
                            break
                last = path[j]
                j += 1
            if path[0] != s:
                print "Start: ", path[0], s
                marked = True
            if path[-1] != e:
                print "End: ", path[-1], e
                marked = True
            if marked:
                print path
                incorrect += 1
        # calculate Euclidean Distance between start and exit
        ed = abs(s % l.size[0] - e % l.size[0]) + abs(s / l.size[0] - e / l.size[0])
        # calculate the length of the actual path taken
        pl = len(path)
        # add the CR for this maze's solution
        crs.append(pl / (float(ed)))
    # output the results
    print "Average time:", sum(times) / float(tests)
    print "Average CR:", sum(crs) / float(len(crs))
    print "Unsolvable mazes (%):", (notFound / float(tests))
    print "Incorrect solutions:", incorrect
    print "Average straight corridors or dead ends (%):", sum(branchingOne) / float(tests)
    print "Average corner corridors (%):", sum(branchingCorner) / float(tests)
