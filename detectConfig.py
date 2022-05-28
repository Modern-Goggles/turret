
# config for detection



# configuration for neural network

# path to config file
NETWORK_CONFIG_PATH = "ssdMobilenet/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

# path to weights file
NETWORK_WEIGHTS_PATH = "ssdMobilenet/frozen_inference_graph.pb"

# path to labls file
LABELS_FILE = "ssdMobilenet/coco.names"

# extract coco class names
COCO_CLASS_NAMES= []
with open(LABELS_FILE,"rt") as f:
    COCO_CLASS_NAMES = f.read().rstrip("\n").split("\n")
