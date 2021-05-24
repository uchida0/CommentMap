#レビューコメントに対して紐づけして可視化するやつ
import  requests
from bs4 import BeautifulSoup
import MeCab
import urllib

# class
#from comment import Comment
import comment
#from morph import Morph

from DataStore.Comment_MongoDB import Comment_MDB


SLOTHLIB_PATH = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
SLOTHLIB_FILE = urllib.request.urlopen(SLOTHLIB_PATH)
SLOTHLIB_STOP_WORDS = [line.decode("utf-8").strip() for line in SLOTHLIB_FILE]
SLOTHLIB_STOP_WORDS = [ss for ss in SLOTHLIB_STOP_WORDS if not ss==u""]

StopWordJa = ["もの", "こと", "とき", "そう", "たち", "これ", "よう", "これら", "それ", "それら", "すべて", "あれ", "あれら", "どれ", "どこ"]
STOP_WORDS = list(set(SLOTHLIB_STOP_WORDS + StopWordJa))

comment_mdb = Comment_MDB()


#マップ作製
#return comment_number_length
def create_map(link):

    #dbのcollectionをリセット
    comment_mdb.reset_collection()

    comment_list = collect_comment(link)

    # Commentクラスをそれぞれ作成
    comments = []
    count = 0
    
    for cl in comment_list:
        c = comment.Comment(cl, count)
        c.make_morph()

        comments.append(c)
        
        count += 1

        
    cn = len(comment_list)

    #ループ回数に改善の余地あり
    for i in range(cn):
        comment1 = comments[i]
        for j in range(cn):
            comment2 = comments[j]
            if i is not j:
                comment1.create_morph_link(comment2)

    for c in comments:
        c.create_keyword_link_list()
    
    #デバッグ用
    #for  i in range(cn):
        #comment_test = comments[i]
        #comment_test.confirm_data()
    
    #MongoDBにデータ挿入する
    comment_mdb.insert_all(comments)

    #for com in comments:
        #print(com.__dict__)
        #print()

    #debug
    #comment_mdb.collect_comment_map(0, word_base="画面")

    return cn


#コメント収集
# return comment_list :list
def collect_comment(link):

    try:
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "html.parser")

        review_comments = soup.findAll("p", {"class": "revEntryCont"})
        comment_list = []

        for rc in review_comments:
            comment = rc.text
            comment_list.append(comment)

        return comment_list
    
    except Exception as e:
        print("リンクが間違っているかもしれません")
        exit(0)

    pass



#if __name__ == "__main__":
    #description = ("価格.comの商品レビューのリンクを貼ってください。\nレビューコメントをマップにします")
    #print(description)

    #link = input("商品レビューリンク：")

    #create_map(link)