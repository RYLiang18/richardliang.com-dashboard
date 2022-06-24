- https://stackoverflow.com/questions/15886469/dropping-all-collections-in-mongoengine
- https://python.hotexamples.com/site/file?hash=0x0dbd402bf678506e7804b5ff1487f3ab482c3c85279c8cba9b0c28b412f0f33a&fullName=elijah-openstack-master/cloudlet-gateway/app.py&project=cmusatyalab/elijah-openstack
- https://stackoverflow.com/questions/65589955/attributeerror-module-flask-login-login-manager-has-no-attribute-user-loader

### **`@login_manager.user_loader` not being detected in `models.py`**
- https://stackoverflow.com/questions/63089350/missing-user-loader-error-exception-in-flask-app 

### **How to display new-line characters**
- https://stackoverflow.com/questions/29608841/how-do-i-store-display-paragraphs-with-mongodb

## **Todo**
- refactor `new_default_homepage()` to future registration code instead of putting it in login code
    - edge case: extremely pepega, but what if new user tries to access their homepage details api without first logging in
- Email property in homepage
- make sure that when user updates their PFP link that the link ends in .jpg or .png