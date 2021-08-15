#!/usr/bin/python3

import requests, sys, signal, re, subprocess, argparse

def arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", "--mask", help="Mask the shortened url", action="store_true", default=False)
	parser.add_argument("-u", "--url", help="The url that will be shortened", required=True)
	args = parser.parse_args()
	return args

def closeSignal(sig, frame):
	print("\n\n[*] Exiting...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, closeSignal)

main_url = "https://is.gd/create.php"

def makeRequest():

	post_data = {
		"url": url,
		"shorturl" : "",
		"opt" : "2",
	}

	r = requests.post(main_url, data=post_data)

	if "Sorry, the URL you entered is on our internal blacklist" in r.text:
		error = re.findall("<div id=\"main\"><p>(.*?)\<" ,r.text)[0]
		print("[!] Can't shorten url, reason:\n")
		print(error)
		sys.exit(1)


	shorter = re.findall("Your shortened URL is:\<\/b\>\<\/p\>\<input type=\"text\" class=\"tb\" id=\"short_url\" value=\"(.*?)\"", r.text)[0]
	go_to = re.findall("Your shortened URL goes to: (.*?)\<", r.text)[0]

	if mask:
		http = re.findall("(.*?:\/\/)", shorter)[0]
		shorter = shorter.replace(http, "")
		if words:
			shorter = domain + "-" + words + "@" + shorter
		else:
			shorter = domain + "@" + shorter
	else:
		pass

	print(f"\n[*] Your shortened URL is: {shorter}\n")
	print(f"[*] Your shortened URL goes to {go_to}\n")
	subprocess.Popen(f"echo {shorter} | tr -d '\n' | xclip -sel clip", shell=True)
	print("\t\t[*] Copied to clipboard\n")

if __name__ == '__main__':

	args = arguments()
	mask = args.mask
	url = args.url

	if not url.startswith("http://") and not url.startswith("https://"):
		print("[!] The url must start with http:// or https://")
		sys.exit(1)

	if mask:
		print("[*] Enter the domain to mask the url\nexample\n\thttps://www.google.com/, https://www.instagram.com, https://www.facebook.com")
		while True:
			domain = input("\ndomain> ")
			if not domain:
				print("[!] The domain is necessary")
				continue
			if not domain.startswith("https://") and not domain.startswith("http://"):
				print("[!] The http:// or https:// is necessary.")
				continue
			if domain.endswith("/"):
				domain = domain[:-1]
			break

		print("\n[*] Enter social engineering words\nexample:\n\telon-musks-number-leaked, pubg-gives-away-free-skins\n\tThe \"-\" are not necessary")
		while True:
			words = input("\nwords> ")
			if not words:
				chose = input("[!] Do you want to continue without the words? [Y/n] ")
				if chose.lower().startswith("n"):
					continue
			words = words.replace(" ", "-")
			break

	makeRequest()