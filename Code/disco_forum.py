from pymongo import MongoClient
import pymongo
import sys,random
from datetime import datetime
from pprint import pprint

def today():
    now = datetime.now()
    return now.strftime("%Y-%m-%d" "T" "%H:%M:%S.%f")

def post_question(db,user_id):

    title = input("Enter title: ")
    body = input("Enter body: ")
    tags_s = input("Enter tags(separate with space. Use '-' to create single tag of multiple words: ")
    tags = tags_s.split()
    tag_str = ""
    if not tags_s.isspace():
        for tag in tags:
            tag_str += "<" + tag + ">"
            tag = "^"+tag+"$"
            result = db.tags.find_one_and_update({"TagName": {"$regex": tag, "$options": "i"}},{"$inc": {"Count": 1}})
            print(result)
            print(tag)
            if result is None:
                while True:
                    try:
                        tag_id = random.randint(1, 1000000)
                        tag_doc = {
                                "Id": str(tag_id),
                                "TagName": tag,
                                "Count": 1
                                }
                        db.tags.insert_one(tag_doc)
                    except pymongo.errors.DuplicateKeyError:
                        continue
                    else:
                        break

    while True:
        try:
            post_id = random.randint(1,1000000)
            if not tags_s.isspace():
                if user_id.isspace() or user_id == '':
                    post = {
                            "Id": str(post_id),
                            "PostTypeId": "1",
                            "CreationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "Score": 0,
                            "ViewCount": 0,
                            "Body": body,
                            "AnswerCount": 0,
                            "CommentCount": 0,
                            "Title": title,
                            "Tags": tag_str,
                            "FavoriteCount": 0,
                            "ContentLicense": "CC BY-SA 2.5"
                        }

                else:
                    post = {
                            "Id": str(post_id),
                            "PostTypeId": "1",
                            "CreationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "Score": 0,
                            "ViewCount": 0,
                            "Body": body,
                            "OwnerUserId": user_id,
                            "AnswerCount": 0,
                            "CommentCount": 0,
                            "Title": title,
                            "Tags": tag_str,
                            "FavoriteCount": 0,
                            "ContentLicense": "CC BY-SA 2.5"
                        }

            else:
                if user_id.isspace() or user_id == '':
                    post = {
                            "Id": str(post_id),
                            "PostTypeId": "1",
                            "CreationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "Score": 0,
                            "ViewCount": 0,
                            "Body": body,
                            "AnswerCount": 0,
                            "CommentCount": 0,
                            "Title": title,
                            "FavoriteCount": 0,
                            "ContentLicense": "CC BY-SA 2.5"
                        }

                else:
                    post = {
                            "Id": str(post_id),
                            "PostTypeId": "1",
                            "CreationDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "Score": 0,
                            "ViewCount": 0,
                            "Body": body,
                            "OwnerUserId": user_id,
                            "AnswerCount": 0,
                            "CommentCount": 0,
                            "Title": title,
                            "FavoriteCount": 0,
                            "ContentLicense": "CC BY-SA 2.5"
                        }
            print(post_id)
            print("posted")
            db.posts.insert_one(post)
        except pymongo.errors.DuplicateKeyError:
            continue
        else:
            break
    return

def search_question(db, user_id):
    search_result = []
    pid_displayed = 0
    keywords = input("Enter keywords separated by space. Use '-' for entering more than one word keyword: ")
    keywords = keywords.split()
    for keyword in keywords:
        result = db.posts.find({"Title":{"$regex":keyword}})
        for doc in result:
            search_result.append(doc)
    for doc in search_result:
        if pid_displayed%5==0 and pid_displayed !=0:
            u_in = input("Enter p to select a post; Enter any other letter to view more: ")
            if u_in.lower() == 'p':
                break
        print('*'*80)
        print("PostID: "+doc["Id"])
        print("Title: "+doc["Title"])
        print("Date: "+doc["CreationDate"])
        print("Score: "+str(doc["Score"]))
        print("Answers: "+str(doc["AnswerCount"]))
        print('*'*80)
        pid_displayed += 1
    pid = input("Enter PostID to select a post: ")
    if pid.isnumeric():
        select_question(db,pid,user_id)
    else:
        print("Invalid pid")
    return


def select_question(db,pid,uid):
    """This function selects a post updates view count and prints the all the post details"""
    result = db.posts.find_one_and_update({"Id": pid},{"$inc": {"ViewCount":1}}) # increases view count of post
    if result is None:
        print("No such pid")
    else:
        pprint(result)
        u_in = input("1. Answer\n2. View all answers\n3. Vote\n4. Return to main menu\nWhat would you like to do?: ")
        if u_in == '1':
            answer(db, pid, uid)
        elif u_in == '2':
            answer_list(db, pid, uid)
        elif u_in == '3':
            vote(db, pid, uid)
        elif u_in == '4':
            return
        else:
            print('Invalid choice. Please select from the given options')
            select_question(db, pid, uid)
        return

def answer(db, qid, uid):
    """records answer into the posts database by creating a unique id and connecting with
        it's corresponding question"""
    posts_coll = db["posts"]
    ans = input("Type in your answer: ")
    date = today()
    while True:
        # try to insert the recorded answer into the database and if the mentioned
        # error occurs, create another pid. This continues until it has been recorded.
        try:
            pid = random.randint(1, 1000000)
            if not uid.isspace() and uid != '':
                posts_coll.insert_one(
                    {'Id':str(pid), "PostTypeId":"2", "ParentId":qid, "CreationDate":date, "Score":0, 
                    "Body":ans, "OwnerUserId":uid, "LastActivityDate":date, "CommentCount":0, "ContentLicense":"CC BY-SA 2.5"}
                )
            else:
                posts_coll.insert_one(
                    {'Id':str(pid), "PostTypeId":"2", "ParentId":qid, "CreationDate":date, "Score":0, 
                    "Body":ans, "LastActivityDate":date, "CommentCount":0, "ContentLicense":"CC BY-SA 2.5"}
                )
            print("Answer posted!")
        except pymongo.errors.DuplicateKeyError:
            continue
        else:
            break
    return

def answer_list(db, qid, uid):
    """displays a list of all the answers for the selected question"""
    posts_coll = db["posts"]
    # cursor for all the answers
    ansList = posts_coll.find({ '$and': [{'PostTypeId':'2'}, {'ParentId':qid}]})
    q = posts_coll.find_one({'Id':qid})
    a = ''
    # if the question has an accepted answer, print first and with a star
    try:
        a = posts_coll.find_one({'Id':q['AcceptedAnswerId']})
        body = a['Body']
        date = a['CreationDate']
        score = (a['Score'])
        print('*'+ a['Id']+'||'+body[0:80].rstrip()+'||'+date+'||'+str(score))
    except:
        pass
    # then print the rest or if the question doesnt have an accepted answer,
    # below prints all the answers in the specified format
    for ans in ansList:
        if a != '':
            if ans == a:
                continue
        body = ans['Body'][0:80]
        date = ans['CreationDate']
        score = (ans['Score'])
        print(ans['Id'], end='||')
        print(body.rstrip(), end='||')
        print("Date: "+date, end='||')
        print("Score: "+score)
    # to select an answer or quit the program
    while True:
        opt = input("Do you want to select answer?(y/n) ")
        if opt == 'y':
            ansList = posts_coll.find({ '$and': [{'PostTypeId':'2'}, {'ParentId':qid}]})
            select_answer(db, ansList, uid)
            break
        elif opt == 'n':
            break
        else:
            print("Input a valid option")
    return

def select_answer(db, ansList, uid):
    """displays selected answer and prompts to vote"""
    aid = input("Type in the id of the answer you wish to select: ")
    ans = {}
    for doc in ansList:
        if doc['Id'] == aid:
            ans = doc
    print('Id: ', ans['Id'])
    print('PostTypeId: ', ans['PostTypeId'])
    print('ParentId: ', ans['ParentId'])
    print('CreationDate: ', ans['CreationDate'])
    print('Score: ', ans['Score'])
    print('Body: ', ans['Body'])
    # if the field OwnerUserId exists for the answer then print it
    # otherwise print none
    try:
        print('OwnerUserId: ', ans['OwnerUserId'])
    except:
        print('OwnerUserId: ', None)
    print('LastActivityDate: ', ans['LastActivityDate'])
    print('CommentCount: ', ans['CommentCount'])
    print('ContentLicense: ', ans['ContentLicense'])

    while True:
        opt = input("Do you want to vote?(y/n) ")
        if opt == 'y':
            vote(db, aid, uid)
            break
        elif opt == 'n':
            break
        else:
            print("Input a valid option")
    return


def vote(db, pid, uid):
    """casts vote if the non-anonymous user hasn't voted already"""
    votes_coll = db['votes']
    posts_coll = db['posts']
    # if user is logged in
    if not uid.isspace() and uid != '':
        # and if the user already voted, exit out of the function
        if votes_coll.count_documents({'PostId': pid, 'UserId': uid}) > 0:
            print("You have already voted on this post")
            return
    date = today()
    while True:
        # inserts the vote into the votes database with a unique Id and
        # updates the score of the post
        try:
            vid = random.randint(1, 10000000)
            if not uid.isspace() and uid != '':
                my_dict = {'Id':vid, 'PostId':pid, 'VoteTypeId':'2', 'UserId':uid, 'CreationDate':date}
            else:
                my_dict = {'Id':vid, 'PostId':pid, 'VoteTypeId':'2', 'CreationDate':date}
            votes_coll.insert_one(my_dict)
            posts_coll.update_one({'Id': pid}, {"$inc": {'Score': 1}})
            print("vote casted!")
        except pymongo.errors.DuplicateKeyError:
            continue
        else:
            break
    return


def main_menu(db, user_id):
    """maim menu for user interface"""
    while True:
        action = input("What would you like to do?\n[P]ost a question (or) [S]earch (or) [E]xit: ").lower()
        if action == 'p':
            post_question(db,user_id)
        elif action == 's':
            search_question(db, user_id)
        elif action == 'e':
            break
    return


def main():
    random.seed()
    port = input("Enter port number: ")
    client = MongoClient('mongodb://localhost:'+port)
    db = client["291db"]
    logged_in = True
    db.votes.create_index([("Id", -1)], unique=True)
    db.tags.create_index([("Id",-1)], unique = True)
    db.posts.create_index([("Id", -1)], unique=True)
    while logged_in:
        user_id = input("Enter userid or press enter to use anonymously: ")
        if not user_id.isspace() and user_id != '':
            #num of questions owned, average score for those questions
            #answers owned and avg score
            #votes registered
            question_info = db.posts.aggregate([
                {"$match": {"OwnerUserId": user_id}},
                {"$match": {"PostTypeId": '1'}},
                {"$group": {"_id": "$OwnerUserId", "total":{"$sum": 1}, "avg_score": {"$avg":"$Score"}}}
            ])
            for doc in question_info:
                print("Questions posted: "+str(doc['total'])+" || Average question score: "+str(doc['avg_score']))
            answer_info = db.posts.aggregate([
                {"$match": {"OwnerUserId": user_id}},
                {"$match": {"PostTypeId": '2'}},
                {"$group": {"_id": "$OwnerUserId", "total":{"$sum": 1}, "avg_score": {"$avg":"$Score"}}}
            ])
            for doc in answer_info:
                print("Answers posted: "+str(doc['total'])+" || Average answer score: "+str(doc['avg_score']))
            vote_info = db.votes.aggregate([
                {"$match": {"UserId": user_id}},
                {"$group": {"_id": "$UserId", "total": {"$sum": 1}}}
            ])
            for doc in vote_info:
                print("Votes Registered: "+str(doc['total']))
        main_menu(db, user_id)
        return


if __name__ == "__main__":
    main()
