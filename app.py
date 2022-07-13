from selenium import webdriver
import tweepy
import json
import yaml
from yaml.loader import SafeLoader



def get_and_update_id_of_wordle(file):

	with open(file) as f:
		data = yaml.load(f, Loader=SafeLoader)
	
	ret_value = data["twitter"]["num"]			# save the id of wordle 
	data["twitter"]["num"] += 1					# change the id

	with open(file, 'w') as f:
		yaml.dump(data, f)

	return ret_value

def make_string_for_twitter(solution, id_of_wordle):

	string_for_twitter = "Today's solution of #Wordle" + id_of_wordle + " is:\n\n" + str(solution) + "\n\n#Wordle #bot #Solutions"

	return string_for_twitter



def tweet_message(api_key, api_secret_key, access_token, access_token_secret, text = ""):


	### Authorization protocol
	auth = tweepy.OAuthHandler(api_key, api_secret_key)
	auth.set_access_token(access_token, access_token_secret)

	### Providing access to API 
	API = tweepy.API(auth)

	### Taking tweet as an input
	tweet = text

	### Tweeting to the linked twitter account
	API.update_status(tweet)

	print("Posted on Twitter!!")


def get_wordle_solution():
	print("Opening Web browser...")

	driver = webdriver.Firefox() 
	print("Done!\n")
	print("Retrieving parameters from Web browser...")

	url='https://www.nytimes.com/games/wordle/index.html'
	try:	
		driver.get(url)
		scriptArray="""localStorage.setItem("key1", 'new item');
		               localStorage.setItem("key2", 'second item'); 
						return Array.apply(0, new Array(localStorage.length)).map(function (o, i) { return localStorage.getItem(localStorage.key(i)); }
						)""" 	
		
		result = driver.execute_script(scriptArray)
		print("Done!\n")
		print(result[0])

		res = json.loads(result[0])

		print(30 * "#" + "\n")
		print("The solution is:")
		print(res["solution"] + "\n")
		print(30 * "#" + "\n")
		print("Closing Web browser...")
	except Exception as e:
		with open("error.log", 'a') as f:
			error = f"Unexpected {e=}, {type(e)=}" + "\n"
			f.write(error)

		print("Exiting..")
		driver.quit()
		exit()


	driver.quit()
	
	print("Done!\n")

	return res["solution"]


def main():
	
	api_key = "<api_key>"
	api_secret_key = "<api_secret_key>"
	access_token = "<access_token>"
	access_token_secret = "<access_token_secret>"
	config_file = "<location_of_yaml>"
	
	sol = get_wordle_solution()
	wordle_id = get_and_update_id_of_wordle(config_file)
	
	tweet = make_string_for_twitter(sol, str(wordle_id))

	print(tweet)

	tweet_message(api_key, api_secret_key, access_token, access_token_secret, tweet)

	print("All finished properly!!\nNo errors found!!")


if __name__ == '__main__':
	
	main()
