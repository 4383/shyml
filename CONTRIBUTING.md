# Contributing to niet

First off, thanks for taking the time to contribute!

The following as a set of guidelines for contributing to niet.
These are mostly guidelines, not rules. Use your best judgment, and fell
free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed
by the [niet Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [herveberaud.pro@gmail.com](mailto:herveberaud.pro@gmail.com).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for niet.
Following these guidelines helps maintainers and the community
understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please perform a
[cursory search](https://github.com/gr0und-s3ct0r/niet/issues?q=is%3Aissue%20is%3Aopen%20)
to see if the problem has already been reported.
If it has and the issue is still open, add a comment to
the existing issue instead of opening a new one.
When you are creating a bug report, please [include as many details as possbile](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you use the niet command line, e.g. which command exactly you used in the terminal. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**


Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version of niet) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version of niet?** What's the most recent version in which the problem doesn't happen? You can install older versions of niet from [the pypi repository](https://pypi.org/project/niet/).
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of niet are you using?** You can get the exact version by running `pip freeze | grep "niet"` in your terminal.
* **What's the name and version of the OS you're using**?
* **What's the version of python you're using**?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for niet, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion and find related suggestions.

When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion) and including the steps that you imagine you would take if the feature you're requesting existed.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of niet which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most niet users.
* **List some other tools or applications where this enhancement exists.**
* **Specify which version of niet you're using.** You can get the exact version by running `pip freeze| grep "niet"` in your terminal.
* **Specify the name and version of the OS you're using.**
* **Specify the version of python you're using**

## Code Contribution

### Hacking on niet

If you're hitting a bug in niet or just want to experiment with adding a feature, follow these steps.

#### Prerequisites

- [pipenv](https://github.com/kennethreitz/pipenv)
- [pbr](https://docs.openstack.org/pbr/latest/)
- [flake8](http://flake8.pycqa.org/en/latest/)
- [tox](https://tox.readthedocs.io/en/latest/)
- python2.7+

#### Cloning

```shell
$ git clone https://github.com/gr0und-s3ct0r/niet
```

#### Setup your environment

From there, you can navigate into the directory where you've cloned the niet source code,
create a virtual environment and install all the required dependencies:

```shell
$ cd niet
$ pipenv shell # pip install -U pipenv (if not installed)
$ pip install -r requirements.txt
$ pip install -r requirements_dev.txt
$ python setup.py develop
```

#### Make your changes

First create your working branch:
```shell
$ git checkout -b somefeature origin/devel
```

> Be sure to create your working branch from `devel` and be sure your devel are up-to-date

Make our changes:
```shell
$ vim <file-to-edit>
$ git commit -am 'I did some changes'
```

#### Ensure everything work fine

Every following checks are automaticaly executed on pull requests so need to
be sure that all of these checks run successfully before submit your pull request
on github.

Code formating and PEP8 validation:
```shell
$ tox -e pep8
```

Unit tests:
```shell
$ tox # by default run tests en python 2.7, 3.4, 3.5, 3.6
```

> Note: If you have just a specific version of python installed on your system, you can test like this:
```shell
$ tox -e py35 # test with python 3.5
```

### Pull Requests

If everything work fine you can create your pull request.

Before ensure you have [squash your commits](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html).

> Be sure to submit your pull request on the upstream `devel` branch!

By using [git-pull-request](https://github.com/jd/git-pull-request):
```shell
$ pip install -U git-pull-request # if not installed
$ git pull-request 
Forked repository: https://github.com/gr0und-s3ct0r/niet
Force-pushing branch `somefeature' to remote `github'
Counting objects: 5, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 562 bytes | 0 bytes/s, done.
Total 5 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/gr0und-s3ct0r/niet.git
 + 73a733f7...1be2bf29 somefeature -> somefeature (forced update)
 Pull-request created: https://github.com/grOund-s3ctOr/niet/pull/33
```

Or manually directly from github:
* Include examples, outputs, etc... whenever possible.
* Include screenshots and animated GIFs in your pull request whenever possible.

## Special cases

### Generate manpages

For generate man-pages for niet read the following instructions:
```shell
$ cd docs
$ make man
$ man --local-file _build/man/niet.1
```
