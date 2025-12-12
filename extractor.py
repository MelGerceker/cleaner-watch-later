from zipfile import ZipFile

zip_path = './personalData/takeout-20230609T125121Z-001.zip'

with ZipFile(zip_path, 'r') as zip:
    zip.extractall()
    
print("Extracted zip file successfully.")

# takeout1234.zip -> Takeout -> Youtube and YouTube Music -> history -> watch-history.html
# delete search history.html also in the same folder?

#TODO: Create drop box for zip