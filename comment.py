import MeCab
#from  morph import Morph
import morph

# param
# class Morph -> Link
# 形態素ごとにリンクを持つ
# comment_number

class Comment:

    #各単語について扱いたいから形態素にして全文を復元する方式を取る
    def __init__(self, comment, comment_number):
        self.comment = comment
        self.comment_number = comment_number
        self.morph_list = []
        self.sellected_word_base_list = []
        self.haslink_word_base_list = {}
        
    
    # Morphクラスに作成していく
    def make_morph(self):
        tagger = MeCab.Tagger()
        tagger.parse("")
        node = tagger.parseToNode(self.comment)

        while node:
            word_surf = node.surface.split(",")[0]
            pos = node.feature.split(",")[0]
            #基本形
            word_base = node.feature.split(",")[6]

            m = morph.Morph(word_surf, word_base, pos, self.comment_number)
            m.sellect_word()

            if m.sellected:
                self.sellected_word_base_list.append(m.word_base)

            self.morph_list.append(m)

            node = node.next


    #形態素からコメント全文を復元
    def get_comment(self):
        pass

    
    #リンクさせるべき形態素の一覧を取得する
    def create_keyword_link_list(self):
        for morph in self.morph_list:
            if morph.link_list:
                self.haslink_word_base_list[morph.word_base] = morph.link_list



    def create_morph_link(self, other_comment):
        for morph in self.morph_list:
            morph.create_link(other_comment)

    
    #デバッグ用
    def confirm_data(self):
        print("comment_number:")
        print(self.comment_number)
        print(self.sellected_word_base_list)

        for morph in self.morph_list:
            print(morph.link_list)