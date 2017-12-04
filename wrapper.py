from ebayCall import ebay
from amazon import amazon
from importer import importData

def main():
    ebay("n64ListAll")
    amazon("n64ListAll")
    importData("Ebay","ebay.json")
    importData("Amazon","amazon_results.json")


if __name__ == "__main__":
    main()
