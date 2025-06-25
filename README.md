# Purpose of this repository

Basically, this repository is a **clone** of this git directory:

```
https://github.com/ror-community/ror-records
```

In this github, you can find all the ror.org **releases**, with the **json** content of the **added** and **modified** oragnisations for each release.

The aim is to create the json transformation to rdf format for each release. Then, from there, to create a commit and an automatic push that would merge all the organisations into the github. Making a separate push for each release will allow us to put tags corresponding to the name of the release, and to make a git diff to see the history of organisations that have been modified or added.

In a nutshell:

1. Switching from json to ttl
2. Commit and push by release
3. Git diff to see changes

## Problems

One of the things to be expected was the structure of the json depending on the different releases. Over the course of its development, ror has changed the architecture of its json several times, making the work directly more complicated, because the template and the code are not adapted to each structure. It will no doubt be necessary to recover each version of the structure and then adapt the code accordingly. As far as the tests to check this are concerned, here's what I've done:

```
1. Test on v1.0/01912nj27.json
    --> argument error due to different structure

2. Test on structure similar to that of the last dump available (v1.66-2025-05-20-ror-data.json)
    --> test on file v1.66/00b3mhg89.json
        -> argument error, because different structure
    --> test on file v1.66/v1/00b3mhg89.json
        -> correct output in folder_to_push
```

What we are going to try to do is to detect the version used. At this address, ror explains the different json structures used during development.

```
https://github.com/ror-community/ror-schema?tab=readme-ov-file
https://ror.readme.io/docs/schema-versions
```

We now need to find out which version our json file belongs to. It is also possible to check our json using these commands:

```
jsonschema -i test.json ror_schema_v2_0.json //  obsolete with jsonschema
check-jsonschema --schemafile test.json ror_schema_v2_0.json // last version
```

## What has been done and problems encountered

The procedure for achieving our goal is as follows:

- retrieve json structures from https://github.com/ror-community/ror-schema?tab=readme-ov-file
- creation of **detect_version_json.py** to find the version of each json (**1.0**, **2.0**, **2.1**)
- creation of 3 templates (**template_1_0**, **template_2_0**, **template_2_1**)
- **template_to_try.py** to associate my json with the correct template
    - if no version matches, **test** json with template
- **create_rdf_file.py** to transform json into rdf
    - if no version matches, **nothing** can be done, so critical error

This solves the first part of the problem of transforming json into rdf. What's missing now is the commit part and automatic push to github.

‼️ Warning ‼️ Subyt currently overwrites duplicate files, which means that there are normally **64,000** files that are added and modified among all the releases. However, in the output folder, there are only **34,000**. This is because there are around **30,000** files that are modified, so as subyt rewrites the json on top, it doesn't take into account the old json.

The problem will be solved at the time of the commit & push part on github, because once pushed, the files will be deleted from the folder in question, and there will be **no duplicates, no deleted files**.

## Resolution

The programme is functional and can be used to transform json to rdf and then push release by release to github. Using tags for each release, you can see the new files added for each release. Here is a summary of the files used and their usefulness:

```
release_rdf_push    // centralises functions and browses directories
detect_version_json // detect the json version according to the ror struct and associate the template
template_to_try     // depending on the version of the json, associate the template and test
git_commit_push     // commits and pushes files to github, then deletes the push files from folder_to_push
create_rdf_file     // creating rdf files using subyt
```

Here's a diagram:

```
release_rdf_push --> template_to_try --> detect_version_json --> create_rdf_file --> git_commit_push
```

## Precision

In the end, we end up with around 64,000 ttl organisations using the releases. This is because the 116,000 organisations in the dump include inactive companies and certain sub-organisations.