# %%
import base64
data = b'ETI9f/T2us5aCHjU4uBEPwWthx5KSidNzcfVifXxmMw5bw/kSbj2hKISc/IFdBcaSKGXkY6MD7WVDtpUmh t4rw9KtvkxZp4kButMbcALjVAHOgICYreVALv/AI='
missing_padding = len(data) % 4
if missing_padding != 0:
    data += b'='* (4 - missing_padding)
a = base64.b64decode(data, '-_')
a = base64.urlsafe_b64decode(data)

# print(a.decode('utf-8'))
print(a.decode('utf-8', errors='ignore'))
print(a)
# %%
