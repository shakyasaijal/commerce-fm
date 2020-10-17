# eCommerce System

## Table of contents

- [Django Setup](#django-setup)
- [Configuration](#configuration)
- [Edit Config File](#edit-config-file)
- [Celery](#celery)
- [Geo Data](#geo-data)
- [React Setup](https://github.com/shakyasaijal/commerce-fm)

## Django Setup

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements/development.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Configuration

`Located In ecommerce/config/config.yaml.example`

```
$ cd config
$ cp config.yaml.example config.yaml
```

## Edit Config File

`1. MULTI_VENDOR = 'True if ecommerce is required for multiple vendors, else False' `<br/>

`2. ADD_TO_CART_WITHOUT_LOGIN = 'True if user can add to cart without login and order without account, else False.' `<br/>

`3. HAS_ADDITIONAL_USER_DATA = 'True if other model has a relationship with User model. The other model will be used to take user information like: address, phone, interests, etc.' `<br/>

`4. MUST_HAVE_ADDITIONAL_DATA = 'True if "HAS_ADDITIONAL_USER_DATA" and if additional data is required to comtinue with other features. For example: without address, phone, interests, etc. user cannot move to other pages.' `<br/>

`5. HAS_CELERY = 'True' if you want celery with redis broker `<br/>

`6. CELERY_FOR_EMAIL = 'True' if you want to send all emails through celery. "HAS_CELERY" also needs to be True to use this. `<br/>

`7. CELERY_BROKER_URL = 'broker_url'. By default, this application has redis configured. You can change with your own choice. `<br/>

`8. DISPLAY_OUT_OF_STOCK_PRODUCTS = 'Should out of stock product needs to be displayed in frontend. True if Yes else False. For example: We won't be able to view out of stock products if it's False.' `<br/>

`9. HAS_REFERRAL_APP = 'True if you need referral code for the ecommerce user and earn rewards else False.'` <br/>

`10. HAS_VENDOR_REFERRAL_APP = 'True if you need referral code for vendors as well.' ` <br/>

`11. FRONTEND_URL = 'Url of frontend for referal redirect url.' `<br/>

`12. TEMPLATE_VERSION = 'This is a template version for dashboard designs.' `<br/>

`13. jwt_secret = 'Secret key for generating access token and refresh token.' `<br/>

`Other configurations are related to django settings.py`

## Celery

`celery -A ecommerce worker -l info`

## Geo Data

`1. Please download GeoLite2-city.mmdb from Max Mind:` [Click Here](https://www.maxmind.com/en/home)<br/>
`2. Add that DB to ecommerce/ecommerce/GeoData/`
