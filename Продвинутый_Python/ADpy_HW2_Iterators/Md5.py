import hashlib

file_to_read = [print(hashlib.md5(line.encode('utf-8')).hexdigest()) for line in open('C:\\_fforhw\\md5_hash\\new_doc.txt', 'r')]

