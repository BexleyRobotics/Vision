import sys
import freenect

ctx = freenect.init()
dev = freenect.open_device(ctx, 0)
freenect.set_tilt_degs(dev, float(sys.argv[1]))
