#!/bin/sh

DOMAIN='PasswordStrength'

i18ndude rebuild-pot --pot ./i18n/${DOMAIN}.pot --merge ./i18n/manual.pot --create ${DOMAIN} . || exit 1
i18ndude sync --pot ./i18n/${DOMAIN}.pot ./i18n/${DOMAIN}-*.po

i18ndude rebuild-pot --pot ./i18n/plone.pot --create plone . || exit 1
i18ndude sync --pot ./i18n/plone.pot ./i18n/plone.po

WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings \(possibly missing i18n markup\)"
echo "There are $ERRORS errors \(almost definitely missing i18n markup\)"
echo "There are $FATAL fatal errors \(template could not be parsed, eg. if it\'s not html\)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or"
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir"

rm ./i18n/rebuild_i18n.log
touch ./i18n/rebuild_i18n.log

find ./ -name "*pt" | xargs i18ndude find-untranslated > ./i18n/rebuild_i18n.log
