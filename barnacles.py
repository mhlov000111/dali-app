import cv2
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage.filters import gaussian

# Image Loading
def load_image_gray(path):
    img_color = cv2.imread(path)
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    return gray

def load_image_bw(path, thresh=50): # manual threshold calculation
    gray = load_image_gray(path)
    _, bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return bw

def load_image_bw_otsu(path): # automatic threshold calculation
    gray = load_image_gray(path)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return bw


# Region counting
def find_peaks(img, sigma, min_dist):
    smooth = gaussian(img, sigma=sigma, preserve_range=True)

    coords = peak_local_max(smooth, min_distance=min_dist, threshold_abs=smooth.mean())

    print(f"Detected {len(coords)} regions")

    # display image / regions    
    plt.imshow(img, cmap='gray')
    plt.scatter(coords[:, 1], coords[:, 0], c='red', s=5)
    plt.show()

    return len(coords)


# Eval
def connected_components(mask):
    mask_bw = load_image_bw(mask)
    y, _ = cv2.connectedComponents(mask_bw)
    return y
