# ror-records
Test repository for developing deployment process for ROR record updates.

# ROR Data release creation & deployment steps

1. [Create JSON files for new and updated ROR records](#create-json-files-for-new-and-updated-ror-records)
2. [Create new release branch](#create-new-release-branch)
3. [Push new/updated ROR JSON files to release branch](#push-newupdated-ror-json-files-to-release-branch)
4. [Generate relationships](#generate-relationships)
5. [Validate files](#validate-files)
6. [Deploy to Staging](#deploy-to-staging)
7. [Test Staging release](#test-staging-release)
8. [Deploy to Production](#deploy-to-production)
9. [Test production release](#test-production-release)
10. [Publish data dump to Zenodo](#publish-data-dump-to-zenodo)
11. [Announce production release](#announce-production-release)

# Create JSON files for new and updated ROR records
JSON files for new and updated ROR records are created by the ROR metadata curation lead and curation advisory board as part of the process managed in [ror-updates](https://github.com/ror-community/ror-updates). **Only changes requested and approved through this curation process are included in ROR data releases.**

Schema-valid ROR record JSON can be generated using the [Leo form app](https://leo.dev.ror.org/). Note that relationships should not be included in record files; these are created in the [Generate relationships](#generate-relationships) step of the deployment process.

# Create new release branch

## Github UI
1. Go to [ror-community/ror-records](https://github.com/ror-community/ror-records)
2. Click the branches dropdown in the upper left (should say 'main' by default)
3. Click staging to switch to the staging branch
4. Click the branches dropdown again (should now say 'staging')
5. Enter the name of your new release branch in the "Find or create branch" field. Names for new release candidate branches should follow the convention v[MAJOR VERSION].[MINOR VERSION].[PATCH VERSION IF APPLICABLE], ex: v1.3.
6. Click Create branch: [NEW BRANCH NAME] from 'staging'

## Git CLI
These steps assume that you have already [installed and configured git](https://git-scm.com/downloads) on your computer, and that you have cloned the [ror-records](https://github.com/ror-community/ror-records) repository locally.

1. In the ror-records checkout the staging branch

        git checkout staging

2. Make sure your local staging branch matches the remote branch (make sure to git stash any local changes before doing this!)

        git fetch origin
        git reset --hard origin/staging

3. Checkout a new branch based on staging. Names for new release candidate branches should follow the convention v[MAJOR VERSION].[MINOR VERSION].[PATCH VERSION IF APPLICABLE], ex: v1.3.

        git checkout -b v1.3

# Push new/updated ROR JSON files to release branch

## Github UI
1. On your computer, place all the JSON files for the new and updated ROR records into a folder with the **exact same name** as the release branch (ex, v1.3).
2. In the ror-records repository, click the Branches dropdown at left and choose the vX.X branch that you created in the previous steps.
3. Click the Add file button at right and choose Upload files
4. Add your folder of files as prompted
5. Under Commit changes, type a commit message in the first text box, leave the radio button set to "Commit directly to the vX.X branch" and click Commit changes.
5. Repeat steps 1-4 if additional files need to be added to the release candidate.

## Git CLI
1. Create in new directory in the root of the ror-records repository the **exact same name** as the release branch (ex, v1.3).

        mkdir v1.3

2. Place the JSON files for new and updated records inside the directory you just created.
2. Add and commit the files

        git add v1.3/
        git commit -m "add new and updated ROR records to release v1.3"

3. Push the files and new branch to the remote ror-records repository

        git push origin v1.3

4. Repeat steps 1-3 if additional files need to be added to the release candidate.

# Generate relationships
Relationships are not included in the intitial ROR record JSON files. Relationships are generated using a script [generaterelationships.py](https://github.com/ror-community/ror-api/blob/dev/rorapi/management/commands/generaterelationships.py) triggered by a Github action [Create relationships](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/generate_relationships.yml), which should be run AFTER all new and updated JSON records to be included in the release are uploaded to the vX.X branch.

*Note: Currently relationships can only be added using this process, not removed. Removing relationships from an existing record requires manually downloading and editing the record, and adding it to the release branch.*

1. Create relationships list as a CSV file using the template [[TEMPLATE] relationships.csv](https://docs.google.com/spreadsheets/d/17rA549Q6Vc-YyH8WUtXUOvsAROwCDmt1vy4Rjce-ELs) and name the file relationships.csv. **IMPORTANT! File must be named relationships.csv and fields used by the script must be formatted correctly**. Template fields used by the script are:

| **Field name**                          | **Description**                                                                             | **Example value**                               |
|-----------------------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------|
| Record ID                               | ROR ID of record being added/updated, in URL form                                           | https://ror.org/015m7w34                        |
| Related ID                              | ROR ID of the related record, in URL form                                                   | https://ror.org/02baj6743                       |
| Relationship of Related ID to Record ID | One the following values: Parent, Child, Related                                            | Parent                                          |
| Name of org in Related ID               | Name of the related organization, as it appears in the name field of the related ROR record | Indiana University – Purdue University Columbus |
| Current location of Related ID          | Production or Release branch                                                                | Production                                      |

2. Place the relationships.csv inside the vX.X directory where the ROR record JSON files are located.
3. Commit and push the relationships.csv file to the current rc branch

        git add v1.3/relationships.csv
        git commit -m "adding relationships list to v1.3"
        git push origin v1.3

3. Go to https://github.com/ror-community/ror-records/actions/workflows/generate_relationships.yml (Actions > Create relationships in the ror-records repository)
4. Click Run workflow at right, choose the vX.X branch that you just pushed relationships.csv to, and click the green Run workflow button.
5. It will take a few minutes for the workflow to run. If sucessful, the workflow will update ROR record JSON files in the vX.X branch that you specified, a green checkbox will be shown on the workflow runs list in Github, and a success messages will be posted to the #ror-curation-releases Slack channel. If the workflow run is unsuccessful, an red X will be shown on the workflow runs list in Github and an error message will be posted to Slack. To see the error details, click the generate-relationships box on the workflow run page in Github.
6. If this workflow fails, there's likely a mistake in the relationships.csv or one or more of the ROR record JSON files that needs to be corrected. In that case, make the needed corrections, commit and push the files to the vX.X branch and repeat steps 3-5 to re-run the Create relationships workflow.

# Validate files
Before finalizing a release candidate, JSON files for new and updated ROR records should be validated to check that they comply with the ROR schema and contained properly formatted JSON. Validation is performed by a script [run_validations.py](https://github.com/ror-community/validation-suite/blob/main/run_validations.py) triggered by a Github action [Validate files](https://github.com/ror-community/ror-records/blob/staging/.github/workflows/validate.yml
), which should be run after all new and updated JSON records to be included in the release are uploaded to the vX.X branch.

1. Go to https://github.com/ror-community/ror-records/actions/workflows/validate.yml (Actions > Create relationships in the ror-records repository)
2. Click Run workflow at right, choose the current vX.X branch, tick "Check box to validate relationshpis",  and click the green Run workflow button.
3. It will take a few minutes for the workflow to run. If sucessful, a green checkbox will be shown on the workflow runs list in Github, and a success messages will be posted to the #ror-curation-releases Slack channel. If the workflow run is unsuccessful, an red X will be shown on the workflow runs list in Github and an error message will be posted to Slack. To see the error details, click the validate-filtes box on the workflow run page in Github.
4. If this workflow fails, there's an issue with the data in one of more ROR record JSON files that needs to be corrected. In that case, check the error details, make the needed corrections, commit and push the files to the vX.X branch and repeat steps 1-3 to re-run the Validate files workflow.

**IMPORTANT! Validate files workflow must succeed before proceeding to deployment**

# Deploy to Staging
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

# Test Staging release

## New records
Choose several new records from the Staging release and, for each record:
1. Check that the record can be retrieved from the Staging API

        curl https://api.staging.ror.org/organizations/[RORID]

2. Check that the record can be retrieved from the Staging UI

        https://staging.ror.org/[RORID]

3. Check that the record can be searched by name in the Staging API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters))

          curl https://api.staging.ror.org/organizations?query=[STAGING%20RECORD%20NAME]

4. Check that the record can be searched by name in the Staging UI

        https://staging.ror.org/search > Enter name in search box

## Updated records
Choose several updated records from the Staging release and, for each record:
1. Check that the record can be retrieved from the Staging API

        curl https://api.staging.ror.org/organizations/[RORID]

2. Check that the record can be retrieved from the Staging UI

        https://staging.ror.org/[RORID]

3. Check that the record can be searched by name in the Staging API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters))

          curl https://api.staging.ror.org/organizations?query=[RECORD%20NAME]

4. Check that the record can be searched by name in the Staging UI

        https://staging.ror.org/search > Enter name in search box

5. Retrieve the record from the Staging API and the Production API and compare changes to verify that the expected changes where made.

        curl https://api.staging.ror.org/organizations/[ROR ID] > staging_[RORID].json
        curl https://api.ror.org/organizations/[ROR ID] > prod_[RORID].json
        diff staging_[RORID].json prod_[RORID].json


## Unchanged records
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

# Test production release

Choose several new, updated and unchanged records and, for each record:

1. Check that the record can be retrieved from the Production API and the results are as expected.

        curl https://api.ror.org/organizations/[RORID]

2. Check that the record can be retrieved from the Production API and the results are as expected.

        https://ror.org/[RORID]

3. Check that the record can be searched by name in the Production API (make sure to [escape spaces and reserved characters](https://ror.readme.io/docs/rest-api#reserved-characters)) and the results are as expected.

          curl https://api.ror.org/organizations?query=[STAGING%20RECORD%20NAME]

4. Check that the record can be searched by name in the Production UI and the results are as expected.

        https://ror.org/search > Enter name in search box

# Publish data dump to Zenodo
1. Download the vX.X-YYYY-MM-DD-ror-data.zip file from ror-data to your computer
2. Log into [Zenodo](https://zenodo.org/) using the info@ror.org account
3. Create a new upload in the [ROR Data community](https://zenodo.org/communities/ror-data) (see past example https://doi.org/10.5281/zenodo.4929693). Make sure to include Related Identifiers metadata referencing previous releases.

# Announce production release
TODO: develop standard text and  list of channels that we announce new release to
TODO: process for notifying requestors that their curation request has been completed


