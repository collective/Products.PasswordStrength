*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

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
    # Wait until page contains  Add New Uer  20
    Scroll To Element  css=#form-widgets-password
    Input for  Password  Input text    12345
    Scroll To Element  css=#form-widgets-password_ctl
    Input for  Confirm password  Input text  12345
    Scroll To Element  css=#form-buttons-register
    Click Button  Register
    Error for  Password  Element should be visible
    Error for  Password  Element should contain   This password doesn't match requirements for passwords
    Error for  Confirm password  Element should be visible
    Error for  Confirm password  Element should contain  This password doesn't match requirements for passwords
    # Accepts well formed password
    Input for  Password  Input text  ABCDEFGHIJabcdefghij1!
    Input for  Confirm password  Input text  ABCDEFGHIJabcdefghij1!
    Scroll To Element  css=#form-buttons-register
    Click Button  Register
    Error for  Password  Element should not be visible
    Error for  Confirm password  Element should not be visible
    # Redirected
    Wait until page contains  Welcome  5
    Element should contain  css=h1.documentFirstHeading  Welcome


*** Keywords ***

Scroll To Element
    [Arguments]  ${locator}
    ${x}=        Get Horizontal Position  ${locator}
    ${y}=        Get Vertical Position    ${locator}
    Execute Javascript  window.scrollTo(${x}, ${y})

Test Setup
    Open test browser
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
    Scroll To Element  css=#form-buttons-save
    Click Button  Save
    Input for  Let users select their own passwords  Checkbox should be selected
    Disable autologin

Own passwords registration disabled
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@security-controlpanel
    Input for  Let users select their own passwords  Unselect checkbox
    Scroll To Element  css=#form-buttons-save
    Click Button  Save
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
