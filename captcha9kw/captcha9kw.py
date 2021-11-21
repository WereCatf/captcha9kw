"""The basic business-logic of captcha9kw.
"""
import requests
from typing import Tuple, Union
import re
import base64
import filetype
import io
import validators
import pathlib
import time

errors = {
    "0001": "API key doesn't exist",
    "0002": "API key not found",
    "0003": "Active API key not found",
    "0004": "API key deactivated by owner",
    "0005": "No user found",
    "0006": "No data found",
    "0007": "No ID found",
    "0008": "No captcha found",
    "0009": "No image found",
    "0010": "Image size not allowed",
    "0011": "Balance insufficient",
    "0012": "Already done.",
    "0013": "No answer found.",
    "0014": "Captcha already answered.",
    "0015": "Captcha submitted too quickly.",
    "0016": "JD Check active.",
    "0017": "Unknown problem.",
    "0018": "No ID found.",
    "0019": "Incorrect answer.",
    "0020": "Not filed on time (wrong UserID)",
    "0021": "Link not allowed.",
    "0022": "Submit denied.",
    "0023": "Solve denied.",
    "0024": "Not enough credits.",
    "0025": "No input found.",
    "0026": "No conditions accepted.",
    "0027": "No couponcode in the database found.",
    "0028": "Already used coupon code.",
    "0029": "Maxtimeout under 60 seconds.",
    "0030": "User not found.",
    "0031": "An account is not yet 24 hours in system.",
    "0032": "An account does not have the full rights.",
    "0033": "Plugin needed a update.",
    "0034": "No HTTPS allowed.",
    "0035": "No HTTP allowed.",
    "0036": "Source not allowed.",
    "0037": "Transfer denied.",
    "0038": "Incorrect answer without space",
    "0039": "Incorrect answer with space",
    "0040": "Incorrect answer with not only numbers",
    "0041": "Incorrect answer with not only A-Z, a-z",
    "0042": "Incorrect answer with not only 0-9, A-Z, a-z",
    "0043": "Incorrect answer with not only [0-9,- ]",
    "0044": "Incorrect answer with not only [0-9A-Za-z,- ]",
    "0045": "Incorrect answer with not only coordinates",
    "0046": "Incorrect answer with not only multiple coordinates",
    "0047": "Incorrect answer with not only data",
    "0048": "Incorrect answer with not only rotate number",
    "0049": "Incorrect answer with not only text",
    "0050": "Incorrect answer with not only text and too short",
    "0051": "Incorrect answer with not enough chars",
    "0052": "Incorrect answer with too many chars",
    "0053": "Incorrect answer without no or yes",
    "0054": "Assignment was not found.",
    "0055": "IP not allowed.",
    "0056": "Limit reached",
    "0057": "Maxtimeout under 75 seconds"
}


class api9kw:
    """Class for accessing and using the 9kw.eu API.

    For any missing functionality or information, see 
    `the official API documentation`_.

    .. _the official API documentation: https://www.9kw.eu/api.html
    """
    __api_key: str = None
    __name: str = "captcha9kw"
    __session: requests.Session = None

    @property
    def account_id(self):
        """int: The ID number of the account the API key belongs to.
        """
        return int(self.__settings("id"))

    @property
    def api_key(self):
        """str: The API key for 9kw.eu services.

        The API key must be a string consisting only of characters 
        ``a-z``, ``A-Z`` and/or ``0-9``, with a minimum length of 5 
        and a maximum length of 50.
        """
        return self.__api_key

    @api_key.setter
    def api_key(self, key: str):
        if(type(key) is not str):
            raise TypeError("Incorrect type: API key must be a string.")
        if(re.fullmatch(r"[a-zA-Z\d]*", key) and len(key) >= 5 and len(key) <= 50):
            self.__api_key = key
            return None
        else:
            raise ValueError(
                "Invalid API key: minimum length is 5, maximum length is 50. Only a-z, A-Z and 0-9 allowed.")

    @property
    def balance(self):
        """int: The account's balance.
        """
        params = {"action": "usercaptchaguthaben",
                  "apikey": self.__api_key, "json": 1}
        return self.__apiGet(params)["credits"]

    @property
    def name(self):
        """str: The name this software should identify itself as to 
        the services.

        Parameter ``source`` in the `the official API documentation`_, 
        defaults to ``captcha9kw``. Must be in the range of 5 to 30 
        characters long.
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        if(type(name) is not str):
            raise TypeError("Incorrect type: name must be a string.")
        if(len(name) > 30):
            raise ValueError("Name too long. Maximum length is 30 characters.")
        self.__name = name

    @property
    def referrals(self):
        """list: The account's list of referrals.
        """
        params = {"action": "userconfigref",
                  "json": 1, "apikey": self.__api_key, "source": self.__name}
        return self.__apiGet(params)["refs"]

    @property
    def referrals_archived(self):
        """list: The account's list of referrals, including archived 
        ones.
        """
        params = {"action": "userconfigref",
                  "json": 1, "apikey": self.__api_key, "source": self.__name, "archiv": 1}
        return self.__apiGet(params)["refs"]

    @property
    def selfonly(self):
        """int: Corresponds to `selfonly` in account settings.

        With `selfonly` enabled the account the API key belongs to will 
        only receive that account's own submitted captchas, not from 
        other accounts.
        """
        return int(self.__settings("selfonly"))

    @selfonly.setter
    def selfonly(self, value: int):
        if(type(value) not in [bool, int]):
            raise TypeError("Argument is not an int.")
        if(value not in [0, 1]):
            raise ValueError("Argument value out of range (0 to 1).")
        self.__settings("selfonly", int(value))

    @property
    def selfsend(self):
        """int: Corresponds to `selfsend` in account settings.
        """
        return int(self.__settings("selfsend"))

    @selfsend.setter
    def selfsend(self, value: int):
        if(type(value) not in [bool, int]):
            raise TypeError("Argument is not an int.")
        if(value not in [0, 1]):
            raise ValueError("Argument value out of range (0 to 1).")
        self.__settings("selfsend", int(value))

    @property
    def selfsolve(self):
        """int: Corresponds to `selfsolve` in account settings.

        With `selfsolve` enabled both in account settings and the 
        submitted captcha, only the account the API key belongs to will 
        get to solve their submitted captchas; the captchas will not be 
        sent to other accounts to be solved. The account will continue 
        to also receive captchas from other accounts.

        Note
        ----
            `selfsolve` must be enabled for both the account and the 
            submitted captcha or else the setting will be ignored by 
            the service.
        """
        return int(self.__settings("selfsolve"))

    @selfsolve.setter
    def selfsolve(self, value: int):
        if(type(value) not in [bool, int]):
            raise TypeError("Argument is not an int.")
        if(value not in [0, 1]):
            raise ValueError("Argument value out of range (0 to 1).")
        self.__settings("selfsolve", int(value))

    @property
    def settings(self):
        """dict: All the account-related settings.
        """
        return self.__settings()

    @property
    def service_status(self):
        """dict: Information about the service's status.
        """
        results = requests.get(
            "https://www.9kw.eu/grafik/servercheck.json", timeout=(5, 3))
        if(results.status_code == 200):
            return results.json()
        else:
            raise RuntimeError(
                f"Connection error: {results.status_code}, '{results.reason}'.")

    @property
    def source(self):
        """str: The name this software should identify itself as to 
        the services.

        Parameter ``source`` in the `the official API documentation`_, 
        defaults to ``captcha9kw``. Must be in the range of 5 to 30 
        characters long.
        """
        return self.__name

    @source.setter
    def source(self, name: str):
        if(type(name) is not str):
            raise TypeError("Incorrect type: The name must be a string.")
        if(len(name) > 30):
            raise ValueError(
                "Name too long. The maximum length is 30 characters.")
        self.__name = name

    def __apiGet(self, params, session=None):
        if(not self.__api_key):
            raise ValueError("API key has not been set.")
        for key in params:
            if(type(key) is bool):
                params[key] = int(params[key])
        if(not session):
            if(self.__session):
                session = self.__session
            else:
                session = requests
        results = session.get("https://www.9kw.eu/index.cgi",
                              params=params, timeout=(5, 3))
        if(results.status_code == 200):
            try:
                contents = results.json()
            except:
                errCode = results.content.decode('utf-8').split(" ", 1)[0]
                raise RuntimeError(
                    f"Server error: '{errors[errCode]}'")
            if(contents["status"]["success"]):
                return contents
            else:
                raise RuntimeError(f"Server error: '{contents['error']}'")
        else:
            raise RuntimeError(
                f"Connection error: {results.status_code}, '{results.reason}'.")

    def __apiPost(self, params, files, session=None):
        if(not self.__api_key):
            raise ValueError("API key has not been set.")
        for key in params:
            if(type(key) is bool):
                params[key] = int(params[key])
        if(not session):
            if(self.__session):
                session = self.__session
            else:
                session = requests
        results = session.post("https://www.9kw.eu/index.cgi",
                               params=params, files=files, timeout=(5, 3))
        if(results.status_code == 200):
            try:
                contents = results.json()
            except:
                errCode = results.content.decode('utf-8').split(" ", 1)[0]
                raise RuntimeError(
                    f"Server error: '{errors[errCode]}'")
            if(contents["status"]["success"]):
                return contents
            else:
                raise RuntimeError(f"Server error: '{contents['error']}'")
        else:
            raise RuntimeError(
                f"Connection error: {results.status_code}, '{results.reason}'.")

    def __settings(self, key=None, value=None):
        if(key is None):
            params = {"action": "userconfig",
                      "apikey": self.__api_key, "json": 1}
            return self.__apiGet(params)
        else:
            if(value is None):
                params = {"action": "userconfig",
                          "apikey": self.__api_key, "json": 1}
                return self.__apiGet(params)[key]
            params = {"action": f"userconfig{key}",
                      "apikey": self.__api_key, "json": 1, key: value}
            self.__apiGet(params)

    def captcha_details(self, id: int, archive: int = 0) -> dict:
        """Query for details on a submitted captcha.

        Parameters
        ----------
        id : int
            ID of the captcha to query details for.
        archive : int, default 0
            Access an archived captcha.

        Returns
        -------
        dict
            A dictionary containing the results.
        """
        params = {"action": "userhistorydetail", "json": 1,
                  "apikey": self.__api_key, "id": id, "archiv": archive}
        return self.__apiGet(params)

    def captcha_feedback_correct(self, id: int, archive: int = 0):
        """Mark the answer for the captcha as correct.

        Note
        ----
            It's good manners to report as to whether the answer was 
            correct or not.

        Parameters
        ----------
        id : int
            ID of the captcha.
        archive : int, default 0
            Access an archived captcha.
        """
        params = {"action": "usercaptchacorrectback", "json": 1,
                  "id": id, "archiv": archive, "apikey": self.__api_key, "correct": 1, "source": self.__name}
        self.__apiGet(params)

    def captcha_feedback_incorrect(self, id: int, archive: int = 0):
        """Mark the answer for the captcha as incorrect.

        Note
        ----
            It's good manners to report as to whether the answer was 
            correct or not.

        Parameters
        ----------
        id : int
            ID of the captcha.
        archive : int, default 0
            Access an archived captcha.
        """
        params = {"action": "usercaptchacorrectback", "json": 1,
                  "id": id, "archiv": archive, "apikey": self.__api_key, "correct": 2, "source": self.__name}
        self.__apiGet(params)

    def captchas_failed(self, archive: int = 0, page: int = 0, onlyapikey: int = 0) -> dict:
        """Query the list of failed or incorrect captchas associated 
        with the account.

        Parameters
        ----------
        archive : int, default 0
            Whether to include results from the archives.
        page : int, default 0
            Desired page number. A page can have up to 10 results.
        onlyapikey : int, default 0
            Return matches only for the API key currently in use.

        Returns
        -------
        dict
            A dictionary with the results.
        """
        params = {"action": "userhistory3",
                  "json": 1, "apikey": self.__api_key, "archiv": archive, "page": page, "onlyapikey": onlyapikey}
        return self.__apiGet(params)

    def captchas_solved(self, source: str = None, correctsource: str = None, archive: int = 0, filter: str = None, confirm: int = 0, page: int = 0, onlyapikey: int = 0) -> dict:
        """Query the list of captchas solved by the account.

        Parameters
        ----------
        source : str or None, default None
            Indicates the name of the software used (e.g. 
            ``phpapi``) by the submitter.
        correctsource : str or None, default None
            Indicates the name of the software used (e.g. 
            ``9kwclient``) by the solver.
        archive : int, default 0
            Include results from the archives.
        filter : str or None, default None

            - ``ok`` - Only entries with OK.
            - ``notok`` - Only entries with NotOK.
            - ``both`` - Only entries with OK or NotOK.
            - ``other`` - Only entries without OK or NotOK.

        confirm : int, default 0
            Only captchas with the confirm option enabled.
        page : int, default 0
            Desired page number. A page can have up to 10 results.
        onlyapikey : int, default 0
            Return matches only for the API key currently in use.

        Returns
        -------
        dict
            A dictionary with the results.
        """
        params = {"action": "userhistory2",
                  "json": 1, "apikey": self.__api_key}
        for x in ["source", "correctsource", "archive", "filter", "confirm", "onlyapikey", "page"]:
            if(locals()[x] is not None):
                if(x == "archive"):
                    params["archiv"] = locals()[x]
                else:
                    params[x] = locals()[x]
        return self.__apiGet(params)

    def captchas_submitted(self, source: str = None, correctsource: str = None, archiv: int = 0, filter: str = None, page: int = 0, onlyapikey: int = 0) -> dict:
        """Query the captchas submitted by the account to the service.

        Parameters
        ----------
        source : str or None, default None
            Indicates the name of the software used (e.g. 
            ``phpapi``) by the submitter.
        correctsource : str or None, default None
            Indicates the name of the software used (e.g. 
            ``9kwclient``) by the solver.
        archive : int, default 0
            Include results from the archives.
        filter : str or None, default None

            - ``ok`` - Only entries with OK.
            - ``notok`` - Only entries with NotOK.
            - ``both`` - Only entries with OK or NotOK.
            - ``other`` - Only entries without OK or NotOK.

        page : int, default None
            Desired page number.
        onlyapikey : int, default 0
            Return matches only for the API key currently in use. 

        Returns
        -------
        dict
            A dictionary with the results.
        """
        params = {"action": "userhistory", "json": 1, "apikey": self.__api_key}
        for x in ["source", "correctsource", "archive", "filter", "page", "onlyapikey"]:
            if(locals()[x] is not None):
                if(x == "archive"):
                    params["archiv"] = locals()[x]
                else:
                    params[x] = locals()[x]
        return self.__apiGet(params)

    def create_account(self, credits: int, referrer: Union[int, str] = None) -> Tuple[str, str]:
        """Create a new account while also transferring some credits 
        to it.

        Parameters
        ----------
        credits : int
            The amount of credits to transfer with a minimum 40000, 
            or a coupon code.
        referrer: int or str, default None
            The ID of the account to set as the referrer for the new one.

        Returns
        -------
        Tuple
            A tuple of the new account's username and password.
        """
        params = {"action": "anmelden2_create",
                  "json": 1, "apikey": self.__api_key, "source": self.__name, "code": credits}
        if(referrer is not None):
            params["ref"] = str(referrer)
        results = self.__apiGet(params)
        return (results["newuser"], results["newpass"])

    def create_coupon(self, credits: int) -> str:
        """Create a coupon code of credits from the account's balance.

        Parameters
        ----------
        credits : int
            How many credits to allocate to the coupon with a minimum 
            of 1000 credits.

        Returns
        -------
        str
            The coupon code as a string.
        """
        params = {"action": "usergutscheincreate",
                  "json": 1, "apikey": self.__api_key, "source": self.__name, "guthaben": credits}
        return self.__apiGet(params)["code"]

    def get_answer(self, id: int, archive: int = 0, wait: int = 0) -> str:
        """Check for and receive the answer to a captcha.

        Note
        ----
            If checking for the answer manually, you should wait at 
            least 5-10 seconds after submitting a captcha before 
            attempting to receive the answer for it. If the answer 
            isn't yet available, wait for a few seconds longer and try 
            again.

        Parameters
        ----------
        id : int
            ID of the submitted captcha.
        archive : int, default 0
            Whether to access an archived captcha.
        wait: int, default 0
            Whether to wait until the captcha is resolved or an error 
            is received.

        Returns
        -------
        str
            The answer or a zero-length string, if the answer is not 
            yet available.
        """
        params = {"action": "usercaptchacorrectdata", "json": 1,
                  "id": id, "archiv": archive, "apikey": self.__api_key, "source": self.__name}
        with requests.Session() as session:
            if(wait):
                time.sleep(5)
                while True:
                    results = self.__apiGet(params, session)
                    if("answer" in results and results["answer"]):
                        return results["answer"]
                    if("try_again" in results and not results["try_again"]):
                        raise RuntimeError(
                            "Server tells us not to try querying for the captcha again.")
                    if("timeout" in results and results["timeout"]):
                        raise RuntimeError(
                            "Timeout waiting for answer to captcha.")
                    time.sleep(2)
            else:
                results = self.__apiGet(params, session)
                if("answer" in results):
                    return results["answer"]
                else:
                    return ""

    def submit_image_captcha(self, data: Union[str, io.BufferedReader], maxtimeout: int = 600, prio: int = 0, confirm: int = 0, selfsolve: int = 0, nomd5: int = 0, ocr: int = 0, debug: int = 0) -> int:
        """Submit an image-based captcha.

        Parameters
        ----------
        data : str or io.BufferedReader
            The image data to be submitted. Can be a fully-qualified 
            URL (ie. must include ``https://`` or similar protocol 
            identifier), a filename or an open, seekable file.
        maxtimeout : int, default 600
            Maximum timeout in range of 60 to 3999 seconds.
        prio : int, default 0
            Priority for the submitted captcha from 1 to 20. Also 
            increases credit cost by the same amount.
        confirm : int, default 0
            Have the answer double-checked by another account. 
            Increases credit cost by 6. Will be ignored, if maximum 
            timeout is set at less than 150 seconds.
        selfsolve : int, default 0
            The captcha will only be solveable by the account the API 
            key belongs to.
        nomd5 : int, default 0
            Disable using MD5 of the submitted data to check for 
            duplicates.
        ocr : int, default 0
            Intended for future automatic recognition. This option is 
            currently not supported and will be ignored.
        debug : int, default 0
            Enables a testing environment to check the system without 
            using a sandbox. It's limited.

        Returns
        -------
        int
            ID of the submission.
        """
        results = None
        if(type(data) is io.BufferedReader):
            data.seek(0)
            results = data.read()
        elif(type(data) is str):
            if(validators.url(data)):
                results = requests.get(
                    data, allow_redirects=True, timeout=(5, 3))
                if(results.status_code != 200):
                    raise RuntimeError(
                        f"Error downloading image from given URL ('{data}')")
                results = results.content
            elif(pathlib.Path(data).is_file()):
                with open(data, "rb") as file:
                    results = file.read()
            else:
                results = base64.b64decode(data)
        if(not filetype.guess(results) or not filetype.guess(results).mime.startswith("image/")):
            raise ValueError("Submitted data is not an image.")
        params = {"action": "usercaptchaupload", "base64": 0, "json": 1,
                  "maxtimeout": maxtimeout, "prio": prio, "selfsolve": selfsolve, "confirm": confirm, "apikey": self.__api_key, "nomd5": nomd5, "source": self.__name, "ocr": ocr, "debug": debug}
        files = {"file-upload-01": results}
        return int(self.__apiPost(params, files)["captchaid"])

    def submit_interactive_captcha(self, sitekey: str, pageurl: str = None, captchatype: str = None, cookies: str = None, useragent: str = None, maxtimeout: int = 600, prio: int = 0, selfsolve: int = 0, confirm: int = 0, debug: int = 0):
        """Submit an interactive captcha, like e.g. reCaptcha V2.

        Parameters
        ----------
        sitekey : str
            The site's captcha key, ie. the ID of the captcha on the 
            site.
        pageurl: str, default None
            The URL of the site. Depends on the site and captcha in 
            question as to whether this is required.
        captchatype : str, default None
            The type of the captcha being submitted (e.g. recaptchav2, 
            recaptchav3, funcaptcha, geetest, hcaptcha, keycaptcha) 
        cookies: str, default None
            If solving the captcha requires using cookies, set them 
            here.
        useragent: str, default None
            If solving the captcha requires a specific user-agent, set 
            that here.
        maxtimeout : int, default 600
            Maximum timeout in range of 60 to 3999 seconds.
        prio : int, default 0
            Priority for the submitted captcha from 1 to 20. Also 
            increases credit cost by the same amount.
        selfsolve : int, default 0
            The captcha will only be solveable by the account the API 
            key belongs to.
        confirm : int, default 0
            Have the answer double-checked by another account. 
            Increases credit cost by 6. Will be ignored, if maximum 
            timeout is set at less than 150 seconds.
        debug : int, default 0
            Enables a testing environment to check the system without 
            using a sandbox. It's limited.

        Returns
        -------
        int
            ID of the submission.
        """
        params = {"action": "usercaptchaupload", "json": 1, "maxtimeout": maxtimeout,
                  "prio": prio, "selfsolve": selfsolve, "confirm": confirm, "apikey": self.__api_key, "interactive": 1, "source": self.__name}
        files = {"file-upload-01": sitekey}
        if(captchatype):
            params["oldsource"] = captchatype
        for x in ["cookies", "useragent", "pageurl", "debug"]:
            if(locals()[x] is not None):
                params[x] = locals()[x]
        return int(self.__apiPost(params, files)["captchaid"])

    def transfer_credits(self, credits: int, userid: int, transferart: int = 1) -> int:
        """Transfer credits to another account.

        Parameters
        ----------
        credits : int
            The amount of credits to transfer with a minimum of 1000 
            credits.
        userid : int
            The ID of the account to transfer to.
        transferart : int, default 1
            What to transfer:

             1. Credits
             2. Also includes values from the bonus program.

        Returns
        -------
        int
            The ID of the transaction.
        """
        params = {"action": "usertransfer",
                  "json": 1, "apikey": self.__api_key, "source": self.__name, "guthaben": credits, "userid": userid, "transferart": transferart}
        return int(self.__apiGet(params)["transferid"])
