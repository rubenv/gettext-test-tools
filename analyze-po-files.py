#!/usr/bin/env python

import fileinput
import sys
import re

fatal = False
infoMatch = re.compile('^(\w+\.po): (.*)\.$')
labelMatch = re.compile('^(\d+) (.*)$')

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

    filename = matches.group(1)
    rest = matches.group(2)
    test = {
        "filename": filename,
        "translated": 0,
        "fuzzy": 0,
        "untranslated": 0,
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

        if label == "translated messages":
            test["translated"] = count
        elif label == "fuzzy translations":
            test["fuzzy"] = count
        elif label == "untranslated messages":
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
    print('    <testcase classname="%s" name="Has no fuzzy translations">' % test["filename"])
    if test["fuzzy"] > 0:
        print('      <failure type="expect">Found %d fuzzy translations</failure>' % test["fuzzy"])
    print('    </testcase>')
    print('    <testcase classname="%s" name="Has no untranslated messages">' % test["filename"])
    if test["fuzzy"] > 0:
        print('      <failure type="expect">Found %d untranslated messages</failure>' % test["untranslated"])
    print('    </testcase>')
print('  </testsuite>')
print('</testsuites>')
