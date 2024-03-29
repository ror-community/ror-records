# ror-records
Test repository for developing deployment process for ROR record updates.

# ROR Data release creation & deployment steps

## Prepare JSON files in ror-updates
1. [Create JSON files for new and updated ROR records](#create-json-files-for-new-and-updated-ror-records)
2. [Validate files in ror-updates](#validate-files-in-ror-updates)
3. [Generate relationships](#generate-relationships)
4. [Validate files again in ror-updates](#validate-files-again-in-ror-updates)

## Release to Staging
1. [Create new release branch](#create-new-release-branch-in-ror-records)
2. [Push new/updated ROR JSON files to release branch](#push-newupdated-ror-json-files-to-release-branch-in-ror-records)
3. [Validate files in ror-records](#validate-files-in-ror-records)
4. [Deploy to Staging](#deploy-to-staging)
5. [Test Staging release](#test-staging-release)

## Release to production
1. [Deploy to Production](#deploy-to-production)
2. [Test production release](#test-production-release)
3. [Create data dump for internal use](#create-data-dump-for-internal-use)

## Publish public data dump
1. [Generate release in ror-updates Github](#generate-release-in-ror-updates-github)
2. [Publish public data dump to Zenodo](#publish-public-data-dump-to-zenodo)
3. [Announce public data dump](#announce-public-data-dump)

## Misc
1. [Manual deployment](#manual-deployment)

# Prepare JSON files in ror-updates

## Create JSON files for new and updated ROR records
JSON files for new and updated ROR records are created by the ROR metadata curation lead and curation advisory board as part of the process managed in [ror-updates](https://github.com/ror-community/ror-updates). **Only changes requested and approved through this curation process are included in ROR data releases.**

Schema-valid ROR record JSON can be generated using the [Leo form app](https://leo.dev.ror.org/). Note that relationships should not be included in record files; these are created in the [Generate relationships](#generate-relationships) step of the deployment process.

Once created, push JSON files to ror-updates in a new branch per below.

### Create new release branch in ror-updates
These steps assume that you have already [installed and configured git](https://git-scm.com/downloads) on your computer, and that you have cloned the [ror-records](https://github.com/ror-community/ror-updates) repository locally.

1. In your local ror-updates directory, checkout the Main branch

        git checkout main

2. Make sure your local Main branch matches the remote branch (make sure to git stash any local changes before doing this!)

        git fetch origin
        git reset --hard origin/main

3. Checkout a new branch based on Main. Branch name does not need to match the ror-records release branch naming convention, but should clearly convey the release number.

        git checkout -b rc-v1.3-review

### Push record files to release branch in ror-updates
1. Create in new directory in the root of the ror-updates repository with the **exact same name** as the branch (ex: rc-v1.3-review).

        mkdir rc-v1.3-review

2. Create subdirectories ```new``` and ```updates``` inside the directory you just created. Note: Creating both directories is not required in order for validation and relationship generation actions to work. If there are only new records or only updates, you only need to create one directory. If there's no ```updates``` directory but the relatinships.csv file contains relationships to production records, the relationship generation action will create an ```updates``` directory and download production records into it.

        mkdir rc-v1.3-review/new
        mkdir rc-v1.3-review/updates

2. Place the JSON files for new and updated records inside the directories you just created.
3. Add and commit the files

        git add rc-v1.3-review/
        git commit -m "add new and updated ROR records to rc-v1.3-review"

4. Push the files and new branch to the remote ror-records repository

        git push origin rc-v1.3-review

5. Repeat steps 1-3 if additional files need to be added to the release candidate.

## Validate files in ror-updates
JSON files for new and updated ROR records should be validated before generating relationshps to check that they comply with the ROR schema and contained properly formatted JSON. Validation is performed by a script [run_validations.py](https://github.com/ror-community/validation-suite/blob/main/run_validations.py) triggered by a Github action [Validate files](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/validate.yml
).

1. Go to https://github.com/ror-community/ror-updates/actions/workflows/validate.yml (Actions > Create relationships in the ror-updates repository)
2. Click Run workflow at right, choose the branch you're working on and leave "Check box to validate relationships" _unchecked_. If you're working on the Main branch or the directory containing the files you'd like to validate has a diffferent name from the branch you're working on, enter name of that directory.
3. Click the green Run workflow button.
4. It will take a few minutes for the workflow to run. If sucessful, a green checkbox will be shown on the workflow runs list in Github, and a success messages will be posted to the #ror-curation-releases Slack channel. If the workflow run is unsuccessful, an red X will be shown on the workflow runs list in Github and an error message will be posted to Slack. To see the error details, click the validate-filtes box on the workflow run page in Github.
5. If this workflow fails, there's an issue with the data in one of more ROR record JSON files that needs to be corrected. In that case, check the error details, make the needed corrections, commit and push the files to your working branch and repeat steps 1-3 to re-run the Validate files workflow.

## Generate relationships
Relationships are not included in the intitial ROR record JSON files. Relationships are generated using a script [generaterelationships.py](https://github.com/ror-community/ror-api/blob/dev/rorapi/management/commands/generaterelationships.py) triggered by a Github action [Create relationships](https://github.com/ror-community/ror-updates/blob/staging/.github/workflows/generate_relationships.yml), which should be run AFTER all new and updated JSON records to be included in the release are uploaded to ror-updates.

*Note: Currently relationships can only be added using this process, not removed. Removing relationships from an existing record requires manually downloading and editing the record, and adding it to the release branch.*

1. Create relationships list as a CSV file using the template [[TEMPLATE] relationships.csv](https://docs.google.com/spreadsheets/d/17rA549Q6Vc-YyH8WUtXUOvsAROwCDmt1vy4Rjce-ELs) and name the file relationships.csv. **IMPORTANT! File must be named relationships.csv and fields used by the script must be formatted correctly**. Template fields used by the script are:

| **Field name**                          | **Description**                                                                             | **Example value**                               |
|-----------------------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------|
| Record ID                               | ROR ID of record being added/updated, in URL form                                           | https://ror.org/015m7w34                        |
| Related ID                              | ROR ID of the related record, in URL form                                                   | https://ror.org/02baj6743                       |
| Relationship of Related ID to Record ID | One the following values: Parent, Child, Related                                            | Parent                                          |
| Name of org in Related ID               | Name of the related organization, as it appears in the name field of the related ROR record | Indiana University – Purdue University Columbus |
| Current location of Related ID          | Production or Release branch                                                                | Production                                      |

2. Place the relationships.csv inside the parent directory where the ROR record JSON files are located (ex: rc-v1.3-review - don't put it inside new or updates directories).
3. Commit and push the relationships.csv file to your working branch, ex:

        git add rc-v1.3-review/relationships.csv
        git commit -m "adding relationships list to v1.3"
        git push origin rc-v1.3-review

3. Go to https://github.com/ror-community/ror-updates/actions/workflows/generate_relationships.yml (Actions > Create relationships in the ror-records repository)
4. Click Run workflow at right, choose the branch that you just pushed relationships.csv to, and click the green Run workflow button.
5. It will take a few minutes for the workflow to run. If sucessful, the workflow will update ROR record JSON files in the branch that you specified, a green checkbox will be shown on the workflow runs list in Github, and a success messages will be posted to the #ror-curation-releases Slack channel. If the workflow run is unsuccessful, an red X will be shown on the workflow runs list in Github and an error message will be posted to Slack. To see the error details, click the generate-relationships box on the workflow run page in Github.
6. If this workflow fails, there's likely a mistake in the relationships.csv or one or more of the ROR record JSON files that needs to be corrected. In that case, make the needed corrections, commit and push the files to the vX.X branch and repeat steps 3-5 to re-run the Create relationships workflow.

## Validate files again in ror-updates
After relationships are added, record files should be validated again to ensure that the changes applied by the script are still schema-valid.
Follow the steps above to run validation, but make sure to tick the "Check box to validate relationships" checkbox.

# Release to Staging

## Create new release branch in ror-records

### Github UI
1. Go to [ror-community/ror-records](https://github.com/ror-community/ror-records)
2. Click the branches dropdown in the upper left (should say 'main' by default)
3. Click staging to switch to the staging branch
4. Click the branches dropdown again (should now say 'staging')
5. Enter the name of your new release branch in the "Find or create branch" field. Names for new release candidate branches should follow the convention v[MAJOR VERSION].[MINOR VERSION].[PATCH VERSION IF APPLICABLE], ex: v1.3.
6. Click Create branch: [NEW BRANCH NAME] from 'staging'

### Git CLI
These steps assume that you have already [installed and configured git](https://git-scm.com/downloads) on your computer, and that you have cloned the [ror-records](https://github.com/ror-community/ror-records) repository locally.

1. In the ror-records checkout the staging branch

        git checkout staging

2. Make sure your local staging branch matches the remote branch (make sure to git stash any local changes before doing this!)

        git fetch origin
        git reset --hard origin/staging

3. Checkout a new branch based on staging. Names for new release candidate branches should follow the convention v[MAJOR VERSION].[MINOR VERSION].[PATCH VERSION IF APPLICABLE], ex: v1.3.

        git checkout -b v1.3

# Push new/updated ROR JSON files to release branch in ror-records

### Github UI
1. On your computer, place all the JSON files for the new and updated ROR records into a folder with the **exact same name** as the release branch (ex, v1.3).
2. In the ror-records repository, click the Branches dropdown at left and choose the vX.X branch that you created in the previous steps.
3. Click the Add file button at right and choose Upload files
4. Add your folder of files as prompted
5. Under Commit changes, type a commit message in the first text box, leave the radio button set to "Commit directly to the vX.X branch" and click Commit changes.
5. Repeat steps 1-4 if additional files need to be added to the release candidate.

### Git CLI
1. Create in new directory in the root of the ror-records repository the **exact same name** as the release branch (ex, v1.3).

        mkdir v1.3

2. Place JSON files for new and updated records inside the directory you just created. Do not place them in subdirectories. If there are relationships, also include relationships.csv file.
. Add and commit the files

        git add v1.3/
        git commit -m "add new and updated ROR records to release v1.3"

3. Push the files and new branch to the remote ror-records repository

        git push origin v1.3

4. Repeat steps 1-3 if additional files need to be added to the release candidate.

## Validate files in ror-records
Before finalizing a release candidate, JSON files for new and updated ROR records should be validated to check that they comply with the ROR schema and contained properly formatted JSON. Validation is performed by a script [run_validations.py](https://github.com/ror-community/validation-suite/blob/main/run_validations.py) triggered by a Github action [Validate files](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/validate.yml
), which should be run after all new and updated JSON records to be included in the release are uploaded to the vX.X branch.

1. Go to https://github.com/ror-community/ror-records/actions/workflows/validate.yml (Actions > Create relationships in the ror-records repository)
2. Click Run workflow at right, choose the current vX.X branch, tick "Check box to validate relationshpis",  and click the green Run workflow button.
3. It will take a few minutes for the workflow to run. If sucessful, a green checkbox will be shown on the workflow runs list in Github, and a success messages will be posted to the #ror-curation-releases Slack channel. If the workflow run is unsuccessful, an red X will be shown on the workflow runs list in Github and an error message will be posted to Slack. To see the error details, click the validate-filtes box on the workflow run page in Github.
4. If this workflow fails, there's an issue with the data in one of more ROR record JSON files that needs to be corrected. In that case, check the error details, make the needed corrections, commit and push the files to the vX.X branch and repeat steps 1-3 to re-run the Validate files workflow.

**IMPORTANT! Validate files workflow must succeed before proceeding to deployment**

## Deploy to Staging
Deploying to staging.ror.org/search and api.staging.ror.org requires making a Github pull request and merging it. Each of these actions triggers different automated workflows:

- **Open pull request against Staging branch:** Check user permissions and validate files
- **Merge pull request to Staging branch:**  Check user permissions, deploy release candidate to Staging API

*Note that only specific Github users (ROR staff) are allowed to open/merge pull requests and create releases.*

1. Go to https://github.com/ror-community/ror-records/pulls (Pull requests tab in ror-records repository)
2. Click New pull request at right
3. Click the Base dropdown at left and choose Staging. Important! Do not make a pull request against the default Main branch.
4. Click the Compare dropdown and choose the vX.X branch that you have been working with in the previous steps.
5. Click Create pull request and enter ```Merge vX.X to staging``` in the Title field. Leave the Comments field blank.
6. Double-check that the Base dropdown is set to Staging and that the list of updated files appears to be correct, then click Create pull request
7. A Github action [Staging pull request](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/staging_pull_request.yml) will be triggered which (1) verifies that the user is allowed to perform a release to staging and (2) runs the file validation script again. If sucessful, a green checkbox will be shown in the pull request details, and a success messages will be posted to the #ror-curation-releases Slack channel.
8. Once the Staging pull request workflow has completed successfully, click Merge pull request
9. A Github action [Deploy to staging](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/merge.yml) will be triggered, which pushes the new and updated JSON files from the vX.X directory to AWS S3 and indexes the data into the ROR Elasticsearch instance. If sucessful, a green checkbox will be shown in the pull request details, and a success messages will be posted to the #ror-curation-releases Slack channel. The new data should now be available in https://staging.ror.org/search and https://api.staging.ror.org

### Multiple staging releases
If records needed to be added or changed after an initial Staging release, add the new/updated records to the existing release branch per [Push new/updated ROR JSON files to release branch](#push-newupdated-ror-json-files-to-release-branch) and repeat the steps to [Generate relationships](#generate-relationships), [Validate files](#validate-files) and [Deploy to Staging](#deploy-to-staging). A few points to note with multiple Staging releases:

- Do not remove records from the release branch that have already been deployed to Staging. Overwrite any records already deployed to Staging that require changes and leave the rest as they are. When ready to deploy to poduction, the release branch should contain all new/updated records to be included in the production release.
- Include relationships for any records already in merged to the vX.X directory on Staging in the release branch relationships.csv (not just the current deployment)
- Deleting record files from the release branch after they have been deployed to Staging will not remove them from the Staging index. At the moment, this will need to be done manually by a developer; in the future, we will add a mechanism to remove records from the Staging index that have been deleted from an release branch. This does not affect production, as the production index is completely separate.

## Test Staging release
*Note: There is currently no staging UI search app (https://staging.ror.org connects to production search app using api.ror.org). UI tests should be run against https://dev.ror.org.*

### New records
Choose several new records from the Staging release and, for each record:
1. Check that the record can be retrieved from the Staging API

        curl https://api.staging.ror.org/organizations/[RORID]

2. Check that the record can be searched by name in the Staging API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters))

          curl https://api.staging.ror.org/organizations?query=[STAGING%20RECORD%20NAME]

### Updated records
Choose several updated records from the Staging release and, for each record:
1. Check that the record can be retrieved from the Staging API

        curl https://api.staging.ror.org/organizations/[RORID]

2. Check that the record can be searched by name in the Staging API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters))

          curl https://api.staging.ror.org/organizations?query=[RECORD%20NAME]

3. Retrieve the record from the Staging API and the Production API and compare changes to verify that the expected changes where made.

        curl https://api.staging.ror.org/organizations/[ROR ID] > staging_[RORID].json
        curl https://api.ror.org/organizations/[ROR ID] > prod_[RORID].json
        diff staging_[RORID].json prod_[RORID].json


### Unchanged records
Choose several records from Production that were not included in the release and for each record:

1. Retrieve the record from the Staging API and the Production API and compare changes to verify that the records are identical.

        curl https://api.staging.ror.org/organizations/[ROR ID] > staging_[RORID].json
        curl https://api.ror.org/organizations/[ROR ID] > prod_[RORID].json
        diff staging_[RORID].json prod_[RORID].json

```diff``` result should be nothing (no response).

# Deploy to Production
Deploying to ror.org/search and api.ror.org requires making a Github pull request and merging it, then tagging and publishing a new release. Each of these actions triggers different automated workflows:

- **Open pull request against Main branch:** Check user permissions and validate files(?)
- **Merge pull request to Main branch:**  Check user permissions and push individual JSON records included in the release to a new directory with the release tag as the directory name in [ror-updates](https://github.com/ror-community/ror-updates). This is for curator convenience; this copy of the release records is not used elsewhere in the deployment process.
- **Publish release:** Check user permissions, deploy release to production API, create new data dump zip file and place in ror-data repository.

*Note that only specific Github users (ROR staff) are allowed to open/merge pull requests and create releases.*

1. Go to https://github.com/ror-community/ror-records/pulls (Pull requests tab in ror-records repository)
2. Click New pull request at right
3. Click the Base dropdown at left and choose Main.
4. Click the Compare dropdown and choose Staging.
5. Click Create pull request, enter ```Merge vX.X to production``` in the Title field. Leave the Comments field blank.
6. Double-check that the Base dropdown is set to Main and that the list of updated files appears to be correct, then click Create pull request
7. A Github action Production pull request will be triggered, which does TBD. If sucessful, a green checkbox will be shown in the pull request details, and a success messages will be posted to the #ror-curation-releases Slack channel.
8. Once the Production pull request workflow has completed successfully, click Merge pull request.
9. Go to https://github.com/ror-community/ror-records/releases (Release tab in ror-records repository)
10. Click Draft new release at right
11. Click the Choose a tag dropdown and enter the version number for the release, ex v1.3. This should be the same number as the release branch and the directory that the release files are located in. Click Create new tag X.X on publish.
12. In the Release name field, enter ```vX.X``` (replace X.X with the release tag number)
13. In the Dsecribe this release field, enter ```Includes updates listed in https://github.com/ror-community/ror-records/milestone/X``` (link to correct milestone for this release)
14. Click Publish release
9. A Github action Deploy to production will be triggered, which pushes the new and updated JSON files to AWS S3, indexes the data into the production ROR Elasticsearch instance and generates  a new data dump file in TBD. If sucessful, a green checkbox will be shown in the pull request details, and a success messages will be posted to the #ror-curation-releases Slack channel. The new data should now be available in https://ror.org/search and https://api.ror.org

## Test production release

Choose several new, updated and unchanged records and, for each record:

1. Check that the record can be retrieved from the Production API and the results are as expected.

        curl https://api.ror.org/organizations/[RORID]

2. Check that the record can be retrieved from the Production API and the results are as expected.

        https://ror.org/[RORID]

3. Check that the record can be searched by name in the Production API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters)) and the results are as expected.

          curl https://api.ror.org/organizations?query=[STAGING%20RECORD%20NAME]

4. Check that the record can be searched by name in the Production UI and the results are as expected.

        https://ror.org/search > Enter name in search box

## Create data dump for internal use
1. In the ror-records repository, go to [Actions > Create data dump](https://github.com/ror-community/ror-records/actions/workflows/generate_dump.yml)
2. Click Run Workflow and enter the name of the release directory (ex, v1.0) and the name of the last production data dump from ror-data that the new dump should be built from, ex 2021-09-23-ror-data (without the .zip file extension)
3. Click the Run workflow button
4. If sucessful, a green checkbox will be shown in the pull request details, and a success messages will be posted to the #ror-curation-releases Slack channel. The new data dump should now be available in ror-data.

# Publish public data dump

## Generate release in ror-updates Github
1. Create a new release in ror-updates that corresponds to the version number of the release
2. Add information in the release notes about the records that have been added and updated. To generate correct Zenodo upload description text, counts of records in release notes must be formatted like:

```
- **Total organizations**: 104,402
- **Records added**: 62
- **Records updated**: 257
```

Added and updated lines are not required. These will not be included in Zenodo description text if they don't exist in the release notes.

## Publish public data dump to Zenodo
**IMPORTANT! Data dump must be created in ror-data AND release must be created in ror-updates before publishing the dump to Zenodo!**
The script that publishes the dump to Zenodo uses the zip file from ror-data and information from the Github release notes to create a new version in Zenodo.

1. In the ror-records repository, go to [Actions > Publish data dump to Zenodo](https://github.com/ror-community/ror-records/actions/workflows/publish_dump_zenodo.yml)
2. Click Run Workflow and enter the release name (ex, v1.17). Leave Zenodo environment and Parent Zenodo Record ID set to the defaults.
3. Click the Run workflow button
4. If sucessful, a green checkbox will be shown in the Actions history, and a success messages will be posted to the #ror-curation-releases Slack channel. The new data dump should now be available in https://zenodo.org/communities/ror-data. The DOI of the new upload will be shown in the "execute script" step of the Action run output in Github.

## Announce production release
Announce the production release on the following channels:
- Community channel in ROR Slack
- Twitter
- Github discussions ("announcements" category)
- PID Forum
- API Users' Group

# Clean up ror-updates Github
1. Close the release milestone
2. Close the issues in the milestone
3. Move the issues in the milestone to the "Done" column on the project board

## Manual deployment

Occasionally, a 504 Gateway Timeout happens while indexing files into AWS ElasticSearch. This will cause the automatic Deploy to Staging (on PR merge) or Deploy to Prod (on release) actions to fail at the Index file step.

In this case, you can re-run the deployment action manually:

1. In the ror-records repository, go to [Actions > Manual deploy to Staging](https://github.com/ror-community/ror-records/actions/workflows/staging_manual_index.yml) or [Actions > Manual deploy to Prod](https://github.com/ror-community/ror-records/actions/workflows/prod_manual_index.yml), depending on which environment you need to deploy to.
2. Click **Run Workflow**, then click **Run worfklow from** and choose the main branch when deploying to production or the staging branch when deploying to staging.
3. In the **Name of the release tag that you would like to deploy**, enter the release name (ex, v1.17)
3. Click the Run workflow button
4. If sucessful, a green checkbox will be shown in the Actions history, and a success messages will be posted to the #ror-curation-releases Slack channel.








