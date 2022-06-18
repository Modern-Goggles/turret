### basic configuration
##############################

# the absolute path to this repository
# this gets populated automatically by install.sh
REPO_DIR = ''

### configuratation for sounds
##############################

# what directory are sounds in
SOUNDS_DIR = f"{REPO_DIR}/sounds"


### configuration for detection
###############################

# path to network config file
NETWORK_CONFIG_PATH = f"{REPO_DIR}/ssdMobilenetV3/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

# path to weights file
NETWORK_WEIGHTS_PATH = f"{REPO_DIR}/ssdMobilenetV3/frozen_inference_graph.pb"

# path to labels file
LABELS_FILE = f"{REPO_DIR}/ssdMobilenetV3/coco.names"

# extract coco class names
COCO_CLASS_NAMES= []
with open(LABELS_FILE,"rt") as f:
    COCO_CLASS_NAMES = f.read().rstrip("\n").split("\n")
