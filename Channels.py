from main import*

channel_1 = Youtube('UCMCgOm8GZkHp8zJ6l7_hIuA')  # Вдудь
channel_2 = Youtube('UC1eFXmJNkjITxPFWTy6RsWg')  # Редакция
print(channel_1.channel_title)
print(channel_1.subscriber_count)

total_subscribers = channel_1 + channel_2
print(total_subscribers)
total_subscribers = channel_1 < channel_2
print(total_subscribers)
total_subscribers = channel_1 > channel_2
print(total_subscribers)

video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')

print(video2)

pl = Playlist('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')

duration = pl.total_duration
print(pl.playlist_title)

print(pl.playlist_info)
print(pl.video_ids)