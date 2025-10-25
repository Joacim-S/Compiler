My compiler implementation for the [Comppilers course](https://hy-compilers.github.io/spring-2025/). See the [language spec](https://hy-compilers.github.io/spring-2025/language-spec/) and [project](https://hy-compilers.github.io/spring-2025/project/#recommended-featureset) pages of the course for supported features.

To try the compiler:

- Download the project release version and extract the files.

- Open Compiler/compilers-project


Install dependencies:

    # Install Python specified in `.python-version`
    pyenv install
    # Install dependencies specified in `pyproject.toml`
    poetry install

Then you can compile a source code file like this:

    #Creates a binary file from the provided source code file.
    ./compiler.sh compile path/to/source/code --output=path/to/output/file

[The language spec](https://hy-compilers.github.io/spring-2025/language-spec/#syntax) page has a simple program you can easily try, as well as syntax for writing your own programs. Trying to compile an invalid program will result in an error.

To run the compiled binary:

    #Add execution permissions to the file
    chmod +x path/to/output/file
    #Run the program
    path/to/output/file
