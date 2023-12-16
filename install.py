import subprocess
import os
import urllib.request
from urllib.request import urlretrieve


dependencies = [
    "numpy",
    "opencv-python-headless",
    "imageio",
    "Pillow",
    "encoded_video",
    
]

def install_dependencies():
    for package in dependencies:
        try:
            subprocess.check_call(["pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            
    try:
        subprocess.check_call(["pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"])
    except subprocess.CalledProcessError:
        print("Failed to install torch, torchvision, torchaudio")

#model_url = "https://github.com/Sxela/ArcaneGAN/releases/download/v0.4/ArcaneGANv0.4.jit"
# Prepare the wget command
#wget_command = f"urllib.request.urlretrieve({model_url})"

# Execute the wget command
#os.system(wget_command)

if __name__ == "__main__":
    install_dependencies()
    urllib.request.urlretrieve("https://github.com/Sxela/ArcaneGAN/releases/download/v0.4/ArcaneGANv0.4.jit")
    