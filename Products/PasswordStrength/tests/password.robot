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
    # Fill form
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    # Reacts with bad password
    Input text  name=form.password  12345
    Input text  name=form.password_ctl  12345
    Click button  id=form.actions.register
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element should contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords
    Element should be visible  css=#formfield-form-password_ctl .fieldErrorBox
    Element should contain  css=#formfield-form-password_ctl .fieldErrorBox  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Click button  id=form.actions.register
    Element should not be visible  css=#formfield-form-password .fieldErrorBox
    Element should not be visible  css=#formfield-form-password_ctl .fieldErrorBox
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome

Test new user form
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@new-user
    # Contains password description ?
    Element should contain  css=#formfield-form-password .formHelp  Minimum 1 capital letter.
    # Fill form
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    # Reacts with bad password
    Input text  name=form.password  12345
    Input text  name=form.password_ctl  12345
    Click button  id=form.actions.register
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element should contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords
    Element should be visible  css=#formfield-form-password_ctl .fieldErrorBox
    Element should contain  css=#formfield-form-password_ctl .fieldErrorBox  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Click button  id=form.actions.register
    Element should not be visible  css=#formfield-form-password .fieldErrorBox
    Element should not be visible  css=#formfield-form-password_ctl .fieldErrorBox
    # Redirected
    Wait until page contains  Users Overview  5
    Element should contain  css=h1.documentFirstHeading  Users Overview
    Page should contain element  css=input[value="rocky"]
    Disable autologin

Test change password form
    Test change password form

Test register form without password
    Test register form without password

Test reset form
    Test reset form

*** Keywords ***
Test Setup
    Open SauceLabs test browser
    Go to  ${PLONE_URL}
    Enable autologin as  Manager
    The self registration enabled
    The mail setup configured
    Own passwords registration enabled
    The inline validation disabled
    ${plone_version} =  Get plone version
    Set global variable  ${plone_version}
    Disable autologin
