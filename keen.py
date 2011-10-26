import sys
import struct
import Image, ImageDraw

def decompress(fi):
    f = open(fi, 'rb')
    # first dword is uncompressed size
    lb = f.read(4)
    length = struct.unpack('i', lb)[0]
    pos = 0
    out = lb
    while pos <= length:
        sys.stdout.write('\r%d / %d' % (pos, length))
        # get a word
        word = f.read(2)
        pos += 2
        # Is this word $FEFE?
        if word == '\xFE\xFE':
            # If yes;
            # Get the next two words (Word1 and Word2)
            w1 = struct.unpack('h', f.read(2))[0]
            w2 = f.read(2)
            pos += 4
            # Copy Word2 [Word1] times
            for i in range(w1):
                out += w2
            # Move forward three words and got to 2.)
        else:
            # If no;
            # Copy the word
            out += word
            # Move forward a word and go to 2.)
    f.close()
    return out

def convert(data):
    # pos  len   what
    # 0    4     data size
    # 4    2     height in tiles
    # 6    2     width in tiles
    # 8    2     num of planes (2)
    # 18   2     planesize. 2 (h * w) rounded to multiples of 16
    # each plan is 2 * planesize, read top left to bottom right
    # tiles first, sprites second

    # get some metadata
    width = struct.unpack('h', data[4:6])[0]
    height  = struct.unpack('h', data[6:8])[0]
    psize  = struct.unpack('h', data[18:20])[0]

    print
    print psize

    # get them tiles
    tiles = []
    data = data[36:]
    offset = 0

    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)

    f = open ('data', 'w')

    for h in range(height):
        inner = []
        for w in range(width):
            tile = struct.unpack('h', data[offset:offset+2])[0]
            offset += 2
            inner.append(tile)
            draw.point((w, h), fill=(tile,tile,tile))
        f.write(str(inner) + '\n')
        tiles.append(inner)
    f.close()

    f = open ('sprites', 'w')

    sprites = []
    for h in range(height):
        inner = []
        for w in range(width):
            tile = struct.unpack('h', data[offset:offset+2])[0]
            offset += 2
            inner.append(tile)
            if tile:
                draw.point((w, h), fill=(255,tile,0))
        f.write(str(inner) + '\n')
        sprites.append(inner)

    f.close()
    im.save('keen.png')
    return tiles, sprites

if __name__ == '__main__':
    data = decompress(sys.argv[1])
    c = convert(data)
