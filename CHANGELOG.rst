Changelog
=========


(unreleased)
------------

Features
~~~~~~~~
- Add ability to cancel a submitted captcha. [WereCatf]

Changes
~~~~~~~
- Use a custom exception for timeout in get_answer() [WereCatf]

  The standard exceptions are fine as-is for most situations, but a custom CaptchaError in get_answer() for timed-out captchas allows for more specific handling of such situations.
- Delete extraneous file. [WereCatf]
- Forgot to add dist to .gitignore. [WereCatf]

Documentation
~~~~~~~~~~~~~
- Update TODO and adjust gitchangelog. [WereCatf]


v0.1.0 (2021-11-21)
-------------------
- Initial commit. [WereCatf]


