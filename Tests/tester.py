import csv
import os
import glob
import sys
import json
import argparse

test_result_file = None
run_all_tests = False

def parse_value(raw_value):
    if raw_value in ['true', 'True']:
        return True
    elif raw_value in ['false', 'False']:
        return False
    return raw_value

def printout(output_file, string):
    print string
    output_file.write(string)
    output_file.write('\n')

def test_requirement(requirement_id):
    requirement_file_path = ''.join(('Requirements/', requirement_id, '.req'))

    if (not(os.path.isfile(requirement_file_path))):
        print os.getcwd()
        print "The specified requirement file does not exist"
        sys.exit()

    raw_result_file_path = ''.join(('Raw/', requirement_id, '.csv'))

    if (not(os.path.isfile(raw_result_file_path))):
       print "The specified raw results file does not exist"
       sys.exit()

    rules_data = open(requirement_file_path)
    rules = json.load(rules_data)

    global test_result_file
    if (test_result_file == None):
        test_result_file_path = ''.join(('Results/', requirement_id, '.txt'))
        test_result_file = open(test_result_file_path, 'w')
    printout(test_result_file, 'Test results for requirement number '+requirement_id)
    printout(test_result_file, 'Requirement file: '+requirement_file_path)
    printout(test_result_file, 'Raw file: '+raw_result_file_path)
    printout(test_result_file, '\n')

    with open(raw_result_file_path, 'rb') as csv_file:
        results_reader = list(csv.DictReader(csv_file, delimiter=';'))
        i = 1
        for rule in rules['rules']:
            variable_name = rule['variable']
            expected_value = rule['expectedValue']
            step = rule['step']
            printout(test_result_file, "==================")
            printout(test_result_file, "Rule %d : %s should equal %s at step %d" % (i, variable_name, str(expected_value), step))
            row_at_step = results_reader[step]
            key = rules['packagePrefix'] if rules['packagePrefix'] else ''
            key += variable_name
            observed_value = parse_value(row_at_step[key])
            success = (observed_value == expected_value)
            success_message = "Success" if success else "Failure:"
            printout(test_result_file, '\n'+success_message)
            if (not(success)):
                print "Expected %s but received %s" % (str(expected_value), str(observed_value))
            printout(test_result_file, "==================\n")
            i += 1

    global run_all_tests
    if (run_all_tests):
        printout(test_result_file, "\n=====================================================================\n")

def main(argv):
    parser = argparse.ArgumentParser('Tests a scade test result file against a given requirement')
    parser.add_argument('--requirement', required=False, help='The requirement id under the valid format : Rxx. The given id should match a requirement file (Requirements/Rxx.req) and a raw results file (Raw/Rxx.req)')
    named_args = parser.parse_args()

    global test_result_file

    if named_args.requirement == None:                      # When no arguments is given, run all tests from the requirements folder
        global run_all_tests
        run_all_tests = True
        test_result_file_path = 'Results/TestsResults.txt'
        test_result_file = open(test_result_file_path, 'w')     # Open file in writing mode to overwrite the content
        test_result_file = open(test_result_file_path, 'a')     # Then open it in append mode so that every test results is appended into it
        print 'Running all tests...'
        print 'Results will be written into ' +  test_result_file_path
        for filename in glob.glob('Requirements/*.req'):
            filename = filename.split('/')[1]
            requirement_id = filename.split('.req')[0]
            test_requirement(requirement_id)

    else:
        test_requirement(named_args.requirement)


if __name__ == "__main__":
    main(sys.argv[1:])
