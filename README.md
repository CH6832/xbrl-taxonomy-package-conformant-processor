# XBRL Taxonomy Package Conformant Processor

## :newspaper: About the project

A small command line program that checks whether an XBRL Taxonomy Package complies with the [Standard Taxonomy Package 1.0](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html) and adjusts it if necessary.

### How it works

1. Run for example `app.py EDINET "full/path/to/input/archive.zip"`. The `app.py` file is the starting point of the application. `EDINET` represents the Electronic Disclosure System provided by the [JFSA](https://www.fsa.go.jp/en/). The path afterwards can be any path locating an XBRL Taxonomy Package (ZIP). In this case `EDINET` is the abbreveation of the taxonomy package provider and `full/path/to/archive.zip` is the path to the zip archive. Packages to test/to experiment with the application are located in the `input`-folder.

2. The class `Checker` class in `TPChecker.py` analyzes the package according to the [Taxonomy Package 1.0 standard](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html). The result of the analyzation is displayed on the command line.

3. Based on the result calculated by the `Checker`-class, the next step is to fix the package. `TPFixer.py` contains an Interface with relevant abstract methods. Each class represents a package by a specific provider. When the class is initialized, the package to fix will be copied over to the `output`-folder. The definied methods from the Interface are responsible for fixing the package. The result of the fixed package will be a fixed `zip` archive containing all relevant data.

### Content overview

    .
    ├── dist/ - python wheel file to install
    ├── docs/ - generated documentation
    ├── images/readme - all images for the app
    ├── input/ - taxonomy packages
    ├── logs/ - logfiles
    ├── src/ - source code
    ├── tests/ - code and data for tests
    ├── .gitignore - contains folders/files ignored by git
    ├── CHANGELOG.md - logfile about project changes
    ├── COPYRIGHT - project copyright
    ├── LICENSE - license text
    ├── README.md - project overview and starting point
    ├── requirements.txt - requirements to run the project
    ├── SECURITY.md - security information
    └── setup.py - projects metadata

## :notebook: Features

* Checking and fixing:
  * xml format checking
  * case sensitivity checking (done by python)
  * archive format ceck
  * top-level directory checking and fixing
  * META-INF folder checking and fixing
  * taxonomyPackage.xml checkng and fixing
  * catalog.xml checking and fixing
  * URL resolution checking and fixing
  * Entrypoint localiazation

## :runner: Getting started

### Prerequisites and example usage

0. Install requirements:

```sh
pip3 install -r requirements.txt
```

1. Navigate into `src` folder

```sh
cd src/
```

2. Run script:

```sh
py app.py [PROVIDER] [PATH/TO/PKG]
```

```sh
py app.py EDINET "input/ALL_20221101/ALL_20221101.zip"
```

```sh
Input information:
------------------
    Provider -> EDINET
    Package  -> ..\input\ALL_20221101\ALL_20221101.zip

Analyzis results:
------------------
    DONE: Package is ZIP
    ERROR: Package has not single toplevel dir
    ERROR: Package has no META-INF folder
    ERROR: Package has no catalog.xml
    ERROR: Package has no taxonomy-package.xml

Fixing package...
.\abspath\to\fixed\zip\Reporting_Frameworks_3.3.0.0_errata.zip
    Final zip generated

Output result:
--------------
    ..\output\ALL_20221101\ALL_20221101.zip is fixed!
```

### Run tests

0. Move into `tests/` folder

```sh
py run_tests.py
```

1. Or you can run every test separately as well:

```sh
pytest test_EBAFixer.py
```

### Create documentation

0. Move into `docs/` folder

```sh
cd docs
```

1. Initilaize project:

```sh
sphinx-quickstart 
```

2. Build/rebuild the documentation:

```sh
make html
```

3. move into `html` folder

```sh
cd `docs/build/html`
```

4. Open `index.html` in browser

![index.html](/images/readme/docs_index.jpg)

### Build and install the `.whl` package

0. Upgrade packages:

```sh
py -m pip install --upgrade build 
```

1. Build package:

```sh
py -m build 
```

2. Install the package:

```sh
py -m pip install "dist/example_package_CHRISTOPH_HARTLEB-0.0.1-py3-none-any.whl"
```

## :bulb: Tips and Tricks

    Use absolute paths for input XBRL taxonomy packages to avoid any path-related issues.
    Ensure your input packages adhere to the XBRL Taxonomy Package 1.0 standard for accurate processing.

## :wrench: Troubleshooting

If you encounter any issues while using the tool, consider the following troubleshooting steps:

- Check if all prerequisites are installed correctly.
- Verify that the input XBRL taxonomy package is valid and adheres to the required format.
- Refer to the error messages for clues on what might be going wrong.
- Search for similar issues in the project's GitHub repository or online forums.

## :loudspeaker: Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please follow these steps:

* Fork the repository.
* Create a new branch for your feature or bug fix.
* Make your changes and ensure all tests pass.
* Submit a pull request with a clear description of your changes.

## :open_book: Documentation

For more information on how to use the tool and its features, open the [official documentation](/docs/build/html/index.html) in a browser of your choice.

## :rocket: Roadmap

Here are some planned features and enhancements for future releases:

    Support for additional XBRL taxonomy package standards.
    Improved error handling and logging.
    Integration with other XBRL processing tools.

## :raising_hand: Support

If you need any assistance or have any questions about the project, feel free to reach out to us via email or open a new issue in the GitHub repository.

## :bookmark: License

This project is licensed under the terms of the [GPL v3](LICENSE).

## :copyright: Copyright

See the [COPYRIGHT](COPYRIGHT) file for copyright and licensing details.

## :books: Resources used to create this project

* Python
  * [Python 3.12 documentation](https://docs.python.org/3/)
  * [Built-in Functions](https://docs.python.org/3/library/functions.html)
  * [Python Module Index](https://docs.python.org/3/py-modindex.html)
  * [lxml - XML and HTML with Python](https://lxml.de/)
  * [SETUPTOOLS - Documentation](https://setuptools.pypa.io/en/latest/)
  * [Python Packaging User Guide](https://packaging.python.org/en/latest/)
  * [Sphinx](https://www.sphinx-doc.org/en/master/)
* XBRL
  * [Extensible Business Reporting Language (XBRL) 2.1](https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html)
  * [Taxonomy Packages 1.0](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html)
* XML
  * [Extensible Markup Language (XML) 1.0 (Fifth Edition)](https://www.w3.org/TR/xml/)
  * [W3C XML Schema Definition Language (XSD) 1.1 Part 1: Structures](https://www.w3.org/TR/xmlschema11-1/)
* Commandline tools
  * [Master the Art of Command Line: Your Ultimate Guide to Developing Powerful Tools](https://hackernoon.com/master-the-art-of-command-line-your-ultimate-guide-to-developing-powerful-tools)
  * [Command Line Interface Guidelines](https://clig.dev/)
* Markdwon
  * [Basic syntax](https://www.markdownguide.org/basic-syntax/)
  * [Complete list of github markdown emofis](https://dev.to/nikolab/complete-list-of-github-markdown-emoji-markup-5aia)
  * [Awesome template](http://github.com/Human-Activity-Recognition/blob/main/README.md)
  * [.gitignore file](https://git-scm.com/docs/gitignore)
* Editor
  * [Visual Studio Code](https://code.visualstudio.com/)
