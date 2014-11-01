*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  Products/PasswordStrength/tests/common.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Test Setup  Test Setup
Test Teardown  Close all browsers

*** Test Cases ***

Test register form
    Go to  ${PLONE_URL}/@@register
    # Contains password description ?
    Element should contain  css=#formfield-form-password .formHelp  Minimum 1 capital letter.
    # Reacts with bad password
    Input text  name=form.password  12345
    Input text  name=form.password_ctl  12345
    Click element  css=#formfield-form-password_ctl
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element should contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords
    Element should be visible  css=#formfield-form-password_ctl .fieldErrorBox
    Element should contain  css=#formfield-form-password_ctl .fieldErrorBox  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Click element  css=#formfield-form-email
    Element should not be visible  css=#formfield-form-password .fieldErrorBox
    Element should not be visible  css=#formfield-form-password_ctl .fieldErrorBox
    # Fill form
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    Click button  id=form.actions.register
    # Redirected
    Element should contain  css=h1.documentFirstHeading  Welcome

Test new user form
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@new-user
    # Contains password description ?
    Element should contain  css=#formfield-form-password .formHelp  Minimum 1 capital letter.
    # Reacts with bad password
    Input text  name=form.password  12345
    Input text  name=form.password_ctl  12345
    Click element  css=#formfield-form-password_ctl
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element should contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords
    Element should be visible  css=#formfield-form-password_ctl .fieldErrorBox
    Element should contain  css=#formfield-form-password_ctl .fieldErrorBox  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Click element  css=#formfield-form-email
    Element should not be visible  css=#formfield-form-password .fieldErrorBox
    Element should not be visible  css=#formfield-form-password_ctl .fieldErrorBox
    # Fill form
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    Click button  id=form.actions.register
    # Redirected
    Element should contain  css=h1.documentFirstHeading  Users Overview
    Element should be visible  css=a[title=rocky]
    Disable autologin

Test change password form
    Log in  test-user  secret
    Go to  ${PLONE_URL}/@@change-password
    # Element should contain  css=h1.documentFirstHeading  Reset Password
    # use xpath locator to bypass strange travis error... 
    Element should contain  xpath=//h1[@class='documentFirstHeading']  Reset Password
    # Element should contain  css=#content .documentDescription  Change Password
    # Contains password description ?
    Element should be visible  jquery=div.formHelp:contains('Minimum 1 capital letter.')
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
    Element should contain  css=h1.documentFirstHeading  Welcome
    ${message} =  Get The Last Sent Email
    Should contain  ${message}  Your user account has been created

*** Keywords ***
Test Setup
    Open SauceLabs test browser
    Go to  ${PLONE_URL}
    Enable autologin as  Manager
    The self registration enabled
    The mail setup configured
    Own passwords registration enabled
    Disable autologin
