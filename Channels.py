from main import Youtube

channel_1 = Youtube('UCMCgOm8GZkHp8zJ6l7_hIuA')  # Вдудь
channel_2 = Youtube('UC1eFXmJNkjITxPFWTy6RsWg')  # Редакция
print(channel_1.channel_title)
print(Youtube.get_service())

total_subscribers = channel_1 + channel_2
print(total_subscribers)
total_subscribers = channel_1 < channel_2
print(total_subscribers)
total_subscribers = channel_1 > channel_2
print(total_subscribers)
