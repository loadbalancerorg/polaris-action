#!/usr/bin/python
import json
import sys


class PolarisResults:
    total_issues = 0
    new_issues = 0
    job_status = None
    json_data = None
    file_location = '.synopsys/polaris/cli-scan.json'
    summary_url = None

    def __load_file(self):
        try:
            f = open(self.file_location, mode='r')
            self.json_data = json.load(f)
        except FileNotFoundError:
            print('Cannot find file:{0}'.format(self.file_location))
            sys.exit(1)
        except json.JSONDecodeError as e:
            print('Cannot parse json data. Reason:{0}'.format(e.msg))
            sys.exit(2)
        finally:
            f.close()

    def __validate_set_required_fields(self):
        if "tools" not in self.json_data:
            print("missing 'tools' section from json output")
            sys.exit(3)

        if "jobStatus" in self.json_data['tools'][0]:
            self.job_status = self.json_data['tools'][0]['jobStatus']
        else:
            print("missing {'tools': ['jobStatus']} from json output cannot determine result of scan")
            sys.exit(4)

        if "issueSummary" not in self.json_data:
            print("missing {'issueSummary'} from json output and cannot determine if new issues have been created")
            sys.exit(5)

        if "total" in self.json_data['issueSummary']:
            self.total_issues = int(self.json_data['issueSummary']['total'])
        else:
            print("missing {'issueSummary': {'total'} from json output")
            sys.exit(6)

        if "newIssues" in self.json_data['issueSummary']:
            self.new_issues = int(self.json_data['issueSummary']['newIssues'])
        else:
            print("missing {'issueSummary'}")
            sys.exit(7)
        if "summaryUrl" in self.json_data['issueSummary']:
            self.summary_url = self.json_data['issueSummary']['summaryUrl']
        else:
            print("missing {'issueSummary': {'summaryURL'}}")
            sys.exit(8)

    def __init__(self, file_location):
        self.file_location = file_location
        # new_issues and total_issues are strings on purpose because that is what github
        # actions is handing me. I will convert them to integers later on....26/04/21 (things might change)
        # https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputs
        self.__load_file()
        self.__validate_set_required_fields()


if __name__ == "__main__":
    # Get the inputs
    user_file_location = sys.argv[1]
    user_total_issues = int(sys.argv[2])
    user_new_issues = int(sys.argv[3])

    results = PolarisResults('.synopsys/polaris/cli-scan.json')
    if results.job_status != "COMPLETED":
        print("The scan job has not completed successfully. Status: {0}".format(results.job_status))
        sys.exit(10)
    print("Completed: the scan results can be found at: {0}".format(results.summary_url))
    # no threshold set so just check to see if we have new issues
    if user_total_issues == 0 and user_new_issues == 0 and results.new_issues > 0:
        print("{0} new issues discovered these should be fixed before continuing.".format(results.new_issues))
        sys.exit(5)
    # check we do not have too many new issues
    elif results.new_issues > user_new_issues & user_new_issues != 0:
        print("There are too many new issues. New issues detected: {0} threshold {1}"
              .format(results.new_issues, user_new_issues))
        sys.exit(20)
    # check we have not breached the total number of issues.
    elif results.total_issues > user_total_issues & user_total_issues != 0:
        print("The threshold for total issues has been reached:{0} threshold {1}"
              .format(results.total_issues, user_total_issues))
        sys.exit(30)
    else:
        print('Nothing wrong here..good work')
        sys.exit(0)
