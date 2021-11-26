.. _api-reference:


API Reference
*************

**class captcha9kw.api9kw**

   Class for accessing and using the 9kw.eu API.

   For any missing functionality or information, see `the official API
   documentation <https://www.9kw.eu/api.html>`_.

   ``property account_id``

      The ID number of the account the API key belongs to.

      :Type:
         int

   ``property api_key``

      The API key for 9kw.eu services.

      The API key must be a string consisting only of characters
      ``a-z``, ``A-Z`` and/or ``0-9``, with a minimum length of 5 and
      a maximum length of 50.

      :Type:
         str

   ``property balance``

      The account’s balance.

      :Type:
         int

   ``property name``

      The name this software should identify itself as to the
      services.

      Parameter ``source`` in the `the official API documentation
      <https://www.9kw.eu/api.html>`_, defaults to ``captcha9kw``.
      Must be in the range of 5 to 30 characters long.

      :Type:
         str

   ``property referrals``

      The account’s list of referrals.

      :Type:
         list

   ``property referrals_archived``

      The account’s list of referrals, including archived ones.

      :Type:
         list

   ``property selfonly``

      Corresponds to *selfonly* in account settings.

      With *selfonly* enabled the account the API key belongs to will
      only receive that account’s own submitted captchas, not from
      other accounts.

      :Type:
         int

   ``property selfsend``

      Corresponds to *selfsend* in account settings.

      :Type:
         int

   ``property selfsolve``

      Corresponds to *selfsolve* in account settings.

      With *selfsolve* enabled both in account settings and the
      submitted captcha, only the account the API key belongs to will
      get to solve their submitted captchas; the captchas will not be
      sent to other accounts to be solved. The account will continue
      to also receive captchas from other accounts.

      Note: *selfsolve* must be enabled for both the account and the
         submitted captcha or else the setting will be ignored by the
         service.

      :Type:
         int

   ``property settings``

      All the account-related settings.

      :Type:
         dict

   ``property service_status``

      Information about the service’s status.

      :Type:
         dict

   ``property source``

      The name this software should identify itself as to the
      services.

      Parameter ``source`` in the `the official API documentation
      <https://www.9kw.eu/api.html>`_, defaults to ``captcha9kw``.
      Must be in the range of 5 to 30 characters long.

      :Type:
         str

   **captcha_cancel_submitted(id: int)**

      Cancel the already-submitted captcha.

      :Parameters:
         **id** (*int*) – ID of the captcha.

   **captcha_details(id: int, archive: int = 0) -> dict**

      Query for details on a submitted captcha.

      :Parameters:
         *  **id** (*int*) – ID of the captcha to query details for.

         *  **archive** (*int**, **default 0*) – Access an archived
            captcha.

      :Returns:
         A dictionary containing the results.

      :Return type:
         dict

   **captcha_feedback_correct(id: int, archive: int = 0)**

      Mark the answer for the captcha as correct.

      Note: It’s good manners to report as to whether the answer was
         correct or not.

      :Parameters:
         *  **id** (*int*) – ID of the captcha.

         *  **archive** (*int**, **default 0*) – Access an archived
            captcha.

   **captcha_feedback_incorrect(id: int, archive: int = 0)**

      Mark the answer for the captcha as incorrect.

      Note: It’s good manners to report as to whether the answer was
         correct or not.

      :Parameters:
         *  **id** (*int*) – ID of the captcha.

         *  **archive** (*int**, **default 0*) – Access an archived
            captcha.

   **captchas_failed(archive: int = 0, page: int = 0, onlyapikey: int
   = 0) -> dict**

      Query the list of failed or incorrect captchas associated with
      the account.

      :Parameters:
         *  **archive** (*int**, **default 0*) – Whether to include
            results from the archives.

         *  **page** (*int**, **default 0*) – Desired page number. A
            page can have up to 10 results.

         *  **onlyapikey** (*int**, **default 0*) – Return matches
            only for the API key currently in use.

      :Returns:
         A dictionary with the results.

      :Return type:
         dict

   **captchas_solved(source: Optional[str] = None, correctsource:
   Optional[str] = None, archive: int = 0, filter: Optional[str] =
   None, confirm: int = 0, page: int = 0, onlyapikey: int = 0) ->
   dict**

      Query the list of captchas solved by the account.

      :Parameters:
         *  **source** (*str** or **None**, **default None*) –
            Indicates the name of the software used (e.g. ``phpapi``)
            by the submitter.

         *  **correctsource** (*str** or **None**, **default None*) –
            Indicates the name of the software used (e.g.
            ``9kwclient``) by the solver.

         *  **archive** (*int**, **default 0*) – Include results from
            the archives.

         *  **filter** (*str** or **None**, **default None*) –

            *  ``ok`` - Only entries with OK.

            *  ``notok`` - Only entries with NotOK.

            *  ``both`` - Only entries with OK or NotOK.

            *  ``other`` - Only entries without OK or NotOK.

         *  **confirm** (*int**, **default 0*) – Only captchas with
            the confirm option enabled.

         *  **page** (*int**, **default 0*) – Desired page number. A
            page can have up to 10 results.

         *  **onlyapikey** (*int**, **default 0*) – Return matches
            only for the API key currently in use.

      :Returns:
         A dictionary with the results.

      :Return type:
         dict

   **captchas_submitted(source: Optional[str] = None, correctsource:
   Optional[str] = None, archiv: int = 0, filter: Optional[str] =
   None, page: int = 0, onlyapikey: int = 0) -> dict**

      Query the captchas submitted by the account to the service.

      :Parameters:
         *  **source** (*str** or **None**, **default None*) –
            Indicates the name of the software used (e.g. ``phpapi``)
            by the submitter.

         *  **correctsource** (*str** or **None**, **default None*) –
            Indicates the name of the software used (e.g.
            ``9kwclient``) by the solver.

         *  **archive** (*int**, **default 0*) – Include results from
            the archives.

         *  **filter** (*str** or **None**, **default None*) –

            *  ``ok`` - Only entries with OK.

            *  ``notok`` - Only entries with NotOK.

            *  ``both`` - Only entries with OK or NotOK.

            *  ``other`` - Only entries without OK or NotOK.

         *  **page** (*int**, **default None*) – Desired page number.

         *  **onlyapikey** (*int**, **default 0*) – Return matches
            only for the API key currently in use.

      :Returns:
         A dictionary with the results.

      :Return type:
         dict

   **create_account(credits: int, referrer: Optional[Union[int, str]]
   = None) -> Tuple[str, str]**

      Create a new account while also transferring some credits to it.

      :Parameters:
         *  **credits** (*int*) – The amount of credits to transfer
            with a minimum 40000, or a coupon code.

         *  **referrer** (*int** or **str**, **default None*) – The ID
            of the account to set as the referrer for the new one.

      :Returns:
         A tuple of the new account’s username and password.

      :Return type:
         Tuple

   **create_coupon(credits: int) -> str**

      Create a coupon code of credits from the account’s balance.

      :Parameters:
         **credits** (*int*) – How many credits to allocate to the
         coupon with a minimum of 1000 credits.

      :Returns:
         The coupon code as a string.

      :Return type:
         str

   **get_answer(id: int, archive: int = 0, wait: int = 0) -> str**

      Check for and receive the answer to a captcha.

      Note: If checking for the answer manually, you should wait at least
         5-10 seconds after submitting a captcha before attempting to
         receive the answer for it. If the answer isn’t yet available,
         wait for a few seconds longer and try again.

      :Parameters:
         *  **id** (*int*) – ID of the submitted captcha.

         *  **archive** (*int**, **default 0*) – Whether to access an
            archived captcha.

         *  **wait** (*int**, **default 0*) – Whether to wait until
            the captcha is resolved or an error is received.

      :Returns:
         The answer or a zero-length string, if the answer is not yet
         available.

      :Return type:
         str

      :Raises:
         **CaptchaError** – Raised when a successfully submitted,
         active captcha times     out or encounters an other error.

   **submit_image_captcha(data: Union[str, _io.BufferedReader],
   maxtimeout: int = 600, prio: int = 0, confirm: int = 0, selfsolve:
   int = 0, nomd5: int = 0, ocr: int = 0, debug: int = 0) -> int**

      Submit an image-based captcha.

      :Parameters:
         *  **data** (*str** or **io.BufferedReader*) – The image data
            to be submitted. Can be a fully-qualified URL (ie. must
            include ``https://`` or similar protocol identifier), a
            filename or an open, seekable file.

         *  **maxtimeout** (*int**, **default 600*) – Maximum timeout
            in range of 60 to 3999 seconds.

         *  **prio** (*int**, **default 0*) – Priority for the
            submitted captcha from 1 to 20. Also increases credit cost
            by the same amount.

         *  **confirm** (*int**, **default 0*) – Have the answer
            double-checked by another account. Increases credit cost
            by 6. Will be ignored, if maximum timeout is set at less
            than 150 seconds.

         *  **selfsolve** (*int**, **default 0*) – The captcha will
            only be solveable by the account the API key belongs to.

         *  **nomd5** (*int**, **default 0*) – Disable using MD5 of
            the submitted data to check for duplicates.

         *  **ocr** (*int**, **default 0*) – Intended for future
            automatic recognition. This option is currently not
            supported and will be ignored.

         *  **debug** (*int**, **default 0*) – Enables a testing
            environment to check the system without using a sandbox.
            It’s limited.

      :Returns:
         ID of the submission.

      :Return type:
         int

   **submit_interactive_captcha(sitekey: str, pageurl: Optional[str] =
   None, captchatype: Optional[str] = None, cookies: Optional[str] =
   None, useragent: Optional[str] = None, maxtimeout: int = 600, prio:
   int = 0, selfsolve: int = 0, confirm: int = 0, debug: int = 0)**

      Submit an interactive captcha, like e.g. reCaptcha V2.

      :Parameters:
         *  **sitekey** (*str*) – The site’s captcha key, ie. the ID
            of the captcha on the site.

         *  **pageurl** (*str**, **default None*) – The URL of the
            site. Depends on the site and captcha in question as to
            whether this is required.

         *  **captchatype** (*str**, **default None*) – The type of
            the captcha being submitted (e.g. recaptchav2,
            recaptchav3, funcaptcha, geetest, hcaptcha, keycaptcha)

         *  **cookies** (*str**, **default None*) – If solving the
            captcha requires using cookies, set them here.

         *  **useragent** (*str**, **default None*) – If solving the
            captcha requires a specific user-agent, set that here.

         *  **maxtimeout** (*int**, **default 600*) – Maximum timeout
            in range of 60 to 3999 seconds.

         *  **prio** (*int**, **default 0*) – Priority for the
            submitted captcha from 1 to 20. Also increases credit cost
            by the same amount.

         *  **selfsolve** (*int**, **default 0*) – The captcha will
            only be solveable by the account the API key belongs to.

         *  **confirm** (*int**, **default 0*) – Have the answer
            double-checked by another account. Increases credit cost
            by 6. Will be ignored, if maximum timeout is set at less
            than 150 seconds.

         *  **debug** (*int**, **default 0*) – Enables a testing
            environment to check the system without using a sandbox.
            It’s limited.

      :Returns:
         ID of the submission.

      :Return type:
         int

   **transfer_credits(credits: int, userid: int, transferart: int = 1)
   -> int**

      Transfer credits to another account.

      :Parameters:
         *  **credits** (*int*) – The amount of credits to transfer
            with a minimum of 1000 credits.

         *  **userid** (*int*) – The ID of the account to transfer to.

         *  **transferart** (*int**, **default 1*) –

            What to transfer:

               1. Credits

               2. Also includes values from the bonus program.

      :Returns:
         The ID of the transaction.

      :Return type:
         int
