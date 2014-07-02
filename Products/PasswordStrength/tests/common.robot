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
