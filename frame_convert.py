import cv
import numpy as np
import Image

lower = 500; upper = 1000

def robustavg(array):
   
    if len(array.shape) == 4: # that is, rgb array
      return array.mean(0)
     
    elif len(array.shape) == 3: # depth array
      weights = ((array > lower ) & (array < upper)).astype(float) + 1e-10
      print weights.shape
      return (array*weights).sum(0) / weights.sum(0)
    else:
      print 'robustavg: invalid array'


def meter_depth(depth):
    meter =  1.0 / (depth * -0.0030711016 + 3.3309495161);
    return meter

def pretty_depth(depth):
    """Converts depth into a 'nicer' format for display

    This is abstracted to allow for experimentation with normalization

    Args:
        depth: A numpy array with 2 bytes per pixel

    Returns:
        A numpy array that has been processed whos datatype is unspecified
    """

    min = 300
    max = 1500
    np.clip(depth, min, max, depth)
   
    depth -= min
    depth *= 256./(max-min)
    depth = depth.astype(np.uint8)
    return depth

def depth_cv(depth):
    """Converts depth into a 'nicer' format for display

    This is abstracted to allow for experimentation with normalization

    Args:
        depth: A numpy array with 2 bytes per pixel

    Returns:
        An opencv image who's datatype is unspecified
    """
    depth = pretty_depth(depth)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    return image


def video_cv(video):
    """Converts video into a BGR format for opencv

    This is abstracted out to allow for experimentation

    Args:
        video: A numpy array with 1 byte per pixel, 3 channels RGB

    Returns:
        An opencv image who's datatype is 1 byte, 3 channel BGR
    """
    video = video[:, :, ::-1]  # RGB -> BGR
    image = cv.CreateImageHeader((video.shape[1], video.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 3)
    cv.SetData(image, video.tostring(),
               video.dtype.itemsize * 3 * video.shape[1])
    return image

def pretty_depth_cv(depth):
    """Converts depth into a 'nicer' format for display

    This is abstracted to allow for experimentation with normalization

    Args:
        depth: A numpy array with 2 bytes per pixel

    Returns:
        An opencv image who's datatype is unspecified
    """
    import cv
    depth = pretty_depth(depth)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    return image

def video_cv(video):
    """Converts video into a BGR format for opencv

    This is abstracted out to allow for experimentation

    Args:
        video: A numpy array with 1 byte per pixel, 3 channels RGB

    Returns:
        An opencv image who's datatype is 1 byte, 3 channel BGR
    """
    import cv
    video = video[:, :, ::-1]  # RGB -> BGR
    image = cv.CreateImageHeader((video.shape[1], video.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 3)
    cv.SetData(image, video.tostring(),
               video.dtype.itemsize * 3 * video.shape[1])
    return image

