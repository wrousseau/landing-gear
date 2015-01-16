import csv
import os.path
import sys
import json
import argparse

def parse_value(raw_value):
    if raw_value in ['true', 'True']:
        return True
    elif raw_value in ['false', 'False']:
        return False
    return raw_value

def main(argv):
    parser = argparse.ArgumentParser('Tests a scade test result file against a given requirement')
    parser.add_argument('--requirement', required=True, help='the requirement file (json format)')
    parser.add_argument("--raw", help="the raw scade test results file (csv format)", required=True)
    named_args = parser.parse_args()
    if (not(os.path.isfile(named_args.requirement))):
        print named_args.requirement
        print "The specified requirement file does not exist"
        sys.exit()

    if (not(os.path.isfile(named_args.raw))):
        print "The specified raw results file does not exist"
        sys.exit()

    rules_data=open(named_args.requirement)
    rules = json.load(rules_data)

    with open(named_args.raw, 'rb') as csv_file:
        results_reader = list(csv.DictReader(csv_file, delimiter=';'))
        i = 1
        for rule in rules['rules']:
            variable_name = rule['variable']
            expected_value = rule['expectedValue']
            step = rule['step']
            print "=================="
            print "Rule %d : %s should equal %s at step %d" % (i, variable_name, str(expected_value), step)
            row_at_step = results_reader[step]
            key = rules['packagePrefix'] if rules['packagePrefix'] else ''
            key += variable_name
            observed_value = parse_value(row_at_step[key])
            success = (observed_value == expected_value)
            success_message = "Success" if success else "Failure:"
            print '\n'+success_message
            if (not(success)):
                print "Expected %s but received %s" % (str(expected_value), str(observed_value))
            print "=================\n"
            i += 1

if __name__ == "__main__":
    main(sys.argv[1:])
