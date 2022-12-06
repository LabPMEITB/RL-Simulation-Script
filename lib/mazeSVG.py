"""
PROGRAMMER  : ANDI MUHAMMAD RIYADHUS ILMY
CREATE DATE : 2022/08/09 15:00
DESCRIPTION : TBD
"""

class drawMaze:
    def __init__(self, mx, my, scale, ns):
        self.x = mx
        self.y = my
        self.scale = scale
        self.ns = ns
        # self.path = path

    def add_commentLine(self, comment, SVG_file):
        """Function to add comment inside SVG file wall."""
        print(f'<!--{comment}-->',file=SVG_file)
        return None

    # def add_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
    #     """Function to draw wall."""
    #     print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

    # def add_coords(wc_f, maze_x, wc_x, wc_y, wc_tx, wc_ty):
    #     """Write a state coordinate to the SVG image file handle f."""
    #     state_number = wc_tx+(wc_ty*maze_x)
    #     print('<text x="{}" y="{}" class="small">S{}</text>'.format(wc_x, wc_y, state_number), file=wc_f)

    # def add_arrow(wc_f, x1, y1, x2, y2):
    #     """Function to draw arrow """
    #     print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="4" marker-end="url(#arrow)" />', file=wc_f)

    def gen_maze(self, filename):
        """Create a grid-maze in SVG format using next state list."""

        # Set the maze aspect ratio
        aspect_ratio = self.x / self.y
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = self.scale
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.x, width / self.y
        # Font size for texts
        font_size = scy/5

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width + 2 * padding, height + 2 * padding,
                            -padding, -padding, width + 2 * padding, height + 2 * padding),
                    file=f)
            print('<defs>', file=f)
            print('<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 4;\n}', file=f)
            print(']]>', file=f)
            print('.small {{ font: bold {}px sans-serif;'.format(font_size), file=f)
            print('         fill: lightgray; }}', file=f)
            print('</style>', file=f)
            # Add arrow
            print('<marker id="arrow" markerWidth="10" markerHeight="7" refX="0" refY="2" orient="auto">', file=f)
            print('\t<polygon points="0 0, 4 2, 0 4" />', file=f)
            print('</marker>', file=f)
            print('</defs>', file=f)

            # Draw layout square
            add_commentLine('Add Grid Layout', f)
            # print('Add initial layout square')
            # for x in range(maze_x):
            #     for y in range(maze_y):
            #         print(f'<rect x="{x*scx}" y="{y*scy}" width="{scx}" height="{scy}" fill="none" stroke="gray" stroke-width="1"/>', file = f)
            # print('',file=f)

            # # Draw State Coordinates
            # for x in range(maze_x):
            #     for y in range(maze_y):
            #         wx, wy = (x+0.1)*scx, (y+0.3)*scy
            #         write_coords(f, maze_x, wx, wy, x, y)
            # print('',file=f)

            # # Draw the "South" and "East" walls of each cell, if present (these
            # # are the "North" and "West" walls of a neighbouring cell in
            # # general, of course).
            # for x in range(maze_x):
            #     for y in range(maze_y):
            #         st = x+(y*maze_x)
            #         if ns_list[st][0]==st:
            #             x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
            #             write_wall(f, x1, y1, x2, y2)

            #         if ns_list[st][1]==st:
            #             x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
            #             write_wall(f, x1, y1, x2, y2)
            # print('',file=f)

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)
    
    def draw_path(self, filename):
        # print(filename)
        # """Write an SVG image of the maze to filename."""

        aspect_ratio = self.x / self.y
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = self.scale
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.y, width / self.x
        # Font size for texts
        font_size = scy/5

        # def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
        #     """Write a single wall to the SVG image file handle f."""

        #     print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        # def write_coords(wc_f, wc_x, wc_y, wc_tx, wc_ty):
        #     """Write a state coordinate to the SVG image file handle f."""
        #     state_number = wc_tx+(wc_ty*self.x)
        #     print('<text x="{}" y="{}" class="small">S{}</text>'.format(wc_x, wc_y, state_number), file=wc_f)

        # def draw_arrow(wc_f, x1, y1, x2, y2):
        #     """Write arrow dircetion based on the given action on the state coordinate to the SVG image file handle f."""
        #     print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="4" marker-end="url(#arrow)" />', file=wc_f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width + 2 * padding, height + 2 * padding,
                            -padding, -padding, width + 2 * padding, height + 2 * padding),
                    file=f)
            print('<defs>', file=f)
            print('<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 4;\n}', file=f)
            print(']]>', file=f)
            print('.small {{ font: bold {}px sans-serif;'.format(font_size), file=f)
            print('         fill: lightgray; }}', file=f)
            print('</style>', file=f)
            # Add arrow
            print('<marker id="arrow" markerWidth="10" markerHeight="7" refX="0" refY="2" orient="auto">', file=f)
            print('\t<polygon points="0 0, 4 2, 0 4" />', file=f)
            print('</marker>', file=f)
            print('</defs>', file=f)

            # Draw layout square
            for x in range(self.x):
                for y in range(self.y):
                    if(y*self.x + x == self.path[0][0]):
                        print(f'<rect x="{x*scx}" y="{y*scy}" width="{scx}" height="{scy}" fill="yellow" stroke="gray" stroke-width="1"/>', file = f)
                    elif(y*self.x + x == self.path[-1][-1]):
                        print(f'<rect x="{x*scx}" y="{y*scy}" width="{scx}" height="{scy}" fill="green" stroke="gray" stroke-width="1"/>', file = f)
                    else:
                        print(f'<rect x="{x*scx}" y="{y*scy}" width="{scx}" height="{scy}" fill="none" stroke="gray" stroke-width="1"/>', file = f)
            print('',file=f)

            # Draw State Coordinates
            for x in range(self.x):
                for y in range(self.y):
                    wx, wy = (x+0.1)*scx, (y+0.3)*scy
                    write_coords(f, wx, wy, x, y)
            print('',file=f)

            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.x):
                for y in range(self.y):
                    st = x+(y*self.x)
                    if self.ns[st][0]==st:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

                    if self.ns[st][1]==st:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            print('',file=f)

            # Draw the Path
            arrow_length = 0.7
            offset = 0.5
            for set in self.path:
                st, at, st1 = set
                x, y = st%self.x, st//self.y 

                if (at == 0):
                    start = 0.1
                    x1 = (x+0.5)*scx
                    y1 = (y+start+offset)*scy
                    x2 = x1
                    y2 = y1+(arrow_length*scy)
                elif (at == 1):
                    start = 0.1
                    x1 = (x+start+offset)*scx
                    y1 = (y+0.5)*scy
                    x2 = x1+(arrow_length*scx)
                    y2 = y1
                elif (at == 2):
                    start = 0.2
                    y1 = (y+0.5)*scy
                    y2 = y1
                    x2 = (x+start-offset)*scx
                    x1 = x2+(arrow_length*scx)
                else:
                    start = 0.2
                    x1 = (x+0.5)*scx
                    x2 = x1
                    y2 = (y+start-offset)*scy
                    y1 = y2+(arrow_length*scy)
                
                draw_arrow(f, x1, y1, x2, y2)
            print('',file=f)

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)