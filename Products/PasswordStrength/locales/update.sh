domain=Products.PasswordStrength
#i18ndude rebuild-pot --pot generated.pot --create $domain ../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

#i18ndude rebuild-pot --pot plone.pot --create plone ../profiles
#i18ndude sync --pot plone.pot */LC_MESSAGES/plone.po
