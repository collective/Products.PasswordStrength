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

Test if register form contains password description
    Go to  ${PLONE_URL}/@@register
    Element Should Contain  css=#formfield-form-password .formHelp  Minimum 1 capital letter.

Test if register form validates inline
    Go to  ${PLONE_URL}/@@register
    Input text  name=form.password  12345
    Click element  css=#formfield-form-password_ctl
    Element should be visible  css=#formfield-form-password .fieldErrorBox
    Element Should Contain  css=#formfield-form-password .fieldErrorBox  This password doesn't match requirements for passwords


*** Keywords ***
Test Setup
    Open SauceLabs test browser
    Go to  ${PLONE_URL}
    Enable autologin as  Manager
    The self registration enabled
    The mail setup configured
    Own passwords registration enabled
    Disable autologin
