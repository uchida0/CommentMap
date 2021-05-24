# キーワードリスト
from flask import Flask
from flask import url_for, redirect, render_template, request
import comment_map
from DataStore.Comment_MongoDB import Comment_MDB
import comment
import morph



app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":

        #link = request.form.get("revlink")
        #MongoDBに格納
        #comment_map.create_map(link)

        return render_template("result_map.html", comment_number = 0)
        
    elif request.method == "GET":

        return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def review_map():
    
    if request.method == "POST":

        link = request.form.get("revlink")
        comment_number = request.form.get("new_comment_number")
        word = request.form.get("keyword")

        if link:
            print(request)
            #MongoDBに格納
            c_num = comment_map.create_map(link)
            
            #comment_number0,keyword_number0が必要

            words, main_comment_text, tolink_comment_text_list, all_comment_num = comment_map.comment_mdb.collect_comment_map(comment_number=0)


            return render_template("result_map.html", comment_num=all_comment_num, keywords=words,main_ctext=main_comment_text, tolink_ctext_list=tolink_comment_text_list, main_comment_number=0)
        
        #else:
        elif comment_number:
            #comment_number = request.form.get("new_comment_number")
            comment_number = int(comment_number)
            print(type(comment_number))
            print(comment_number)
            #comment_number = int(comment_number)
            #word = request.form.get("keyword")

            words, main_comment_text, tolink_comment_text_list, all_comment_num = comment_map.comment_mdb.collect_comment_map(comment_number=comment_number)

            return render_template("result_map.html", comment_num=all_comment_num, keywords=words, main_ctext=main_comment_text, tolink_ctext_list=tolink_comment_text_list, main_comment_number=comment_number)


    #elif request.method == "GET":

        elif word:
            comment_number = request.form.get("comment_number")
            comment_number = int(comment_number)
            print(type(comment_number))
            print(comment_number)
            #comment_number = int(comment_number)
            #word = request.form.get("keyword")
            print(type(word))
            print(word)

            words, main_comment_text, tolink_comment_text_list, all_comment_num = comment_map.comment_mdb.collect_comment_map(comment_number=comment_number, word_base=word)

            return render_template("result_map.html", comment_num=all_comment_num, keywords=words, main_ctext=main_comment_text,tolink_ctext_list=tolink_comment_text_list, main_comment_number=comment_number)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

