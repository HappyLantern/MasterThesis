import rasterio

with rasterio.open('./Washan/files/tifstuff/tiffile1.tif') as dst:
    # Width and height of the picture
    print(dst.width)
    print(dst.height)
    # The number of bands in the tif.file
    print(dst.count)
    # The bounds of the image, related to the width and height
    print(dst.bounds)
    # The affine transformation of the image. Maps the pixel locations in (row, col) to (x, y) spatial locations.
    # The transformation matrix of this file is not clear. Seems like its meant to do nothing.
    print(dst.transform)
    # The coordinate reference system CRS of the image. (None) -> Relates to the transform I guess.
    # EPSG-X identifies a particular CRS. This system is used for mapping areas in some specific part of the hemisphere.
    print(dst.crs)

    print(dst.indexes)
    
    # The bands count from 1,...,x
    # The .read() method returns a Numpy N-D array
    band1 = dst.read(1)
    print(band1)

    print(band1[dst.height // 2, dst.width // 2])

    {i: dtype for i, dtype in zip(dst.indexes, dst.dtypes)} # Get the dtype for each band
    print(dst.dtypes) # 1 band, uint16

    # The index() method gives the array indices corresponding to points in the georeferenced space. 
    # In this case, the image has already been normalized, so the values are the same. 
    # Know the distance from the resolution I guess.
    x, y = (dst.bounds.left + 10000, dst.bounds.top + 10000)
    row, col = dst.index(x, y) 
    print(row, col)
    print(band1[row, col])
    print(dst.xy(dst.height // 2, dst.width // 2))
    


