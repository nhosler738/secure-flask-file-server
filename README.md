Author: Nathan Hosler
Date Created: 07/11/2025


To do:
    - login system (works)
    - file upload system (works)
    - file download system (works)
    - file encryption system 



About: A simple flask file server where files can be securely uploaded and downloaded from.

Login System:
    - User enters the shared server-key into the login page -> Browser session created 
    - The flask apps designated secret key will be used to cryptographically sign mainly cookies and session data
        - Whenever flask stores information on the client-side, it signs that data using the secret key to prevent tampering 
        - Flask can verify that the session cookie is authentic 

    Flask sessions are turned to "temporary" = they last only as long as the browser tab/window is open
    Session data is also stored on the disk (server) instead of in cookies (on clients browser)
        - Data is not exposed to the client (more secure)







