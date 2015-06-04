Overrides are as follows

-                    <div class="formHelp" 
                          i18n:translate="help_new_password">
                         Enter your new password. Minimum 5 characters.
                     </div>
+                    <div class="formHelp" tal:content="python:here.portal_registration.testPasswordValidity('')"
