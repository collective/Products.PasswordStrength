*** Keywords ***

## Actions

Own passwords registration enabled
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@security-controlpanel
    Input for  Let users select their own passwords  Select checkbox
    Click button  Save
    Input for  Let users select their own passwords  Checkbox should be selected
    Disable autologin

Own passwords registration disabled
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@security-controlpanel
    Input for  Let users select their own passwords  Unselect checkbox
    Click button  Save
    Input for  Let users select their own passwords  Checkbox should not be selected
    Disable autologin

Input for
    [arguments]     ${title}   ${extra_keyword}   @{list}
    ${for}=  Get Element Attribute  xpath=//label[contains(., "${title}")]  for
    Run Keyword     ${extra_keyword}  id=${for}   @{list}

Hint for
    [arguments]     ${title}   ${extra_keyword}   @{list}
    Run Keyword     ${extra_keyword}  xpath=//label[contains(., "${title}")]/span[@class="formHelp"]   @{list}

Error for
    [arguments]     ${title}   ${extra_keyword}   @{list}
    Run Keyword     ${extra_keyword}  xpath=//label[contains(., "${title}")]/following-sibling::div[@class="fieldErrorBox"]   @{list}

## Common tests

Test change password form
    Log in  test-user  secret
    Sleep  2
    Go to  ${PLONE_URL}/@@change-password
    # Element should contain  css=h1.documentFirstHeading  Reset Password
    # Contains password description ?
    Hint for  New password  Element should contain   Minimum 1 capital letter
    # In Plone 4.1, the current password can't be validated
    # Products/PlonePAS/gruf_support.py(16)authenticate() : 'test_user_1_' used as login in place of 'test-user'
    Run keyword if  '${plone_version}' <= '4.1.99'  Pass execution  Stopped this test with Plone < 4.2
    # Reacts with bad password
    Input for  Current password  Input text  secret
    Input for  New password  Input text  12345
    Input for  Confirm password  Input text  12345
    Click button  Change Password
    # Redirected on same page
    Element should be visible  jquery=div.error>div:contains("This password doesn't match requirements for passwords")
    # Accepts well formed password
    Input for  Current password  Input text  secret
    Input for  New password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Change Password
    # Redirected on same page
    Element should be visible  jquery=dl.portalMessage dd:contains('Password changed')
    Log out

Test register form without password
    Own passwords registration disabled
    Go to  ${PLONE_URL}/@@register
    # Contains password description ?
    Input for  Password  Element should not be visible
    # Fill form
    Input for  User Name  Input text  rocky
    Input for  E-mail  Input text  rocky@balboa.com
    Click button  Register
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome
    ${message} =  Get The Last Sent Email
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}
    # Contains password description ?
    Hint for  Password  Element should contain  Minimum 1 capital letter.
    # Fill form
    Input for  User id  Input text   rocky
    Input for  User name  Input text   12345
    Input for  Confirm password  Input text  12345
    Click button  Reset Password
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
    Input for  User Name  Input text   rocky
    Input for  E-mail  Input text  rocky@balboa.com
    Input for  Password  Input text   ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Register
    Element should contain  css=h1.documentFirstHeading  Welcome
    # do a reset
    Go to  ${PLONE_URL}/mail_password_form?userid=rocky
    Click button  Start password reset
    ${message} =  Get The Last Sent Email
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}
    # Contains password description ?
    Hint for  New Password  Element should contain  Minimum 1 capital letter.
    # Fill form
    Input for  User id  Input text  rocky
    Input for  Password  Input text  12345
    Input for  Confirm password  Input text  12345
    Click button  Reset
    # Reacts with bad password
    Error for  Password  Element should contain  Minimum 1 capital letter.
    Input for  User id  Input text  rocky
    Input for  Password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Reset Password
    Element should contain  css=div.documentDescription  Your password has been set successfully.
