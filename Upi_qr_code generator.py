import qrcode
upi_id = input("enter your upi id : ")

phonepe_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234"
paytm_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234"
googlepay_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234"

phonepe_qr = qrcode.make(phonepe_url)
paytm_qr = qrcode.make(paytm_url)
googlepay_qr = qrcode.make(googlepay_url)



googlepay_qr.show()



