import requests
import time

USERS = ["miles"]

def cur_ms_time():
    return round(time.time() * 1000)

# Classify post - by time range
def iter_user_post(user_id, time_range):
    """
    user_id: influencer's id
    time_range: time window, in hours
    
    return: a list of valid post id
    """
    min_time = cur_ms_time() - time_range*3600*1000
    URL = "https://api.gettr.com/u/user/{}/posts?offset=0&max=20&dir=fwd&incl=posts%7Cstats%7Cuserinfo%7Cshared%7Cliked&fp=f_uo".format(user_id)
    
    posts = requests.get(URL).json()["result"]["data"]["list"]

    cand_postid_ls = [] #postID in this class

    for post in posts:
        if post["cdate"] > min_time:
            cand_postid_ls.append(post["activity"]["pstid"])
            
    return cand_postid_ls

# Iterate commons
def iter_post_comments(post_id, time_range): 
    """
    post_id: 
    time_range: time window, in mins
    
    return: a list of valid comment id
    """
    min_time = cur_ms_time() - time_range*60*1000 # to ms
    URL = "https://api.gettr.com/u/post/{}/comments?offset=0&max=20&dir=rev&incl=posts%7Cstats%7Cuserinfo%7Cshared%7Cliked".format(post_id)
    
    comments = requests.get(URL).json()["result"]["data"]["list"] # comments
    
    cand_com_list = [] # comments that within the time windows

    for comment in comments:
        if comment["cdate"] > min_time:
            cand_com_list.append(comment["_id"])
            
    return cand_com_list

# Send to discord
def send_comments_to_discord(cand_com_list):
    # Pseudocode
    # Print the selected comment
    for com_id in cand_com_list:
        print("https://gettr.com/comment/" + com_id)

# Main
if __name__ == "__main__":
	
	for user in USERS:
	    post_list = iter_user_post(user, 6) #6hours
	    for post in post_list:
	        comms_list = iter_post_comments(post, 20) #10 mins
	        send_comments_to_discord(comms_list)