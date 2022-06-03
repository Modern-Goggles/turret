### configuration for detection

# path to config file
NETWORK_CONFIG_PATH = "ssdMobilenetV3/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

# path to weights file
NETWORK_WEIGHTS_PATH = "ssdMobilenetV3/frozen_inference_graph.pb"

# path to labls file
LABELS_FILE = "ssdMobilenetV3/coco.names"

# extract coco class names
COCO_CLASS_NAMES= []
with open(LABELS_FILE,"rt") as f:
    COCO_CLASS_NAMES = f.read().rstrip("\n").split("\n")
