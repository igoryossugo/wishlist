# Genie
A wishlist API

## Installation


1.  Create a virtualenv (use `virtualenvwrapper`):

        mkvirtualenv genie

2.  Install requirements via `pip`:

        make requirements-dev

3. (Optional) Install required libs for debian base OS:
    As root:
    ```sh
    apt install libcurl4-openssl-dev libssl-dev
    ```

4.  Run the project:

        make run

## Tests


To run the test suite, execute:

    make test

## Create new release


We use `bumpversion` to generate new releases, following the base
principles of [SEMVER](http://semver.org/).

-   Patch [ X.X.0 to X.X.1 ] :

        make release-patch

-   Minor [ X.0.X to X.1.X ] :

        make release-minor

-   Major [ 0.X.X to 1.X.X ] :

        make release-major
