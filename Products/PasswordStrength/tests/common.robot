*** Keywords ***

## Actions

Own passwords registration enabled
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@security-controlpanel
    Select checkbox  id=form.enable_user_pwd_choice
    Click button  id=form.actions.save
    Checkbox should be selected  id=form.enable_user_pwd_choice
    Disable autologin

Own passwords registration disabled
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@security-controlpanel
    Unselect checkbox  id=form.enable_user_pwd_choice
    Click button  id=form.actions.save
    Checkbox should not be selected  id=form.enable_user_pwd_choice
    Disable autologin

## Common tests

Test change password form
    Log in  test-user  secret
    Sleep  2
    Go to  ${PLONE_URL}/@@change-password
    # Element should contain  css=h1.documentFirstHeading  Reset Password
    # Contains password description ?
    Element should contain  css=#content-core form div:nth-of-type(2).field div.formHelp  Minimum 1 capital letter
    # In Plone 4.1, the current password can't be validated
    # Products/PlonePAS/gruf_support.py(16)authenticate() : 'test_user_1_' used as login in place of 'test-user'
    Run keyword if  '${plone_version}' <= '4.1.99'  Pass execution  Stopped this test with Plone < 4.2
    # Reacts with bad password
    Input text  name=form.current_password  secret
    Input text  name=form.new_password  12345
    Input text  name=form.new_password_ctl  12345
    Click button  id=form.actions.reset_passwd
    # Redirected on same page
    Element should be visible  jquery=div.error>div:contains("This password doesn't match requirements for passwords")
    # Accepts well formed password
    Input text  name=form.current_password  secret
    Input text  name=form.new_password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.new_password_ctl  ABCDEFGHIJabcdefghij1!
    Click button  id=form.actions.reset_passwd
    # Redirected on same page
    Element should be visible  jquery=dl.portalMessage dd:contains('Password changed')
    Log out

Test register form without password
    Own passwords registration disabled
    Go to  ${PLONE_URL}/@@register
    # Contains password description ?
    Element should not be visible  css=#formfield-form-password
    # Fill form
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    Click button  id=form.actions.register
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome
    ${message} =  Get The Last Sent Email
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}
    # Contains password description ?
    Element should contain  css=form[name="pwreset_action"] div:nth-of-type(2).field div.formHelp  Minimum 1 capital letter.
    # Fill form
    Input text  userid  rocky
    Input text  password  12345
    Input text  password2  12345
    Click button  css=form[name="pwreset_action"] input[type="submit"]
    # Reacts with bad password
    Element should contain  css=div.error div  Minimum 1 capital letter.
    Input text  userid  rocky
    Input text  password  ABCDEFGHIJabcdefghij1!
    Input text  password2  ABCDEFGHIJabcdefghij1!
    Click button  css=form[name="pwreset_action"] input[type="submit"]
    Element should contain  css=div.documentDescription  Your password has been set successfully.

Test reset form
    # create the user
    Go to  ${PLONE_URL}/@@register
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Click button  id=form.actions.register
    Element should contain  css=h1.documentFirstHeading  Welcome
    # do a reset
    Go to  ${PLONE_URL}/mail_password_form?userid=rocky
    Click button  css=form[name="mail_password"] input[type="submit"]
    ${message} =  Get The Last Sent Email
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}
    # Contains password description ?
    Element should contain  css=form[name="pwreset_action"] div:nth-of-type(2).field div.formHelp  Minimum 1 capital letter.
    # Fill form
    Input text  userid  rocky
    Input text  password  12345
    Input text  password2  12345
    Click button  css=form[name="pwreset_action"] input[type="submit"]
    # Reacts with bad password
    Element should contain  css=div.error div  Minimum 1 capital letter.
    Input text  userid  rocky
    Input text  password  ABCDEFGHIJabcdefghij1!
    Input text  password2  ABCDEFGHIJabcdefghij1!
    Click button  css=form[name="pwreset_action"] input[type="submit"]
    Element should contain  css=div.documentDescription  Your password has been set successfully.
