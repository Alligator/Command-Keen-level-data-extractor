# Commander Keen Level Data Extractor

Python script to extract tile data and sprites from Commander Keen 1-3 levels, using information from [here](http://www.shikadi.net/moddingwiki/Commander_Keen_1-3_Level_format) and [here](http://www.shikadi.net/moddingwiki/RLEW_compression).

## Standalone
The script can be used standalone like this:
    python keen.py file
This returns two files, one named `data` and one named `sprites` containg the tile IDs and sprite IDs as python list structures.

## Module
The script can also be used as a module, like so:
 ha   import keen
The module has two methods.
    decompress(file)
Expects a filename as a string.
Returns a string representing the entire decompressed file.

   convert(data) 
Excepts data to be a string.
Returns a tuple containg the lists of tiles a sprites.

### Example
To retrieve all the data from the file "LEVEL1".
    tiles, sprites = convert(decompress("LEVEL1"))
