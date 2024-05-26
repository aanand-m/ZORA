import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
import os

# def totalPages(productUrl):
#     resp = requests.get(
#   url='https://proxy.scrapeops.io/v1/',
#   params={
#       'api_key': '1d9ac50c-530a-487d-ac01-835ae38773f8',
#       'url': {productUrl}, 
#   },
# )

def scrape (reviewUrl, pages, fileName):
    cust_names = []
    rev_date = []
    ratings = []
    rev_title = []
    rev_content = []
    for page in range(1,pages):
        url1 = reviewUrl+str(page)
        code = code = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
      'api_key': '1d9ac50c-530a-487d-ac01-835ae38773f8',
      'url': {url1},
        },
        )
        if str(code) == "<Response [200]>":
            soup = BeautifulSoup(code.content,'html.parser')

            names = soup.select('span.a-profile-name')[2:]
            c_names = []
            [c_names.append(x) for x in names if x not in c_names]

            titles = soup.select('a.review-title span')
            title = [span for span in titles if not span.has_attr('class')]

            dates = soup.select('span.review-date')[2:]

            stars = soup.select('i.review-rating span.a-icon-alt')[2:]

            reviews = soup.select('span.review-text-content span')

            for i in range(len(c_names)):
                cust_names.append(c_names[i].get_text())
                rev_date.append(dates[i].get_text())
                ratings.append(stars[i].get_text().replace(' out of 5 stars',''))
                rev_title.append(title[i].get_text())
                rev_content.append(reviews[i].get_text().strip("\n "))
    
    df = pd.DataFrame()
    headers = ['Customer Name','Date','Ratings','Review Title','Reviews']
    df['Customer Name'] = cust_names
    df['Date'] = rev_date
    df['Ratings'] = ratings
    df['Review Title'] = rev_title
    df['Reviews'] = rev_content
    if not df.columns.tolist() == headers:  # Check if headers already set
        df.columns = headers
    path = os.getcwd() +f"/datasets/{fileName}"
    df.to_csv(path,index=False)
    # with open(fileName,'r'):
    #     pass
    print("file saved")


# function for dumping dataset on aws-s3 bucket.
def dump(access_key, secret_key,fileName):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)  # Create S3 client
    bucket_name = "sentiment-data-bucket" # name of s3 bucket where the data will be stored.
    file_name = fileName
    file_path = os.getcwd() +f"/datasets/{fileName}"  # Local file path
    s3.upload_file(file_path, bucket_name, file_name) # upload
    print(f"File {file_name} uploaded successfully to {bucket_name}")


    
def main(reviewUrl,pages,fileName):
    # # asin = input("Enter ASIN for the product you wish to scrape: ")
    # # productUrl = "https://www.amazon.in/dp/{asin}/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B0CB7VH5Y3&pd_rd_w=KRPlP&content-id=amzn1.sym.dcd65529-2e56-4c74-bf19-15db07b4a1fc&pf_rd_p=dcd65529-2e56-4c74-bf19-15db07b4a1fc&pf_rd_r=EHDAY5HWV6875RKEG8ZY&pd_rd_wg=yJkPZ&pd_rd_r=f6252e9c-34c8-4498-ac91-dbe4d789118b&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM"
    reviewUrl = reviewUrl + "&pageNumber="
    pages = int (pages)
    # # print("There are total ", totalPages(productUrl) ," pages of reviews for this product." )
    # pages = int(input("How many pages do you wish to scrape ? NOTE:- one page contains 10 reviews: ")) + 1

    # fileName=input("Enter the name for your dataset: ")
    access_key = "AKIA3YHIEH3CFQUZSW5Q"
    secret_key = "Rwj1XRFGxZSMlVkzptDzRm+XnGy/T50hy1yiTZWh"
    scrape(reviewUrl,pages,fileName)

    dump(access_key, secret_key, fileName)
