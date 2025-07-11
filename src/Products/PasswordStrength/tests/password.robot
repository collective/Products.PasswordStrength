*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Test Setup
Test Teardown  Close all browsers

*** Test Cases ***

Test register form
    Go to  ${PLONE_URL}/@@register
    # Contains password description ?
    Hint for  Password  Element should contain  Minimum 1 capital letter.
    # Fill form
    Input for  User Name  Input text  rocky
    Input for  Email  Input text  rocky@balboa.com
    # Reacts with bad password
    Input for  Password  Input text    12345
    Input for  Confirm password  Input text  12345
    Click button  Register
    Error for  Password  Element should be visible
    Error for  Password  Element should contain   This password doesn't match requirements for passwords
    Error for  Confirm password  Element should be visible
    Error for  Confirm password  Element should contain  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input for  Password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Register
    Error for  Password  Element should not be visible
    Error for  Confirm password  Element should not be visible
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome

Test new user form
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@new-user
    # Contains password description ?
    Hint for  Password  Element should contain   Minimum 1 capital letter.
    # Fill form
    Input for  User Name  Input text  rocky
    Input for  Email  Input text  rocky@balboa.com
    # Reacts with bad password
    Input for  Password  Input text  12345
    Input for  Confirm password  Input text  12345
    Click button  Register
    Error for  Password  Element should be visible
    Error for  Password  Element should contain  This password doesn't match requirements for passwords
    Error for  Confirm password  Element should be visible
    Error for  Confirm password  Element should contain  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input for  Password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Register
    Error for  Password  Element should not be visible
    Error for  Confirm password  Element should not be visible
    # Redirected
    Wait until page contains  Add New User  5
    Element should contain  css=h1.documentFirstHeading  Users
    Page should contain element  css=input[value="rocky"]
    Disable autologin


Test change password form
    # Log in  test-user  secret
    Enable autologin as  Manager
    @{roles} =  Create list  Manager
    Create User  tester  password=testTEST123$  roles=@{roles}
    Disable autologin
    Log in  tester  testTEST123$
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
    Input for  Current password  Input text  testTEST123$
    Input for  New password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Change Password
    # Redirected on same page
    Element should be visible  jquery=div.portalMessage:contains('Password changed')
    Go to  ${PLONE_URL}/logout

Test register form without password
    Enable autologin as  Manager
    @{roles} =  Create list  Manager
    Create User  tester  password=testTEST123$  roles=@{roles}
    Disable autologin

    Own passwords registration disabled
    Go to  ${PLONE_URL}/@@register
    # Contains password description ?
    Element should not be visible  Input for  Password
    # Fill form
    Input for  User Name  Input text  rocky
    Input for  Email  Input text  rocky@balboa.com
    Click button  Register
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome
    ${message_bytes} =  Get The Last Sent Email
    ${message} =  Decode Bytes To String  ${message_bytes}  utf-8
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}

    # Contains password description ?
    # passwordreset has different (manual) form markup than z3c-form based forms...
    Element should contain  xpath=//label[contains(., "New password")]/following::small  Minimum 1 capital letter.
    # Fill form
    Input for  My user name is  Input text   rocky
    Input for  New password  Input text   12345
    Input for  Confirm password  Input text  12345
    Click button  Set my password
    # Reacts with bad password
    Element should contain  css=div.field.error div.invalid-feedback  Minimum 1 capital letter.
    Input for  My user name is  Input text   rocky
    Input for  New password  Input text   ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Set my password
    Element should contain  css=div.portalMessage  Password reset successful, you are logged in now!

Test reset form
    # create the user
    Go to  ${PLONE_URL}/@@register
    Input for  User Name  Input text   rocky
    Input for  Email  Input text  rocky@balboa.com
    Input for  Password  Input text   ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Register
    Element should contain  css=h1.documentFirstHeading  Welcome
    # do a reset
    Go to  ${PLONE_URL}/mail_password_form?userid=rocky
    # DEBUG
    Wait until page contains  Lost Password
    Click button  Start password reset
    ${message_bytes} =  Get The Last Sent Email
    ${message} =  Decode Bytes To String  ${message_bytes}  utf-8
    Should contain  ${message}  plone/passwordreset
    ${reset_url} =  Extract reset url  ${message}
    # go to reset form
    Go to  ${PLONE_URL}/${reset_url}
    # Contains password description ?
    # passwordreset has different (manual) form markup than z3c-form based forms...
    Element should contain  xpath=//label[contains(., "New password")]/following::small  Minimum 1 capital letter.
    # Fill form
    Input for  My user name is  Input text  rocky
    Input for  New password  Input text  12345!
    Input for  Confirm password  Input text  12345
    Click button  Set my password
    # Reacts with bad password
    Element should contain  css=div.field.error div.invalid-feedback  Minimum 1 capital letter.
    Input for  My user name is  Input text  rocky
    Input for  New password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Click button  Set my password
    Element should contain  css=div.portalMessage  Password reset successful, you are logged in now!


*** Keywords ***

Test Setup
    Open SauceLabs test browser
    Go to  ${PLONE_URL}
    Enable autologin as  Manager
    The self registration enabled
    The mail setup configured
    Own passwords registration enabled
    ${plone_version} =  Get plone version
    Set global variable  ${plone_version}
    Disable autologin

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
    Run Keyword     ${extra_keyword}  xpath=//label[contains(., "${title}")]/following::div[@class="form-text"]   @{list}

Error for
    [arguments]     ${title}   ${extra_keyword}   @{list}
    Run Keyword     ${extra_keyword}  xpath=//label[contains(., "${title}")]/following::div[@class="invalid-feedback"]   @{list}
