# SavonPython


### This is a work in progress!


The purpose of this app is to automate the clipping of all coupons that are available to you on the vons.com website.  The process for a human to do this is as follows:

1) Open vons.com website (or handheld app).
2) Log on to website.
   1) Enter username or phone number
   2) Enter one time passcode, or optionally choose to use a password.
      (Handheld app has no option for using a passcode)
   3) Locate available coupons
   4) Click each available coupon one at a time, waiting for page to refresh between clicks

The challenge is that new coupons are added all the time, and the sheer quantity makes clipping all coupons a significant time investment.  If you only clipped coupons as needed, you might miss discounts that you would receive if you clipped all coupons.

I'd estimate that anyone dedicated to clipping all coupons before grocery shopping to spend at least a half hour each week.  Since I know that I either wont remember to do this each week, or wont be willing to spend that time, I instead dedicated 40 hours in to writing an app that does this for you.  The math works damnit!

#### Challenges

Like most modern website, vons.com implements some tools to detect non human interactions.  And the heavy javascript interface would be rather difficult for automation to go through the process a human would do.  In working through this build I determined that vons.com uses an enterprise solution called Incapsula.  Incapsula works as follows:

1) Checks the headers for all requests to see if there is a liklihood that the request was recived through automation.
2) Requires a javascript interpreter (a web browser) to run js that is generated for the session.
3) Javascript has the following parameters:
   1) Has a var b value that is a long hexadecimal string.
   2) Contains a function to decode the var b
   3) decoded hex is another js.
   4) immediately executes decoded js.
   5) js is a highly obfuscated bit of code that:
      1) sets initial cookies in browser
      2) launches an iframe (not visible to user) that calls a sub url of vons.com, which confirms that the js process completed.
      3) sets permanent cookies in browser to validate that the browser session has been confirmed to be human.
4) Initiates a call to Okta to set a session cookie.

This all occurs when first loading the web page, and before a user has set any site settings, or attempted to logon.  There are several other cookies that are set for google captcha, doubleclick, etc.  However, they are not needed.  Once a user chooses to sign in, an api call is made that delivers the user/phone info.  Then when either a one time code, or password is entered, it makes another api call to deliver that info, and then generates another call to okta.  This process sets additional cookies to identify the authenticated user.  There are regular calls to okta to refresh these cookies throughout the session.

#### What this tool does

Although I had written my own tools to do some of the js interpretation, I found the incap_cracker_py3 library towards the end, and found they had generally resolved the hurdles I couldnt overcome.  I have copied the needed scripts in to this app.  Credit to them for that code.
https://github.com/ziplokk1/incapsula-cracker-py3/tree/master

Using the incapsula library, a new requests session is generated.  This session is wrapped with some tools that identify the incapsula url/js files, and interprets what they would otherwise do within the iframe of your browser.  This makes it so the session can collect the needed cookies to browse vons.com.  The get_session_cookies script runs through the entire flow that is necessary to log on to vons.com with your email address and password.  With that completed, it then makes an api call to find all of the coupons available to your account.  It then parses to coupons that are not yet clipped.  And finally it clips each coupon.

## One important note.  Even though it uses a password, vons.com defaults to a one time passcode.  So every time this runs, you will get an OTP email from vons.

## The core components of this script should work universally for anyone.  However you will need to update some of the hash strings based on your own individual accounts in the get_session_cookies script.  You can determine the ones for your account using a proxy like postman or mitmproxy, and search for these urls.  If I can further automate these in the future, I will update this script.  