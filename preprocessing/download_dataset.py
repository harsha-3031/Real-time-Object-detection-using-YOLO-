
from roboflow import Roboflow
rf = Roboflow(api_key="HrugIbTHK87KYdfBrQVr")
project = rf.workspace("sky-zfxvm").project("coco-yrx1j")
version = project.version(1)
dataset = version.download("yolov8")
