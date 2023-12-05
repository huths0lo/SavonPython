"# SavonPython"

This is a work in progress!

This application is intended to check once a day for new coupons in your vons account.  It will then clip all available coupons to maximize your grocery store savings.

If anyone would like to assist with completion of this code, the only problem I'm currently having is in obtaining the jwt.  I am able to logon through their OKTA flow, and get all of the cookies.  But I have not yet figured out how to get the JWT.

The coupon clipping code works, if I log on with a web browser, and then use the JWT and Cookie from my web browser.

Needs chrome 114 or less.  Binaries are in chrome_drivers folder.  Install on linux with:

sudo dpkg -i ./chrome_drivers/google-chrome-stable_current_amd64.deb