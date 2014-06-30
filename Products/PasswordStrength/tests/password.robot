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
    Element Should Contain  css=#formfield-form-password .formHelp  Minimum 1 capital letter.
    # Reacts with bad password
    Input text  name=form.password  12345
    Input text  name=form.password_ctl  12345
    Click element  css=#formfield-form-password_ctl
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element Should Contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords
    Element should be visible  css=#formfield-form-password_ctl .fieldErrorBox
    Element Should Contain  css=#formfield-form-password_ctl .fieldErrorBox  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input text  name=form.password  ABCDEFGHIJabcdefghij1!
    Click element  css=#formfield-form-password_ctl
    Element should not be visible  css=#formfield-form-password .fieldErrorBox
    # Fill form
    Input text  name=form.password_ctl  ABCDEFGHIJabcdefghij1!
    Input text  name=form.username  rocky
    Input text  name=form.email  rocky@balboa.com
    Click button  id=form.actions.register
    # Redirected
    Element Should Contain  css=h1.documentFirstHeading  Welcome

*** Keywords ***
Test Setup
    Open SauceLabs test browser
    Go to  ${PLONE_URL}
    Enable autologin as  Manager
    The self registration enabled
    The mail setup configured
    Own passwords registration enabled
    Disable autologin
