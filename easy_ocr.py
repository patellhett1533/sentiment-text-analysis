import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('dummy-bill.png')

for (bbox, text, prob) in result:
    print("[INFO] {:.2f} : {}".format(prob, text))
