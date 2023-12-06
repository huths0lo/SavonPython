test = requests.get(url='https://assets.adobedtm.com/f785e82dd3f6/82777d7d7286/launch-b6e6e4763761.json')


response = {
    "global.privacy": "optedin",
    "__dev__campaign.pkey": "@NwdswItr6-OfVj0CeH_Io8bCYuiSG2xW0pJEAe_bZDIc-hACH18r-46TnEQHqE5UJeMLfwzmldky-gsR_kv0vI6vfNaP6XX05QrazKWbuOrr95WLMdqnGXO3swBOKzYMCYi3ZF_9eIzIiB4xOPdd236_wFD6Lw-8gS_vbrhhAVaHjL7j6vFiPBs87RtX4yEBheu7bw",
    "__stage__campaign.pkey": "@8at0S6QBLZTRl1AWHcl7iJ4LB0VTqRWjANzvayVE8u1MS_WCrErv3xi0Z7CS_RsHyWhbaD_QS8_dDwGIblt-r8amPNho7uxsEWcLPcDs3iytbz9PNLkXarD7qNsaOns8yQEbxxWnP6RQlW7JnntrX_oyk3GZQMO8pBB_VO1-kT-89mvHC-hga6b6QSY_43cS9pcPJw",
    "campaign.timeout": 5,
    "analytics.offlineEnabled": false,
    "__dev__analytics.rsids": "sfsafewaytest1",
    "campaign.mcias": "mcias-va7.cloud.adobe.io/mcias",
    "target.environmentId": 0,
    "campaign.pkey": "@zkJm-iptHCFypEcQT40HL2XSUIWED61QCwsdAXp3k-379QpKt2lh4YiIVzGZmMpPpDhHqbTotpvGMgGxfaQuGmWbFFt-lJY7QveKCbarWSnHpGAPWNcQ5iP77QCKaUfHAsAbwX8oZDDT4QylvK3iA4mXzsrTdwGbvN-KYQmcBfU7i7QFBZJA6dB_aSXlQ0i5mEV5tA",
    "__stage__analytics.rsids": "sfsafewayqa,sfsafewaytest2",
    "analytics.rsids": "sfsafewayprod1",
    "analytics.batchLimit": 0,
    "target.timeout": 5,
    "target.propertyToken": "",
    "analytics.launchHitDelay": 0,
    "analytics.backdatePreviousSessionInfo": false,
    "__stage__campaign.server": "safewayinc-mkt-stage4.campaign.adobe.com",
    "build.environment": "prod",
    "rules.url": "https://assets.adobedtm.com/f785e82dd3f6/82777d7d7286/launch-b6e6e4763761-rules.zip",
    "target.clientCode": "safewayinc",
    "experienceCloud.org": "A7BF3BC75245ADF20A490D4D@AdobeOrg",
    "lifecycle.sessionTimeout": 300,
    "campaign.server": "safewayinc-mkt-prod1.campaign.adobe.com",
    "__dev__campaign.server": "safewayinc-mkt-stage3.campaign.adobe.com",
    "analytics.server": "safeway.sc.omtrdc.net",
    "target.server": "safewayinc.tt.omtrdc.net",
    "property.id": "PRe8cb87aae9024d90b35b33ad9c1a5557",
    "analytics.aamForwardingEnabled": true
}

def step_2():
    url = 'https://dpm.demdex.net/id?d_rtbd=json&d_ver=2&d_orgid=A7BF3BC75245ADF20A490D4D@AdobeOrg&d_mid=83004351063505175235468967317664493943&d_blob=j8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI&dcs_region=9'
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU OS 17_1_2 like Mac OS X; en_US)',
        'accept-language': 'en-US',
        'accept-encoding': 'gzip, deflate, br'
    }
    response = requests.get(url=url, headers=headers)
    return response

