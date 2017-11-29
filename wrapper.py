from ebayCall import ebay
from amazon import amazon
from imports import importData

def main():
    ebay("n64list")
    amazon("n64list")
    importData("EbayTest","ebay.json")
    importData("AmazonTest","amazon_results.json")


if __name__ = "__main__":
    main()
