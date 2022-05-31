from screeninfo import get_monitors as gm
si = gm()
print(si[0].x, si[0].y, si[0].height, si[0].width)