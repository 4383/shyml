# niet

[![Build Status](https://travis-ci.org/openuado/niet.svg?branch=master)](https://travis-ci.org/openuado/niet)
![PyPI](https://img.shields.io/pypi/v/niet.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niet.svg)
![PyPI - Status](https://img.shields.io/pypi/status/niet.svg)
[![Downloads](https://pepy.tech/badge/niet)](https://pepy.tech/project/niet)
[![Downloads](https://pepy.tech/badge/niet/month)](https://pepy.tech/project/niet/month)

Get data from YAML file directly in your shell.

> How to easily parse and retrieve data from YAML file in our shell?

A few years ago the previous question led us to develop niet.

Indeed, at that time we needed a way to retrieve data for our own needs and
so we created niet. The goal was to develop a tools that will allow us to
standardize how we parse YAML locally or in our CI pipelines. We wanted
something reusable and easily distribuable.

Niet was born.

Niet is like [xmllint](http://xmlsoft.org/xmllint.html) or
[jq](https://stedolan.github.io/jq/) but for YAML and JSON data -
you can use it to slice and filter and map and transform structured data.

You can easily retrieve data by using simple expressions or using
xpath advanced features to access non-trivial data.

You can easily convert YAML format into JSON format and vice versa.

## Features
- Extract elements by using xpath syntax
- Extract values from json format
- Extract values from yaml format
- Automaticaly detect format (json/yaml)
- Read data from a web resource
- Read data from file or pass data from stdin
- Format output values
- Format output to be reused by shell `eval`
- Convert YAML to JSON
- Convert JSON to YAML

## Install or Update niet

```sh
$ pip install -U niet
```

## Requirements

- Python 3.6 or higher

## Supported versions

Since niet 2.0 the support of python 2.7 have been dropped so if
if you only have python 2.7 at hands then you can use previous version (lower
to 2.0) but you should consider first that the no support will be given on
these versions (no bugfix, no new feature, etc). If you report an issue or
or propose a new feature then they will be addressed only for current or
higher version.

## Usage

### Help and options

```shell
$ niet --help
usage: niet [-h] [-f {json,yaml,eval,newline,ifs,squote,dquote,comma}] [-s] [-v]
            object [file]

Read data from YAML or JSON file

positional arguments:
  object                Path to object separated by dot (.). Use '.' to get
                        whole file. eg: a.b.c
  file                  Optional JSON or YAML filename. If not provided niet
                        read from stdin

optional arguments:
  -h, --help            show this help message and exit
  -f {json,yaml,eval,newline,ifs,squote,dquote,comma}, --format {json,yaml,eval,newline,ifs,squote,dquote,comma}
                        output format
  -i, --in-place        Perform modification in place. Will so alter read file
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Print output in a file instead of stdout (surcharged
                        by infile parameter if set)
  -s, --silent          silent mode, doesn't display message when element was
                        not found
  -v, --version         print the Niet version number and exit (also
                        --version)
  --debug               Activate the debug mode (based on pdb)

output formats:
  json          Return object in JSON
  yaml          Return object in YAML
  eval          Return result in a string evaluable by a shell eval command as an input
  newline       Return all elements of a list in a new line
  ifs           Return all elements of a list separated by IFS env var
  squote        Add single quotes to result
  dquote        Add double quotes to result
  comma         Return all elements separated by commas
```

### With Json from stdin

```shell
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "Fizz", "4", "Buzz"]}}' | niet fizz.buzz
1
2
Fizz
4
Buzz
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "Fizz", "4", "Buzz"]}}' | niet fizz.buzz -f squote
'1' '2''Fizz' '4' 'Buzz'
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "fizz", "4", "buzz"]}}' | niet . -f yaml
fizz:
  buzz:
  - '1'
  - '2'
  - fizz
  - '4'
  - buzz
foo: bar
$ echo '{"foo": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet "fizz.buzz[2]"
two
$ echo '{"foo": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f dquote "fizz.buzz[0:2]"
"zero" "one"
$ echo '{"foo": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f dquote "fizz.buzz[:3]"
"zero" "one" "two"

```

### With YAML file

Consider the yaml file with the following content:
```yaml
# /path/to/your/file.yaml
project:
    meta:
        name: my-project
    foo: bar
    list:
        - item1
        - item2
        - item3
    test-dash: value
```

You can [download the previous example](https://gist.githubusercontent.com/4383/53e1599663b369f499aa28e27009f2cd/raw/389b82c19499b8cb84a464784e9c79aa25d3a9d3/file.yaml) locally for testing purpose or use the command line for this:
```shell
wget https://gist.githubusercontent.com/4383/53e1599663b369f499aa28e27009f2cd/raw/389b82c19499b8cb84a464784e9c79aa25d3a9d3/file.yaml
```

You can retrieve data from this file by using niet like this:
```sh
$ niet ".project.meta.name" /path/to/your/file.yaml
my-project
$ niet ".project.foo" /path/to/your/file.yaml
bar
$ niet ".project.list" /path/to/your/file.yaml
item1 item2 item3
$ # assign return value to shell variable
$ NAME=$(niet ".project.meta.name" /path/to/your/file.yaml)
$ echo $NAME
my-project
$ niet project.'"test-dash"' /path/to/your/file.json
value
```

### With JSON file

Consider the json file with the following content:
```json
{
    "project": {
        "meta": {
            "name": "my-project"
        },
        "foo": "bar",
        "list": [
            "item1",
            "item2",
            "item3"
        ],
        "test-dash": "value"
    }
}
```

You can [download the previous example](https://gist.githubusercontent.com/4383/1bab8973474625de738f5f6471894322/raw/0048cd2310df2d98bf4f230ffe20da8fa615cef3/file.json) locally for testing purpose or use the command line for this:
```shell
wget https://gist.githubusercontent.com/4383/1bab8973474625de738f5f6471894322/raw/0048cd2310df2d98bf4f230ffe20da8fa615cef3/file.json
```

You can retrieve data from this file by using niet like this:
```sh
$ niet "project.meta.name" /path/to/your/file.json
my-project
$ niet "project.foo" /path/to/your/file.json
bar
$ niet "project.list" /path/to/your/file.json
item1 item2 item3
$ # assign return value to shell variable
$ NAME=$(niet "project.meta.name" /path/to/your/file.json)
$ echo $NAME
my-project
$ niet project.'"test-dash"' /path/to/your/file.json
value
```

### Object Identifiers

An identifier is the most basic expression and can be used to extract a single
element from a JSON/YAML document. The return value for an identifier is
the value associated with the identifier. If the identifier does not
exist in the JSON/YAML document, than niet display a specific message and
return the error code `1`, example:

```sh
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "3"]}}' | niet fizz.gogo
Element not found: fizz.gogo
$ echo $?
1
```

See the [related section](#deal-with-errors) for more info on how to manage
errors with `niet`.

Niet is based on `jmespath` to find results so for complex research you can
refer to the [jmespath specifications](http://jmespath.org/specification.html#identifiers)
to use identifiers properly.

If you try to search for an identifier who use some dash you need to surround
your research expression with simple and double quotes, examples:

```sh
$ echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f dquote '"foo-biz"'
bar
$ echo '{"key-test": "value"}' | niet '"key-test"'
value
```

However, `niet` will detect related issues and surround automatically your
identifier if `jmespath` fail to handle it.

Hence, the following examples will return similar results than the previous
examples:

```sh
$ echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f dquote foo-biz
bar
$ echo '{"key-test": "value"}' | niet key-test
value
```

If your object is not at the root of your path, an example is available in
`tests/sample/sample.json`, then you need to only surround the researched
identifier like this `project.'"test-dash"'`

```json
{
    "project": {
        "meta": {
            "name": "my-project"
        },
        "foo": "bar",
        "list": [
            "item1",
            "item2",
            "item3"
        ],
        "test-dash": "value"
    }
}

```

Example:
```sh
niet project.'"test-dash"' tests/sample/sample.json
```

Further examples with [`jmespath` identifiers](http://jmespath.org/specification.html#examples).

### Output

#### Stdout
By default, niet print the output on stdout. 

#### Save output to a file
It if possible to pass a filename using -o or --output argument to writes
directly in a file. This file will be created if not exists or will be
replaced if already exists.

#### In-file modification
It is possible to modify directly a file using -i or --in-place argument. This will replace
the input file by the output of niet command. This can be used to extract some data of a file or
reindent a file.

### Output formats 
You can change the output format using the -f or --format optional 
argument. 

By default, niet detect the input format and display complex objects
in the same format. If the object is a list or a value, newline output
format will be used.

Output formats are: 
  - ifs
  - squote
  - dquote
  - newline
  - yaml
  - json

#### ifs
Ifs output format print all values of a list or a single value in one line.
All values are separated by the content of IFS environment variable if defined,
space otherwise.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ IFS="|" niet .project.list /path/to/your/file.yaml -f ifs
item1|item2|item3
$ IFS=" " niet .project.list /path/to/your/file.yaml -f ifs
item1 item2 item3
$ IFS="@" niet .project.list /path/to/your/file.yaml -f ifs
item1@item2@item3
```

This is usefull in a shell for loop,
but your content must, of course, don't contain IFS value:
```shell
OIFS="$IFS"
IFS="|"
for i in $(niet .project.list /path/to/your/file.yaml -f ifs); do
    echo ${i}
done
IFS="${OIFS}"
```

Previous example provide the following output:
```sh
item1
item2
item3
```

For single quoted see [squote](#squote) ouput or [dquote](#dquote) double quoted output with IFS

#### squote
Squotes output format print all values of a list or a single value in one line.
All values are quoted with single quotes and are separated by IFS value.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ # With the default IFS
$ niet .project.list /path/to/your/file.yaml -f squote
'item1' 'item2' 'item3'
$ # With a specified IFS
$ IFS="|" niet .project.list /path/to/your/file.yaml -f squote
'item1'|'item2'|'item3'
```

#### dquote
Dquotes output format print all values of a list or a single value in one line.
All values are quoted with a double quotes and are separated by IFS value.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ # With the default IFS
$ niet .project.list /path/to/your/file.yaml -f dquote
'item1' 'item2' 'item3'
$ # With a specified IFS
$ IFS="|" niet .project.list /path/to/your/file.yaml -f dquote
"item1"|"item2"|"item3"
```

#### newline

`newline` output format print one value of a list or a single value per line.

The `newline` format is mostly usefull with shell while read loops and
with script interactions.

Example:
```sh
while read value: do
    echo $value
done < $(niet --format newline project.list your-file.json)
```

#### comma

`comma` output format print results on the same line and separated by commas.

The `comma` format allow you to format your outputs to consume your results
with other commands lines interfaces. By example some argument parser
allow you to pass multi values for the same parameter (the
[beagle command](https://beagle-hound.readthedocs.io/en/latest/) per
example allow you to
[repeat the `--repo` option](https://beagle-hound.readthedocs.io/en/latest/cli/index.html#cmdoption-beagle-search-repo)).

Example of integration with beagle and shell:

```sh
$ OSLO_PROJECTS_URL=https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml
$ beagle search \
    -f link \
    --repo $(niet "oslo.deliverables.*.repos[0]" ${OSLO_PROJECTS_URL} -f comma) 'venv'
```

The previous command will return all the links of files
who contains `venv` on the openstack oslo's scope of projects (pbr,
taskflow, oslo.messaging, etc).

Else another with a more reduced scope on openstack oslo's projects:

```sh
$ niet "oslo.deliverables.*.repos[0][?contains(@, \`oslo\`) == \`true\`]" \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml \
    -f comma
openstack/oslo-cookiecutter,openstack/oslo-specs,openstack/oslo.cache,
openstack/oslo.concurrency,openstack/oslo.config,openstack/oslo.context,
openstack/oslo.db,openstack/oslo.i18n,openstack/oslo.limit,openstack/oslo.log,
openstack/oslo.messaging,openstack/oslo.middleware,
openstack/oslo.policy,openstack/oslo.privsep,openstack/oslo.reports,
openstack/oslo.rootwrap,openstack/oslo.serialization,openstack/oslo.service,
openstack/oslo.tools,openstack/oslo.upgradecheck,openstack/oslo.utils,
openstack/oslo.versionedobjects,openstack/oslo.vmware,openstack/oslotest
```

In the previous example we retrieve only the projects repos who contains
`oslo` in their names, so other projects like `taskflow`, `pbr`, etc will
be ignored.

#### eval

Eval output format allow you to eval output string to initialize shell
variable generated from your JSON/YAML content.

You can intialize shell variables from your entire content, example:

```sh
$ echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f eval .
 foo_biz="bar";fizz__buzz=( zero one two three )
$ eval $(echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f eval .)
$ echo ${foo_biz}
bar
$ echo ${fizz__buzz}
zero one two three
$ eval $(echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f eval '"foo-biz"'); echo ${foo_biz}
bar
$ echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f eval fizz.buzz
fizz_buzz=( zero one two three );
```

Parent elements are separated by `__` by example the `fizz.buzz` element
will be represented by a variable named `fizz__buzz`. You need to consider
that when you call your expected variables.

Also you can initialize some shell array from your content and loop over in
a shell maner:

```sh
$ eval $(echo '{"foo-biz": "bar", "fizz": {"buzz": ["zero", "one", "two", "three"]}}' | niet -f eval fizz.buzz)
$ for el in ${fizz_buzz}; do echo $el; done
zero
one
two
three
```
 
#### yaml
Yaml output format force output to be in YAML regardless the input file format.

#### json
Json output format force output to be in JSON regardless the input file format.

### Read data from a web resource

Niet allow you to read data (json/yaml) from a web resource accessible by using
the HTTP protocole (introduced in niet 2.1).

This can be done by passing an url to niet which refer to a raw content (json
or yaml).

Here is some examples with the [openstack governance's projects data](https://github.com/openstack/governance/blob/master/reference/projects.yaml):

```sh
$ # List all the oslo projects repos (https://wiki.openstack.org/wiki/Oslo)
$ niet "oslo.deliverables.*.repos[0]" \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml
openstack/automaton
openstack/castellan
...
openstack/debtcollector
...
openstack/futurist
openstack/oslo.cache
openstack/oslo.concurrency
openstack/oslo.config
openstack/oslo.context
openstack/oslo.db
openstack/oslo.i18n
openstack/oslo.limit
openstack/oslo.log
openstack/oslo.messaging
openstack/oslo.middleware
openstack/oslo.policy
...
openstack/oslo.service
openstack/osprofiler
openstack/pbr
...
openstack/stevedore
openstack/taskflow
openstack/tooz
openstack/whereto
$ niet oslo.service \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml
Common libraries
$ # Get the openstack oslo's mission
$ niet oslo.mission \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml
To produce a set of python libraries containing code shared by OpenStack projects.
The APIs provided by these libraries should be high quality, stable, consistent,
documented and generally applicable.
$ eval $(niet oslo.service \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml -f eval) && \
    test "${oslo_service}" = "Common libraries"
$ # Get the name of the oslo PTL
$ eval $(niet oslo.ptl.name \
    https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml -f eval)
$ echo "${oslo_ptl_name}" # now display your evaluated result
$ # Convert original distant yaml file into json
$ niet . https://raw.githubusercontent.com/openstack/governance/master/reference/projects.yaml -f json
```

For further examples of filters and selections please take a look to
[the jmespath's doc](https://jmespath.org/examples.html).

### Result not found

By default when no results was found niet display a specific message and return
the error code `1`, example:
```sh
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "3"]}}' | niet fizz.gogo
Element not found: fizz.gogo
$ echo $?
1
```

You can avoid this behavior by passing niet into a silent mode.

Silent mode allow you to hide the specific message error but continue to return
a status code equal to `1` when the key was not found.

You can use the silent mode by using the flag `-s/--silent`, example:
```sh
$ echo '{"foo": "bar", "fizz": {"buzz": ["1", "2", "3"]}}' | niet fizz.gogo -s
$ echo $?
1
```

### Deal with errors

When your JSON file content are not valid niet display an error and exit
with return code `1`

You can easily protect your script like this:
```sh
PROJECT_NAME=$(niet project.meta.name your-file.yaml)
if [ "$?" = "1" ]; then
    echo "Error occur ${PROJECT_NAME}"
else
    echo "Project name: ${PROJECT_NAME}"
fi
```

## Examples

You can try niet by using the samples provided with the project sources code.

> All the following examples use the sample file available in niet sources code
at the following location `tests/samples/sample.yaml`.

Sample example:
```yaml
# tests/samples/sample.yaml
project:
    meta:
        name: my-project
    foo: bar
    list:
        - item1
        - item2
        - item3
```

### Extract a single value 

Retrieve the project name:
```sh
$ niet project.meta.name tests/samples/sample.yaml
my-project
```

### Extract a list and parse it in shell

Deal with list of items
```sh
$ for el in $(niet project.list tests/samples/sample.yaml); do echo ${el}; done
item1
item2
item3
```

Also you can `eval` your `niet` output to setput some shell variables
that you can reuse in your shell scripts, the following example is similar to
the previous example but make use of the eval ouput format (`-f eval`):

```sh
$ eval $(niet -f eval project.list tests/samples/sample.yaml)
$ for el in ${project__list}; do echo $el; done
zero
one
two
three
```

### Extract a complex object and parse it in shell

Extract the object as JSON to store it in shell variable :
```shell
$ project="$(niet -f json .project tests/samples/sample.yaml)"
```

Then parse it after in bash in this example:
```shell
$ niet .meta.name <<< $project
my-project
```

### Transform JSON to YAML

With niet you can easily convert your JSON to YAML
```shell
$ niet . tests/samples/sample.json -f yaml
project:
  foo: bar
  list:
  - item1
  - item2
  - item3
  meta:
    name: my-project
```

### Transform YAML to JSON

With niet you can easily convert your YAML to JSON
```shell
$ niet . tests/samples/sample.yaml -f json
{
    "project": {
        "meta": {
            "name": "my-project"
        },
        "foo": "bar",
        "list": [
            "item1",
            "item2",
            "item3"
        ]
    }
}
```

### Indent JSON file

This is an example of how to indent a JSON file :
```shell
$ niet . tests/samples/sample_not_indented.json 
{
    "project": {
        "meta": {
            "name": "my-project"
        },
        "foo": "bar",
        "list": [
            "item1",
            "item2",
            "item3"
        ],
        "test-dash": "value"
    }
}
```


## Tips

You can pass your search with or without quotes like this:
```sh
$ niet project.meta.name your-file.yaml
$ niet "project.meta.name" your-file.yaml
```

You can execute `niet` step by step by using the debug mode. It will allow
you to inspect your execution during your debug sessions.

## Contribute

If you want to contribute to niet [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)
