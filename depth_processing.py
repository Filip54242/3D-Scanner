import numpy as np
import cv2
import skimage.exposure


def pretty_depth(depth):
    
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2

    stretch = skimage.exposure.rescale_intensity(depth, in_range='image', out_range=(0,255)).astype(np.uint8)

    # convert to 3 channels
    stretch = cv2.merge([stretch,stretch,stretch])

    # define colors
    color1 = (0, 0, 255)     #red
    color2 = (0, 165, 255)   #orange
    color3 = (0, 255, 255)   #yellow
    color4 = (255, 255, 0)   #cyan
    color5 = (255, 0, 0)     #blue
    color6 = (128, 64, 64)   #violet
    colorArr = np.array([[color1, color2, color3, color4, color5, color6]], dtype=np.uint8)

    # resize lut to 256 (or more) values
    lut = cv2.resize(colorArr, (256,1), interpolation = cv2.INTER_LINEAR)

    # apply lut
    result = cv2.LUT(stretch, lut)
    return result


def depth2xyzuv(depth, u=None, v=None):
    depth=np.asarray(depth)
    if u is None or v is None:
        u,v = np.mgrid[:480,:640]
  
    C = np.vstack((u.flatten(), v.flatten(), depth.flatten(), 0*u.flatten()+1))

    X,Y,Z,W = np.dot(xyz_matrix(),C)
    X,Y,Z = X/W, Y/W, Z/W
    xyz = np.vstack((X,Y,Z)).transpose()
    xyz = xyz[Z<0,:]

    U,V,_,W = np.dot(np.dot(uv_matrix(), xyz_matrix()),C)
    U,V = U/W, V/W
    uv = np.vstack((U,V)).transpose()    
    uv = uv[Z<0,:]       

    return xyz, uv



def uv_matrix():

    rot = np.array([[ 9.99846e-01,   -1.26353e-03,   1.74872e-02], 
                  [-1.4779096e-03, -9.999238e-01,  1.225138e-02],
                  [1.747042e-02,   -1.227534e-02,  -9.99772e-01]])
    trans = np.array([[1.9985e-02, -7.44237e-04,-1.0916736e-02]])
    m = np.hstack((rot, -trans.transpose()))
    m = np.vstack((m, np.array([[0,0,0,1]])))
    KK = np.array([[529.2, 0, 329, 0],
                 [0, 525.6, 267.5, 0],
                 [0, 0, 0, 1],
                 [0, 0, 1, 0]])
    m = np.dot(KK, (m))
    return m

def xyz_matrix():
    fx = 594.21
    fy = 591.04
    a = -0.0030711
    b = 3.3309495
    cx = 339.5
    cy = 242.7
    mat = np.array([[1/fx, 0, 0, -cx/fx],
                  [0, -1/fy, 0, cy/fy],
                  [0,   0, 0,    -1],
                  [0,   0, a,     b]])
    return mat