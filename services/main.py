import csv
import argparse
from cloud.cloudinary_client import CloudinaryImaging

def csv_parse(file_path):
    name_type = set()
    with open(file_path, newline='', encoding="UTF-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for path, name, _type in spamreader:
            print(name, _type)
            name_type.add("asd")
            if not imaging.upload_img(name, _type, path):
                print(f"error uploafing image: {name} {_type} {path}")
            else:
                name_type.add((name, _type))
    return name_type

def main(args):
    for name, _type in csv_parse(args):
        print(*((name, _type, url) for url in imaging.get_img_urls(name)), sep="\n")

if __name__ == "Main":
    main("asd")