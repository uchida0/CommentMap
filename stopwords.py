import urllib

SLOTHLIB_PATH = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
SLOTHLIB_FILE = urllib.request.urlopen(SLOTHLIB_PATH)
SLOTHLIB_STOP_WORDS = [line.decode("utf-8").strip() for line in SLOTHLIB_FILE]
SLOTHLIB_STOP_WORDS = [ss for ss in SLOTHLIB_STOP_WORDS if not ss==u""]

StopWordJa = ["もの", "こと", "とき", "そう", "たち", "これ", "よう", "これら", "それ", "それら", "すべて", "あれ", "あれら", "どれ", "どこ"]
STOP_WORDS = list(set(SLOTHLIB_STOP_WORDS + StopWordJa))