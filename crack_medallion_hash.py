import csv
import re
import hashlib

LLLDDD_FORMAT = re.compile(r'[A-Z]{3}\d{3}')

def read_target_digests():
  with open('medallion_hashes.txt', encoding='utf-8') as infile:
    return [h.strip() for h in list(infile)]

def medallion_matches_format(medallion, pattern):
  return pattern.match(medallion)

def medallions():
  with open('medallions.csv', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter=',', quotechar='"')
    fieldnames = next(reader)
    for line in reader:
      data = dict(zip(fieldnames, line))
      medallion = data["License Number"]
      if medallion_matches_format(medallion, LLLDDD_FORMAT):
        yield data

def hash_medallion(medallion):
  return hashlib.sha256(bytes(medallion, 'utf-8')).hexdigest()

def main():
  targets = frozenset(read_target_digests())
  match_count = 0
  for line in medallions():
    digest = hash_medallion(line["License Number"])
    if digest in targets:
      match_count += 1
      print('%2d/%2d matched `%s` to medallion `%s` owned by %s' % (
        match_count,
        len(targets),
        digest,
        line["License Number"],
        line["Name of Licensee"]
      ))

if __name__ == '__main__':
  main()