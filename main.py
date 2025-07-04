from src.scraper import Scraper
import requests

scraper = Scraper("Delhi")

images = scraper.get_images()
for image in images:
    scraper.download_image(image)



# https://bhoonidhi.nrsc.gov.in/imgarchive/PRODUCTJPGS//R2A/LIS3/2025/JUN/13//RA313JUN2025044189009600051PSANSTUC00GTDF.jpg
# url = "https://bhoonidhi.nrsc.gov.in/imgarchive/PRODUCTJPGS//R2A/LIS3/2025/JUN/13//RA313JUN2025044189009600051PSANSTUC00GTDF.jpg"
# response = requests.get(url, stream=True)
# with open("test.jpg", "wb") as file:
#     for chunk in response.iter_content(chunk_size=8192):
#         file.write(chunk)
# print("Image downloaded successfully.")
