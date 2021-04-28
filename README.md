# polaris-action
Github action for Coverity Polaris scanner. 
This action is designed to be included in your worflow files and gives the ability to run a polaris scan against your codebase
(NOTE: you will need an active polaris subscription for this to work)

# Usage
Create your github workflow configuration in .github/workflows/scan.yml or something similar ish

```yml
name: CI Dooer
on: push
jobs:
  coverity_polaris_check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2
      - name: Run Polaris tests
        uses: loadbalancerorg/polaris-action@v1
        with: 
          server_url: ${{ secrets.POLARIS_URL }} # (Required)
          access_token: ${{ secrets.POLARIS_ACCESS_TOKEN }} # (Required)
          total_issues: 0 # (Not required)
          new_issues: 0 # (Not required)
          cli_scan_json_file: .synopsys/polaris/cli-scan.json # (Not required)
          
```

if total_issues and new_issues are not set the build will be marked as a failure if any new issues in the code are detected. You can set thresholds by setting values in total_issues or new_issues. Which when reached will fail the builds. For example if you set new_issues to 5 if 6 new issues are detected then the build will fail. The same is true of total_issues.  

# Arguments
- server_url: Your polaris instance url (required)
- access_token: Your user access token created in the polaris interface (required)
- total_issues: (default:0)
- new_issues: (default:0)
- cli_scan_json_file: When the scan completes the results are stored in cli-scan.json. By default its .synopsys/polaris/cli-scan.json if yours differs alter this value. 

Any problems feel free to contact github@loadbalancer.org 
