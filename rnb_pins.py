#!/usr/bin/env python3

import csv
from collections import OrderedDict

def load_pins():
  with open('rnb_pins.csv', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter=',', quotechar='"')
    fieldnames = next(reader)
    for line in reader:
      yield dict(zip(fieldnames, line))

def main():
  pin_data = list(load_pins())

  scrooge_pin = None
  encryped_pins = dict()
  for pin in pin_data:
    cipher_text = pin["Encrypted PIN"]
    if pin["Customer name"] == "Ebenezer Scrooge":
      scrooge_pin = cipher_text
    encryped_pins[cipher_text] = encryped_pins.setdefault(cipher_text, 0) + 1

  total_ciphers = len(pin_data)
  top_pins = dict()
  THRESHOLD = 0.003
  for cipher_text, count in encryped_pins.items():
    if count / total_ciphers > THRESHOLD:
      top_pins[cipher_text] = count

  print("Ebenezer Scrooge's pin cipher text: %s" % scrooge_pin)
  sorted_pins = OrderedDict(sorted(top_pins.items(), key=lambda p: p[0]))
  for cipher, count in sorted_pins.items():
    print("%s appears %d times (%0.3f%% of %d)" % (
      cipher, count, count / total_ciphers * 100, total_ciphers
    ))

if __name__ == '__main__':
  main()