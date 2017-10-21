# All of lines are config API Server
# config Host, port
HOST = '127.0.0.1'
PORT = '5003'
# Input url file spam training
INPUTSPAMURL = "data_training\\spam.train"
# Input url file not spam training
INPUTNSPAMURL = "data_training\\NSpam.train"
# Input url file stop words training
STOPWORDURL= "data_training\\stop_word.train"
# Input Url file test sample
SPAMTEXTURL = "test.txt"
# Input Url file model
SPAM_MODEL = "spam-model.pkl"
# Display predict
SPAM = 'SPAM'
NSPAM = 'NOT SPAM'
# Config kernel parameter
KERNEL_TYPE  = 'linear'
GAMMA = 'auto'
COST = 1.0
# Config type Message
FILE_W_SUCESS = 'FILE_W_SUCESS'
FILE_W_ERROR = 'FILE_W_ERROR'
FILE_W_EXISTS = 'FILE_W_EXISTS'
WF_CONTENT_EMPTY = 'WF_CONTENT_EMPTY'
# Config display output Message
MESS_W_SUCCESS = 'Lưu dữ liệu thành công'
MESS_W_ERROR = 'Có lỗi xảy ra khi xử lý dữ liệu '
MESS_W_EXISTS = 'Dữ liệu đã tồn tại trong hệ thống'
MESS_C_EMPTY = 'Dữ liệu trống'
MESS_UNDEFINED = 'Lỗi chưa xác định'