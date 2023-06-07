- https://stackoverflow.com/questions/15886469/dropping-all-collections-in-mongoengine
- https://python.hotexamples.com/site/file?hash=0x0dbd402bf678506e7804b5ff1487f3ab482c3c85279c8cba9b0c28b412f0f33a&fullName=elijah-openstack-master/cloudlet-gateway/app.py&project=cmusatyalab/elijah-openstack
- https://stackoverflow.com/questions/65589955/attributeerror-module-flask-login-login-manager-has-no-attribute-user-loader

### **`@login_manager.user_loader` not being detected in `models.py`**

- https://stackoverflow.com/questions/63089350/missing-user-loader-error-exception-in-flask-app

### **How to display new-line characters**

- https://stackoverflow.com/questions/29608841/how-do-i-store-display-paragraphs-with-mongodb

### **Default values for fields in `Flask-WTF`**

https://stackoverflow.com/questions/21314068/wtforms-field-defaults-suddenly-dont-work

### **Use tab to indent in textarea**

https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea

### **MongoDB's cons**

- No join queries (ex. joining 2 collections with the same field name)
- perhaps should have used planetscale and sqlalchemy for this project

### **How to redirect to the previous page in Flask**

- https://stackoverflow.com/questions/42284397/flask-how-to-redirect-to-previous-page-after-successful-login
- use session to store the previous URL

```
# session is a dict
from flask import session

session['url'] = url_for('previous_URL')
```

### Optional Parameters in Flask

- https://stackoverflow.com/questions/14032066/can-flask-have-optional-url-parameters
- useful for the `common` routes

## **todo**

- Homepage:

  - edit full name works
  - edit email works
  - edit profile picture link works, but picture doesn't display
  - update description works
  - personal links work
  - about me works

- experience:
  - can create experience
  - can view experience
  - within experience:
    - CAN'T edit company name
    - CAN'T edit position
    - CAN'T edit start and stop dates
    - CAN'T add tech stack yet
    - can add bullet points
    - can add links
    - can't edit about
