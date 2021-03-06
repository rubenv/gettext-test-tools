#!/usr/bin/env python

import fileinput
import sys
import re

fatal = False
infoMatch = re.compile('^(.*?)\.po: (.*)\.$')
labelMatch = re.compile('^(\d+) (.*)$')

threshold = 5 # Max % of fuzzy / untranslated messages
failures = 0
tests = []

for line in fileinput.input():
    if line.strip() == '':
        continue
    
    matches = infoMatch.match(line)
    if matches == None:
        print("Failed to match line: " + line)
        fatal = True
        continue

    filename = matches.group(1).replace("./", "").replace(".", "-")
    rest = matches.group(2)
    test = {
        "filename": filename,
        "translated": 0,
        "fuzzy": 0,
        "untranslated": 0,
        "total": 0,
    }

    parts = rest.split(', ')
    for part in parts:
        matches = labelMatch.match(part)
        if matches == None:
            print("Failed to part " + part + " in line: " + line)
            fatal = True
            continue

        count = int(matches.group(1))
        label = matches.group(2)

        test["total"] += count
        if label.startswith("translated message"):
            test["translated"] = count
        elif label.startswith("fuzzy translation"):
            test["fuzzy"] = count
        elif label.startswith("untranslated message"):
            test["untranslated"] = count
        else:
            print("Unknown label: " + label)
            fatal = True

    tests.append(test)

    if test["fuzzy"] > 0 or test["untranslated"] > 0:
        failures += 1

if fatal:
    sys.exit(1)

print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<testsuites>')
print('  <testsuite name="Translation statistics" errors="0" tests="%d" failures="%d">' % (len(tests), failures))
for test in tests:
    print('    <testcase classname="%s" name="Has translations">' % test["filename"])
    if test["translated"] == 0:
        print('      <failure type="expect">Expected translated messages</failure>')
    print('    </testcase>')
    if test["total"] > 0:
        print('    <testcase classname="%s" name="Has not too much fuzzy translations">' % test["filename"])
        fuzzy = test["fuzzy"] * 100 / float(test["total"])
        if fuzzy > threshold:
            print('      <failure type="expect">Found %d fuzzy translations</failure>' % test["fuzzy"])
        print('    </testcase>')
        print('    <testcase classname="%s" name="Has not too much untranslated messages">' % test["filename"])
        untranslated = test["untranslated"] * 100 / float(test["total"])
        if untranslated > threshold:
            print('      <failure type="expect">Found %d untranslated messages</failure>' % test["untranslated"])
        print('    </testcase>')
print('  </testsuite>')
print('</testsuites>')
