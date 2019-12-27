# USAGE
# python download_images.py --urls urls_atvs.txt --output images/santa

# import the necessary packages
from imutils import paths
import argparse
import requests
import cv2
import os
from bs4 import BeautifulSoup
import requests

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=False, default=None,
	help="path to output directory of images")
ap.add_argument("--prefix", required=False, default="", help="Prefix to add to images")

args = vars(ap.parse_args())
prefix = args['prefix']

total = 0
rows = []
for i in range(1,4):
	response = requests.get("https://pixabay.com/images/search/dirtbike/", {"pagi": i})
	soup = BeautifulSoup(response.text, 'lxml')
	for img_element in soup.find_all('img'):
		rows.append(img_element.attrs['src'])

# loop the URLs
for url in rows:
	try:
		# try to download the image
		print(url)
		r = requests.get(url, timeout=60)

		# save the image to disk
		p = os.path.sep.join([args["output"], f"{prefix}{str(total).zfill(8)}.jpg"])
		f = open(p, "wb")
		f.write(r.content)
		f.close()

		# update the counter
		print("[INFO] downloaded: {}".format(p))
		total += 1

	# handle if any exceptions are thrown during the download process
	except:
		print("[INFO] error downloading {}...skipping".format(p))

# loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete = False

	# try to load the image
	try:
		image = cv2.imread(imagePath)

		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			print("None")
			delete = True

	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True

	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)