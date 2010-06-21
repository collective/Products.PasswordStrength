Overrides are as follows

--- a/CMFPlone/branches/2.5/skins/plone_login/join_form.cpt
+++ b/Products/PasswordStrength/skins/PasswordStrength_public/join_form.cpt
@@ -141,8 +141,7 @@
               i18n:attributes="title title_required;"
               i18n:translate="label_required">(Required)</span>
 
+              <div class="formHelp" 
+                  tal:content="python:here.portal_registration.testPasswordValidity(' ')">
-              <div class="formHelp" i18n:translate="help_password_creation">
                 Minimum 5 characters.
               </div>

--- a//CMFPlone/branches/2.5/skins/plone_prefs/password_form.pt
+++ b/Products/PasswordStrength/skins/PasswordStrength_public/password_form.pt
@@ -48,7 +48,7 @@
             <div class="field">
                 <label for="password" i18n:translate="label_new_password">New password</label>
 
+                <div class="formHelp" tal:content="python:here.portal_registration.testPasswordValidity(' ')"> 
-                <div class="formHelp" i18n:translate="help_new_password">


--- a/Products/PasswordResetTool/tags/1.0/skins/PasswordReset/pwreset_form.cpt
+++ b/Products/PasswordStrength/skins/PasswordStrength_public/pwreset_form.cpt
@@ -55,7 +54,7 @@
                            i18n:translate="label_new_password">New password</label>
                           <div tal:content="error">Validation error output</div>
 
-                    <div class="formHelp" tal:content="python:here.portal_registration.testPasswordValidity(' ')"
+                    <div class="formHelp" 
                          i18n:translate="help_new_password">
                         Enter your new password. Minimum 5 characters.
                     </div>


join_form_validate.vpy

+       # Altered so testPasswordValidity can be used instead
+     if not state.getError('password'):
+        error = context.portal_registration.testPasswordValidity(password, password_confirm)
+        if error:
+                        state.setError('password', error)
+                        state.setError('password_confirm', error)
-     if not state.getError('password') and len(password) < 5:
-         minlimit('password')
-         minlimit('password_confirm')

