"""
PROGRAMMER  : ANDI MUHAMMAD RIYADHUS ILMY
CREATE DATE : 2022/08/09 15:00
DESCRIPTION : TBD
"""

class drawMaze:
    def __init__(self, mx, my, ns, scale=None):
        self.x = mx
        self.y = my
        if (scale==None):
            self.scale = 50*mx
        else:
            self.scale = scale
        self.ns = ns
        # self.path = path

        # Set the maze aspect ratio
        self.aspect_ratio = self.x / self.y
        # Pad the maze all around by this amount.
        self.padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        self.height = self.scale
        self.width = int(self.scale * self.aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        self.scy, self.scx = self.height / self.x, self.width / self.y
        # Font size for texts
        self.font_size = self.scy/5

    def add_comment(self, file, comment):
        """Function to add comment inside SVG file wall."""
        print(f'<!--{comment}-->',file=file)
        return None

    def add_grid(self, file, x, y, fill='"none"', stroke='"gray"', stroke_w='"1"'):
        x_val = int(x*self.scx)
        y_val = int(y*self.scy)
        print(f'<rect x="{x_val}" y="{y_val}" width="{self.scx:.0f}" height="{self.scy:.0f}" fill={fill} stroke={stroke} stroke-width={stroke_w}/>', file = file)
        return None

    def add_coords(self, file, x, y, tx, ty):
        """Write a state coordinate to the SVG image file handle f."""
        state_number = tx+(ty*self.x)
        print(f'<text x="{x}" y="{y}" class="small">S{state_number}</text>', file=file)
        return None

    def add_wall(self, file, x1, y1, x2, y2):
        """Function to draw wall."""
        print(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"/>', file=file)
        return None
    
    def add_arrow(self, file, x1, y1, x2, y2):
        """Function to draw arrow."""
        print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="4" marker-end="url(#arrow)" />', file=file)
        return None

    def add_val(self, file, x, y, val):
        """Write a value to a coordinate in the SVG image file handle f."""
        print(f'<text x="{x}" y="{y}" class="qVal">{val:.12f}</text>', file=file)
        return None

    def draw_grid(self, file, path=None, goal_st=None):
        self.add_comment(file, 'Add Grid Layout')
        for x in range(self.x):
            for y in range(self.y):
                if (path != None):
                    if(y*self.x + x == path[0][0]):
                        self.add_grid(file, x, y, fill='"yellow"')
                    elif(y*self.x + x == path[-1][-1]):
                        self.add_grid(file, x, y, fill='"green"')
                    else:
                        self.add_grid(file, x, y)
                elif (goal_st != None):
                    if(y*self.x + x == goal_st):
                        self.add_grid(file, x, y, fill='"green"')
                    else:
                        self.add_grid(file, x, y)
                else:
                    self.add_grid(file, x, y)
        print('',file=file)
        return None

    def draw_coordinate(self, file):
        self.add_comment(file, 'Add Coordinates')
        for x in range(self.x):
            for y in range(self.y):
                wx, wy = int((x+0.1)*self.scx), int((y+0.3)*self.scy)
                self.add_coords(file, wx, wy, x, y)
        print('',file=file)
        return None

    def draw_walls(self, file):
        self.add_comment(file, 'Add Walls')
        for x in range(self.x):
            for y in range(self.y):
                st = int(x+(y*self.x))
                if self.ns[st][0]==st:
                    x1, y1, x2, y2 = x*self.scx, (y+1)*self.scy, (x+1)*self.scx, (y+1)*self.scy
                    self.add_wall(file, x1, y1, x2, y2)

                if self.ns[st][1]==st:
                    x1, y1, x2, y2 = (x+1)*self.scx, y*self.scy, (x+1)*self.scx, (y+1)*self.scy
                    self.add_wall(file, x1, y1, x2, y2)
        print('',file=file)
        return None
    
    def draw_path(self, file, path):
        self.add_comment(file, 'Add path made of arrows')
        arrow_length = 0.7
        offset = 0.5
        for set in path:
            st, at, st1 = set
            x, y = st%self.x, st//self.y 

            if (at == 0):
                start = 0.1
                x1 = (x+0.5)*self.scx
                y1 = (y+start+offset)*self.scy
                x2 = x1
                y2 = y1+(arrow_length*self.scy)
            elif (at == 1):
                start = 0.1
                x1 = (x+start+offset)*self.scx
                y1 = (y+0.5)*self.scy
                x2 = x1+(arrow_length*self.scx)
                y2 = y1
            elif (at == 2):
                start = 0.2
                y1 = (y+0.5)*self.scy
                y2 = y1
                x2 = (x+start-offset)*self.scx
                x1 = x2+(arrow_length*self.scx)
            else:
                start = 0.2
                x1 = (x+0.5)*self.scx
                x2 = x1
                y2 = (y+start-offset)*self.scy
                y1 = y2+(arrow_length*self.scy)
            
            self.add_arrow(file, int(x1), int(y1), int(x2), int(y2))
        print('',file=file)
        return None

    def draw_convergence(self, file, matrix, goal):
        self.add_comment(file, 'Add action arrows and Q-Values')
        arrow_length = 0.1
        offset = 0.2
        for st in range(len(matrix)):
            maxQ, at = matrix[st]
            x, y = st%self.x, st//self.y 
            if (st != goal):
                if (at == 0): # Arrow Down
                    start = 0.1
                    x1 = (x+0.5)*self.scx
                    y1 = (y+start+offset)*self.scy
                    x2 = x1
                    y2 = y1+(arrow_length*self.scy)
                elif (at == 1): # Arrow Right
                    start = 0.1
                    x1 = (x+start+offset)*self.scx
                    y1 = (y+0.5)*self.scy
                    x2 = x1+(arrow_length*self.scx)
                    y2 = y1
                elif (at == 2): # Arrow Left
                    start = 0.8
                    y1 = (y+0.5)*self.scy
                    y2 = y1
                    x2 = (x+start-offset)*self.scx
                    x1 = x2+(arrow_length*self.scx)
                else: # Arrow Up
                    start = 0.9
                    x1 = (x+0.5)*self.scx
                    x2 = x1
                    y2 = (y+start-offset)*self.scy
                    y1 = y2+(arrow_length*self.scy)
                self.add_arrow(file, x1, y1, x2, y2)
                
                # Write Q-Value
                wx, wy = int((x+0.1)*self.scx), int((y+0.9)*self.scy)
                self.add_val(file, wx, wy, maxQ)
        print('',file=file)
        return None

    def gen_svg(self, filename, path=None, goal_st=None):
        """Write an SVG file of a grid-maze."""
        with open(filename, 'w') as f:
            # SVG preamble and styleself.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(self.width+2*self.padding, self.height+2*self.padding,
                            -self.padding, -self.padding, self.width+2*self.padding, self.height+2*self.padding),
                    file=f)
            print('<defs>', file=f)
            print('<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 4;\n}', file=f)
            print(']]>', file=f)
            print('.small {{ font: bold {}px sans-serif;'.format(self.font_size), file=f)
            print('         fill: lightgray; }}', file=f)
            print('</style>', file=f)
            if (path != None): # preamble for arrow marker
                markerWidth = self.scale/10
                markerHeight = markerWidth/2
                print(f'<marker id="arrow" markerWidth="{markerWidth}" markerHeight="{markerHeight}" refX="0" refY="1" orient="auto">', file=f)
                print('\t<polygon points="0 0, 2 1, 0 2" />', file=f)
                print('</marker>', file=f)
            print('</defs>', file=f)

            # Draw initial grid square
            self.draw_grid(f, path=path, goal_st=goal_st)

            # Draw state coordinates
            self.draw_coordinate(f)

            # Draw the South and East walls of each cell
            self.draw_walls(f)

            # Draw the Path
            if (path != None):
                self.draw_path(f, path)

            # Draw the North and West maze border, which won't have been drawn by the procedure above.
            self.add_comment(f, 'Add the north and west maze border')
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(self.width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(self.height), file=f)
            print('</svg>', file=f)
        return None

    def gen_convergenceMap(self, filename, maxMatrix, goal):
        """Write an SVG file of a grid-maze."""
        with open(filename, 'w') as f:
            # SVG preamble and styleself.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(self.width+2*self.padding, self.height+2*self.padding,
                            -self.padding, -self.padding, self.width+2*self.padding, self.height+2*self.padding),
                    file=f)
            print('<defs>', file=f)
            
            print('<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 4;\n}', file=f)
            print(']]>', file=f)
            print('.small {{ font: bold {}px sans-serif;'.format(self.font_size), file=f)
            print('         fill: lightgray; }}', file=f)
            print('</style>', file=f)
            
            print('<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 4;\n}', file=f)
            print(']]>', file=f)
            print('.qVal {{ font: {}px monospace;'.format(self.font_size/2), file=f)
            print('         fill: black; }}', file=f)
            print('</style>', file=f)

            # preamble for arrow marker
            markerWidth = self.scale/10
            markerHeight = markerWidth/2
            size = self.scale/100
            print(f'<marker id="arrow" markerWidth="{markerWidth}" markerHeight="{markerHeight}" refX="0" refY="{size}" orient="auto">', file=f)
            print(f'\t<polygon points="0 0, {size*2} {size}, 0 {size*2}" />', file=f)
            print('</marker>', file=f)
            print('</defs>', file=f)

            # Draw initial grid square
            self.draw_grid(f, goal_st=goal)

            # Draw state coordinates
            self.draw_coordinate(f)

            # Draw the South and East walls of each cell
            self.draw_walls(f)

            # Draw the Path
            self.draw_convergence(f, maxMatrix, goal)

            # Draw the North and West maze border, which won't have been drawn by the procedure above.
            self.add_comment(f, 'Add the north and west maze border')
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(self.width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(self.height), file=f)
            print('</svg>', file=f)
        return None