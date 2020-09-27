# eCommerce System

React Implementation of **E-Commerce: Single and Multi Vendor** web app.

## Table of contents

- [Pre-requisites](#prerequisites)
- [Running it locally](#running-it-locally)
- [Eslint and Prettier](#eslint-and-prettier)
- [Errors](#errors)
- [Backend Setup](https://github.com/shakyasaijal/commerce-fm/tree/dev/ecommerce)

## Pre-requisites

If you want to setup node and run the application in your host os.

- [Yarn >= v1](https://yarnpkg.com/en/docs/install)
  [we are using yarn as primary package manager.]
- [npm 5+](https://www.npmjs.com/package/eslint-config-airbnb)
  [We are using npm only for eslint-config-airbnb]

## Running it locally

```
/**
    If you want to clone the repo using https use https://github.com/shakyasaijal/commerce-fm.git instead.
*/

Clone with SSH
$ git clone git@github.com:shakyasaijal/commerce-fm.git
$ cd commerce-fm
```

Pull the dependencies and start server.

```
$ yarn install
$ yarn run dev
```

## Eslint and Prettier

For the default eslint config we are using:

- eslint
- prettier
- [eslint-config-airbnb](https://github.com/airbnb/javascript)

For viewing the lint related issues, run the following command.

```
$ yarn eslint
```

For fixing the lint related issues run the following command:

```
$ yarn eslint:fix
```

For fixing the formatting related issues run the following command:

```
yarn prettier:fix
```

For fixing the both lint and prettier related issues run the following command:

```
$ yarn lint:fix
```

## Errors

- Checking errors: `$ yarn lint`
- Error during commit: `$ yarn lint:fix`

[Note: Pre commit hook is installed so unless lint and prettier auto fix or a programmer themselves fixes formatting related issues, commit can't be made.]
