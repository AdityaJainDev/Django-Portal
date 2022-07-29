# AD IT Systems Portal

## Development

* Install Requirements.txt:
  ```
  $ pip3 install requirements-frozen.txt
  ```
  Source: <https://pypi.org/project/mysqlclient/>
  
* Run python server:
    ```
    $ python manage.py runserver
    ```
- For SEPA payments, navigate to 
    ```
    localhost:8000/sepa?knr="knr"&token="token"
    ```
    - Replace `knr` and `token` with respective values
    - No login required for this form.

- For Login, use [Kunden Center](https://kunden.aditsystems.de/kc/Login/Login.html) credentials by navigating to `http://localhost:8000/en/accounts/login/`

- Dashboard displays Invoice Details and Personal Data, which can be edited or viewd in more details.

## API usage

- CRM Endpoint -> `https://ascrm.aditsystems.de/api/{CRMModule}/{CRMAction}`
    * CRMModule and CRMAction is fetched via PHP [RestFul API](https://git.aditsystems.de/as-crm/kundencenter/-/tree/main/modules)
    * Replace the variables and fetch data accordingly.