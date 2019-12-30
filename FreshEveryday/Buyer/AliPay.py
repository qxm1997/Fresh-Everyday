from alipay import AliPay


def aliPay(order_id,order_price):
    # 公钥
    alipay_public_key = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkQPdV5Yqrw7w52mcjC6zTDEAm/hTH51XlMocjMEOyUlFrTFzxe1C5yi9gom0tK7b+A+Da5jzE7ncwH2dL27iYEN5FHYs0lqcE1hNYSz9itf2j+O64D9ogSz0BBI9CIKfsqSXZpiICJ0W9O1Lg9EaYjyDNP73MoJPCiv02QGR0FTeVUbJDGvFY9qeXX9NCP6qbieXq81/0DkPttrPr3cP7fAM0xKzzr5CXQZLX+20DAQ38nULdosZMvImRL1KHuZVxMtafbL/JQ4/4r937NcO2jPfYi9026txL2hYZWFMdWg82Vb1iRflRCNkl8ynwsAG9KroHMNbN0pxub8IhATG4wIDAQAB
    -----END PUBLIC KEY-----'''

    # 私钥
    app_private_key = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAkQPdV5Yqrw7w52mcjC6zTDEAm/hTH51XlMocjMEOyUlFrTFzxe1C5yi9gom0tK7b+A+Da5jzE7ncwH2dL27iYEN5FHYs0lqcE1hNYSz9itf2j+O64D9ogSz0BBI9CIKfsqSXZpiICJ0W9O1Lg9EaYjyDNP73MoJPCiv02QGR0FTeVUbJDGvFY9qeXX9NCP6qbieXq81/0DkPttrPr3cP7fAM0xKzzr5CXQZLX+20DAQ38nULdosZMvImRL1KHuZVxMtafbL/JQ4/4r937NcO2jPfYi9026txL2hYZWFMdWg82Vb1iRflRCNkl8ynwsAG9KroHMNbN0pxub8IhATG4wIDAQABAoIBAETq20SG31428ZJpBLcyco+hMjLtv0NlGXxi2VKjZY2PvwdiWy0TZxpIqFfjbff4qh2n8cMu+0bCrADnMc6bGga5yk9JImAOI+KlspCeOxjDLjCP//4W5GmPnaBZspvayF60Dif6EZxWW9Sm+Z55v9oz+/8xtPVSLJIe9cw0DMI++MZUeIroNzMYS9UCtgad7kddqjF77oXBzpcL3t1d+fmGtuimChIGzUmArt5sKtVEKY0DPVAWPNmI1dM54QgD6UXWDMkrR0aSc2ge4dowAd6Tk4QSx6D5JLGFEvC+id7d9DerZtyk69TA6Dy3wD9RWy1tRgmjSV34NlWkqA0ynxECgYEA6Mv9XfnJrhibSqf5au4kvM4muktIUu6MwXjD5C9EaK1bQjj5CU/kMM5F5gKWGM9EsvsTN+ia4EFKD7efdJSpViLrnBRbMOdMOfPDxXkbuCpO/S9Y8wq7RF5sHjLQlz2uebTOGGdM2GIzbG8FrtlQB11MIWt5BE7yQb/oE8XIU08CgYEAn3gMfT4fro1Z/9gwEIy9L52i/KaD5J6ZteoZsuRihzvXWSF7TlbudU4hmFDGRyQ61fuqiDisqwfNV+1u8MvWYKfYyPzt3vXsSYqOhyCWAX81CbhZxcrRDzA3c8RyVy09OusRanBSmZm/uuUyo06Fue8dyCoe1ZtZWiA/sIYPPi0CgYAhy4tKmzqGBZh1rBDvTwcSSbMhlFA5idvxMkDt3VbHA3OeF3s/uNNdqnRHQdTcYSqN+Rj/IstpBtFjmrqRSAuVL5iYnfPnE4zjVNn0zvIROEMjSj5VehdZg4OalrHlYtTzYiYRMN3dA9SHR07B5VZS215z85Ar6fINTXi5dhrwzQKBgDSOXRddxRVDErlGJ7kcmTE7M78upeNP/fq9V5DkwjAtobCHX1sXPWm9wUawwFgr8ZQaaD6S5x1K6fsjjl+f3lxmlQTQjxjfVet61bRlIesGYJV+g1+zkyj9TBlEUia3CyoC1O+OazqiOFVBOmol896ultMkRptBorYYUMU9uYJVAoGAHpsthlIDh8gPqtEISawox1eoE7fG+qEJgjiUNh9iBVk6I/5BzVhUbYvkp6Q3F660faB0pg4pF6cR501O0zElgJfDBmCQmwHYk8RAbC1X41jjxU0qY2Rf8RekNeSjGZzvZ8CeJvb0nJYc3UJ9eLyHjbbyKlfEUDbcURDEJqi2tqg=
    -----END RSA PRIVATE KEY-----'''

    ## 2. 实例化一个支付对象
    ali_pay = AliPay(
        ## app id
        appid='2016101500694171',
        app_notify_url=None,
        app_private_key_string=app_private_key,
        alipay_public_key_string=alipay_public_key,
        sign_type="RSA2",
    )



    ## 3. 构建支付订单信息
    ## 网页支付
    order_info = ali_pay.api_alipay_trade_page_pay(
        subject="沙箱支付",   ### 交易的主题
        out_trade_no= order_id,    ### 订单号
        total_amount= order_price,    ### 交易金额  字符串
        return_url= "http://127.0.0.1:8000/buyer/hhh/",     ### 回调地址
        notify_url= "http://127.0.0.1:8000/buyer/hhh/",     ## 通知地址
    )


    ##  4. 返回支付宝支付链接
    url = "https://openapi.alipaydev.com/gateway.do?" + order_info

    return url


# from alipay import AliPay
#
#
# def aliPay(order_id,order_price):
#     ## 公钥
#     alipay_public_key = """-----BEGIN PUBLIC KEY-----
#     MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhtoL7Dd0agpcnuawx39CN+LkPWRKsAAEgG4simcOGM5E3we88/NMUii/55laKISPzXLqst+u3WmSD5OU2dRbIX5lBXEMqZ2BN3c9rr1b/+XUHfHyvHjzcSOWhddr2fOg/tPOceCj3nqe8ViFMjNhR2RFXK6K3XZb8RT+mg9pvg5UPkcW/9Ffuuk1KTkliRZhnQ5k1WJjCmlx8hJNTrG5xkp3qHGrvgxGSmQFkSXPTyG5Md0YsxEBNSeEH+gxit9garlhU41hdavRrVS/tLcRoeEsTyQMtSR6Upr7IGH4V5UC65RbxOzHQX+2iqQUJ4iSN6Wl1f24bJYQAiS6leXQKQIDAQAB
#     -----END PUBLIC KEY-----"""
#     ## 私钥
#     alipay_private_key = """-----BEGIN RSA PRIVATE KEY-----
#     MIIEowIBAAKCAQEAhtoL7Dd0agpcnuawx39CN+LkPWRKsAAEgG4simcOGM5E3we88/NMUii/55laKISPzXLqst+u3WmSD5OU2dRbIX5lBXEMqZ2BN3c9rr1b/+XUHfHyvHjzcSOWhddr2fOg/tPOceCj3nqe8ViFMjNhR2RFXK6K3XZb8RT+mg9pvg5UPkcW/9Ffuuk1KTkliRZhnQ5k1WJjCmlx8hJNTrG5xkp3qHGrvgxGSmQFkSXPTyG5Md0YsxEBNSeEH+gxit9garlhU41hdavRrVS/tLcRoeEsTyQMtSR6Upr7IGH4V5UC65RbxOzHQX+2iqQUJ4iSN6Wl1f24bJYQAiS6leXQKQIDAQABAoIBADFoeq3Vs6WWnlDqHSM7ETwAubd0o5jQqNWViGQ9VgDosns1DpojLnd7zrRAj7QAvd98l1lqc1tUbtueKw+Uqr8e3EyeGxGaT9nOqp73alncD1fZaiJ7/lYZv/DR+QYmKXq0iBNZRzEgpFOxJzw5bw8FQhSvLtntn8o48v/nXcrwVA0th+3rjmchgsuzxVrgii1S0XjCGyv9fXbHVboYPScE4sMTKJKlNvC3cHsAohyo6hwzKwtzbzQNRDM+5w+euYimjf8eM72De9B2TKtszALWOhkHJrsbuprZUsiT0gs43DT3gLXjwmvz15eBK5phxP6P3WCaELrngoopJ64s28ECgYEA0CcY85agMB+FLUPqqbRHwgB1WhwUUFDFmPUgxf+hAhK6EEqkc7Ykf9hBAeTSUQbDxfs2t7l826XCwwF8qXkPOtecmQvoKAC4OzEG/QaDaVOzyT0LJfVKYd+6xnp8+Uy34HL1FmpYRkums71JccC1x4MofDNX09g10LI+8SyLHCUCgYEApdl/iVbRReysdvlSkP9uqQQ3JBozHz2T4fu9qpqcpR2vxZIFjp/U6LZNIpuN/aaJzXXhHAg45mhpJOdKB8P3XkHJbNSWDgwCdPeGuPtJ94tZeOm90EBQ7ggioTPrG/dYC2xX6ElugODMpg41oLNbbyRWp4/j16XQuvc9vpY2IrUCgYAInEVs9iMkOnmQ2MlhQcLiJJC2LIkulVjHLgSwDBYF9u5ZdCz/WF6EJ1bxFB0bGvOIQg8OZI7kqyO2W15jyE03+ulQb2yoEveMA0gtuVJATiUWwv6uEEqGZ/Ha+gAnc+P7VeYLilSie8imkML0AKvEWAmZsaoFamE3g9gUs+oBPQKBgDw8idjdAndOJbm0hmuJiqyyjkB7j5PKLrsGTvX23+wMozmz9na90HuRMuTd8K1u3mAUb2VaCyiMRZwUsUuuvlqqtDjl4XZKoF3RRUpMYqoZH68N3lYT9hDuPX2lOMBYjs7fU/JXMV53x3yMbqfmXNA6N4r2dP9vByfRAskFD7Z9AoGBAI1jexPHEFTAM25/RuQF5Qc7Mrr+HY5CseboGkJZ/nlyvL8yafM2R8KlsvVStJ4sB1BG4S8b+QCHJR9BqRgT3sDuHFUp51yyMQNocXqi7icwIwYoyCUUf56aFujIrUFvDsrhf5x+Pj95GluYcBtRT46PeylzliVH73lkgwESG38/
#     -----END RSA PRIVATE KEY-----"""
#
#
#
#     ## 2. 实例化一个支付对象
#     ali_pay = AliPay(
#         ## app id
#         appid = "2016101300673550",
#         ## app 通知地址
#         app_notify_url = None,
#         ## 私钥  字符串
#         app_private_key_string=alipay_private_key,
#         ## 公钥
#         alipay_public_key_string=alipay_public_key,
#     )
#
#
#
#     ## 3. 构建支付订单信息
#     ## 网页支付
#     order_info = ali_pay.api_alipay_trade_page_pay(
#         subject="沙箱支付",   ### 交易的主题
#         out_trade_no= order_id,    ### 订单号
#         total_amount= order_price,    ### 交易金额  字符串
#         return_url= "http://127.0.0.1:8000/Buyer/hhh/",     ### 回调地址
#         notify_url= "http://127.0.0.1:8000/Buyer/hhh/",     ## 通知地址
#     )
#
#
#     ##  4. 返回支付宝支付链接
#     url = "https://openapi.alipaydev.com/gateway.do?" + order_info
#
#     return url
